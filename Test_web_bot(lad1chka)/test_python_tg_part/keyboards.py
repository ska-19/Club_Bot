from aiogram.types import WebAppInfo, ReplyKeyboardMarkup
from aiogram import types


web_app = WebAppInfo(url='https://lad1chka.github.io/')

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Site', web_app=web_app)]
    ],
    resize_keyboard=True
)