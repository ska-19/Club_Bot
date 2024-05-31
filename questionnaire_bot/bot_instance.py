from aiogram import Bot
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv


load_dotenv('../.env')
token = os.getenv('TOKEN_API_RC')
SQL_URL_RC = (f'postgresql+asyncpg://{os.getenv("DB_USER_RC")}:{os.getenv("DB_PASS_RC")}'
              f'@{os.getenv("DB_HOST_RC")}:{os.getenv("DB_PORT_RC")}/{os.getenv("DB_NAME_RC")}')

bot = Bot(
    token=token,
    parse_mode=ParseMode.HTML
)

