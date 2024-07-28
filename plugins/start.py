import asyncio
import base64
import logging
import os
import random
import re
import string
import time

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
    OWNER_ID,
    AUTO_DELETE_SECONDS
)
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_user, del_user, full_userbase, present_user
from shortzy import Shortzy

"""add time in seconds for waiting before delete 
1 min = 60, 2 min = 60 × 2 = 120, 5 min = 60 × 5 = 300"""
SECONDS = int(AUTO_DELETE_SECONDS)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    owner_id = OWNER_ID

    # Check if the user is the owner
    if id == owner_id:

        await message.reply("You are the owner! Additional actions can be added here.")

    else:
        if not await present_user(id):
            try:
                await add_user(id)
            except:
                pass

        verify_status = await get_verify_status(id)
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)

        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply("𝑌𝑜𝑢𝑟 𝑡𝑜𝑘𝑒𝑛 𝑖𝑠 𝑖𝑛𝑣𝑎𝑙𝑖𝑑 𝑜𝑟 𝐸𝑥𝑝𝑖𝑟𝑒𝑑. 𝑇𝑟𝑦 𝑎𝑔𝑎𝑖𝑛 𝑏𝑦 𝑐𝑙𝑖𝑐𝑘𝑖𝑛𝑔 /start")
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            if verify_status["link"] == "":
                reply_markup = None
            await message.reply(f"𝑌𝑜𝑢𝑟 𝑡𝑜𝑘𝑒𝑛 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦 𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑 𝑎𝑛𝑑 𝑣𝑎𝑙𝑖𝑑 𝑓𝑜𝑟: {get_exp_time(VERIFY_EXPIRE)}", reply_markup=reply_markup, protect_content=False, quote=True)

        elif len(message.text) > 7 and verify_status['is_verified']:
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end+1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            temp_msg = await message.reply("𝑃𝑙𝑒𝑎𝑠𝑒 𝑤𝑎𝑖𝑡....")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("𝑆𝑜𝑚𝑒𝑡ℎ𝑖𝑛𝑔 𝑤𝑒𝑛𝑡 𝑤𝑟𝑜𝑛𝑔 .!")
                return
            await temp_msg.delete()
            
            snt_msgs = []
            
            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                    snt_msgs.append(snt_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    snt_msgs.append(snt_msg)
                except:
                    pass

            SD = await message.reply_text(f"𝐹𝑖𝑙𝑒𝑠 𝑤𝑖𝑙𝑙 𝑏𝑒 𝑑𝑒𝑙𝑒𝑡𝑒𝑑 𝑖𝑛 {SECONDS} 𝑠𝑒𝑐𝑜𝑛𝑑𝑠 𝑡𝑜 𝑎𝑣𝑜𝑖𝑑 𝑐𝑜𝑝𝑦𝑟𝑖𝑔ℎ𝑡 𝑖𝑠𝑠𝑢𝑒𝑠. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑓𝑜𝑟𝑤𝑎𝑟𝑑 𝑡ℎ𝑒 𝑓𝑖𝑙𝑒𝑠.")
            await asyncio.sleep(SECONDS)

            for snt_msg in snt_msgs:
                try:
                    await snt_msg.delete()
                    await SD.delete()
                except:
                    pass

        elif verify_status['is_verified']:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("𝐴𝑏𝑜𝑢𝑡 𝑀𝑒", callback_data="about"),
                  InlineKeyboardButton("𝐶𝑙𝑜𝑠𝑒", callback_data="close")]]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )

        else:
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                short_url = f"instantearn.in"
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                    [InlineKeyboardButton("𝐶𝑙𝑖𝑐𝑘 𝐻𝑒𝑟𝑒e", url=link)],
                    [InlineKeyboardButton('𝐻𝑜𝑤 𝑡𝑜 𝑢𝑠𝑒 𝑡ℎ𝑒 𝑏𝑜𝑡', url=TUT_VID)]
                ]
                await message.reply(f"𝑌𝑜𝑢𝑟 𝐴𝑑𝑠 𝑡𝑜𝑘𝑒𝑛 𝑖𝑠 𝑒𝑥𝑝𝑖𝑟𝑒𝑑, 𝑟𝑒𝑓𝑟𝑒𝑠ℎ 𝑦𝑜𝑢𝑟 𝑡𝑜𝑘𝑒𝑛 𝑎𝑛𝑑 𝑡𝑟𝑦 𝑎𝑔𝑎𝑖𝑛. 🏚️🗝️.\n\n𝑇𝑜𝑘𝑒𝑛 𝑇𝑖𝑚𝑒𝑜𝑢𝑡: {get_exp_time(VERIFY_EXPIRE)}\n\n𝑊ℎ𝑎𝑡 𝑖𝑠 𝑡ℎ𝑒 𝑡𝑜𝑘𝑒𝑛?\n\n𝑇ℎ𝑖𝑠 𝑖𝑠 𝑎𝑛 𝑎𝑑𝑠 𝑡𝑜𝑘𝑒𝑛. 𝐼𝑓 𝑦𝑜𝑢 𝑝𝑎𝑠𝑠 1 𝑎𝑑, 𝑦𝑜𝑢 𝑐𝑎𝑛 𝑢𝑠𝑒 𝑡ℎ𝑒 𝑏𝑜𝑡 𝑓𝑜𝑟 6 𝐻𝑜𝑢𝑟 𝑎𝑓𝑡𝑒𝑟 𝑝𝑎𝑠𝑠𝑖𝑛𝑔 𝑡ℎ𝑒 𝑎𝑑. 💌", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)



    
        
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "𝐽𝑜𝑖𝑛 𝐶ℎ𝑎𝑛𝑛𝑒𝑙 🔔",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '𝑇𝑟𝑦 𝑎𝑔𝑎𝑖𝑛',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total users      : <code>{total}</code>
Successful       : <code>{successful}</code>
Blocked accounts : <code>{blocked}</code>
Deleted accounts : <code>{deleted}</code>
Unsuccessful     : <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
