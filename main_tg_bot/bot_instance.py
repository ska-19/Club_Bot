from aiogram import Bot, types
import os
from dotenv import load_dotenv
from aiogram.enums import ParseMode
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv


load_dotenv('../.env')
token = os.getenv('TOKEN_API')
SQL_URL = f'postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
URL = os.getenv('URL')

bot = Bot(
    token=token,
    parse_mode=ParseMode.HTML
)

