from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo

def get_main_ikb(tg_id: int = 0) -> InlineKeyboardMarkup:
    """Get main keyboard."""
    web_app = WebAppInfo(url=f'https://club-bot.onrender.com/pages/profile_user/{tg_id}')
    ikb = [
        [InlineKeyboardButton(text='ЗАПУСТИТЬ', web_app=web_app)],
        [InlineKeyboardButton(text='Создать клуб', callback_data='create_club')],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard

def get_back_button() -> InlineKeyboardMarkup:
    """Get back button."""
    ikb = [
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard
