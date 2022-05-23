import logging
from os import getenv

BACKEND = "Telegram" if getenv("ENVIRONMENT") == "production" else "Text"

BOT_IDENTITY = {
    "token": "my_token",
}
BOT_ADMINS = ("My_id",) if getenv("ENVIRONMENT") == "production" else ("@CHANGE_ME",)

BOT_DATA_DIR = r"I:\slerm\pythonforops\10.chatops_errbot\cource_work\data"
BOT_EXTRA_PLUGIN_DIR = r"I:\slerm\pythonforops\10.chatops_errbot\cource_work\plugins"
BOT_LOG_FILE = r"I:\slerm\pythonforops\10.chatops_errbot\cource_work\errbot.log"
BOT_EXTRA_STORAGE_PLUGINS_DIR = r"I:\slerm\pythonforops\10.chatops_errbot\cource_work\err-storage-redis"

STORAGE = "Redis"
STORAGE_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}

BOT_LOG_LEVEL = logging.DEBUG

BOT_PREFIX = "/" if getenv("ENVIRONMENT") == "production" else "!"
BOT_ALT_PREFIXES = ("Bot", "Бот", "bot", "бот", "Вопрос", "вопрос")
BOT_ALT_PREFIXES_SEPARATORS = (":", ",", ":")
