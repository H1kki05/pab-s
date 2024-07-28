import os
import logging
from logging.handlers import RotatingFileHandler

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID & API HASH from my.telegram.org
#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002241642612"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Hanielx")


#auto delete seconds in seconds add time in seconds for waiting before delete 1 min = 60, 2 min = 60 × 2 = 120, 5 min = 60 × 5 = 300
AUTO_DELETE_SECONDS = int(os.environ.get("AUTO_DELETE_SECONDS", "300"))

#Shortner (token system) 
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 21600)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "") 

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002147381718"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "8"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>𝐻𝑒𝑦 {first}</b>\n\n<b>𝑊𝑒𝑙𝑐𝑜𝑚𝑒 𝑡𝑜 𝑡ℎ𝑒 𝐻𝑎𝑛𝑖𝑒𝑙 𝐹𝑖𝑙𝑒 𝑆𝑡𝑜𝑟𝑒 𝐵𝑜𝑡!✨ </b>\n \n<b><a href='https://t.me/+WA5vFPHEMfJmODk1'>𝑊𝑎𝑡𝑐ℎ 𝑚𝑜𝑣𝑖𝑒𝑠/𝑡𝑣 𝑠ℎ𝑜𝑤𝑠 🍿🌟 </a></b>\n \n<b><a href='https://t.me/+ddfydq6pKYtmNjU9'>𝑊𝑎𝑡𝑐ℎ 𝑒𝑥𝑐𝑙𝑢𝑠𝑖𝑣𝑒 𝑐𝑜𝑛𝑡𝑒𝑛𝑡 🎥🔞</a></b>")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "6612030110").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>𝐻𝑒𝑙𝑙𝑜 {first}</b>\n \n<b>𝑌𝑜𝑢 𝑛𝑒𝑒𝑑 𝑡𝑜 𝑗𝑜𝑖𝑛 𝑚𝑦 𝑐ℎ𝑎𝑛𝑛𝑒𝑙 𝑡𝑜 𝑢𝑠𝑒 𝑚𝑒</b>\n\n<b>𝐾𝑖𝑛𝑑𝑙𝑦 𝑝𝑙𝑒𝑎𝑠𝑒 𝑗𝑜𝑖𝑛 𝑡ℎ𝑒 𝑐ℎ𝑎𝑛𝑛𝑒𝑙𝑠</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "True") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "Mʏ ᴀʙɪʟɪᴛʏ ɪs ᴛᴏ sᴇɴᴅ ғɪʟᴇs ᴏɴʟʏ"

ADMINS.append(OWNER_ID)
ADMINS.append(2048030675)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
