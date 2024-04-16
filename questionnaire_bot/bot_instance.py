from aiogram import Bot, types
import os
from dotenv import load_dotenv
from aiogram.enums import ParseMode

load_dotenv('.env')
token = os.getenv('TOKEN_API')

bot = Bot(
    token=token,
    parse_mode=ParseMode.HTML
)