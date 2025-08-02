from os import environ

LOG_FILENAME = environ.get("TDIC_LOG_PATH", "TDictionary.log")
DATABASE_URL = environ["TDIC_DATABASE_URL"]
TELEGRAM_BOT_TOKEN = environ["TDIC_TELEGRAM_BOT_TOKEN"]
