import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("token")
TOKEN_PAYMASTER = os.getenv("paymaster_token")
TOKEN_SBER = os.getenv("sber_token")

CURRENCY_API_KEY = os.getenv("currency_api_key")

POSTGRES_HOST = os.getenv("pg_host")
POSTGRES_PORT = os.getenv("pg_port", default=5432)
POSTGRES_USER = os.getenv("pg_user")
POSTGRES_PASSWORD = os.getenv("pg_password")
POSTGRES_DB = os.getenv("pg_db")
POSTGRES_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST = os.getenv("redis_host")
REDIS_PORT = os.getenv("redis_port", default=6379)
REDIS_DB = os.getenv("redis_db")

ADMINS = [
    1473001288,
]
LG_EXTERIORS = {
    "fn": "Factory New",
    "mw": "Minimal Wear",
    "ft": "Field-Tested",
    "ww": "Well-Worn",
    "bs": "Battle-Scarred",
}
SH_EXTERIORS = {
    "Factory New": "fn",
    "Minimal Wear": "mw",
    "Field-Tested": "ft",
    "Well-Worn": "ww",
    "Battle-Scarred": "bs",
}

BACK_BTN = "↩️ Back"
BUY_BTN = "🛒 Buy"
LEFT_BTN = "⬅️"  # ❮
RIGHT_BTN = "➡️"  # ❯
SBER_ICON = "💳 Sber"
PAYMASTER_ICON = "💰 Paymaster"
