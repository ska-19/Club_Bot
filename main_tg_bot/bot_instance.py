from aiogram import Bot
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv


load_dotenv('../.env')
token = os.getenv('TOKEN_API')
SQL_URL = (f'postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}'
           f'@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
URL = os.getenv('URL')

bot = Bot(
    token=token,
    parse_mode=ParseMode.HTML
)
