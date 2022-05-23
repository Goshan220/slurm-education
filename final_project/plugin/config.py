import logging
from os import getenv

BACKEND = "Telegram" if getenv("ENVIRONMENT") == "production" else "Text"

BOT_IDENTITY = {
    "token": "token is here",
}
BOT_ADMINS = ("75051276",) if getenv("ENVIRONMENT") == "production" else ("@CHANGE_ME",)

BOT_DATA_DIR = r'I:\slerm\pool-tracker\plugin\data'
BOT_EXTRA_PLUGIN_DIR = r'I:\slerm\pool-tracker\plugin\plugins'

BOT_LOG_FILE = r'I:\slerm\pool-tracker\plugin\errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_PREFIX = "/" if getenv("ENVIRONMENT") == "production" else "!"
BOT_ALT_PREFIXES = ("Bot", "Бот", "bot", "бот")
BOT_ALT_PREFIXES_SEPARATORS = (":", ",", ":")
