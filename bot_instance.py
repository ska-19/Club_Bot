from aiogram import Bot, types
import os
from dotenv import load_dotenv

load_dotenv('.env')
token = os.getenv('TOKEN_API')

bot = Bot(
    token=token,
    parse_mode="HTML"
)