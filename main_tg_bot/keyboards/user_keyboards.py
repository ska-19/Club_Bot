from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo


def get_main_ikb(user_data: dict = None, is_admin: bool = False) -> InlineKeyboardMarkup:
    """Get main keyboard."""
    tg_id = user_data['tg_id']
    web_app = WebAppInfo(url=f'https://club-bot.onrender.com/pages/profile_user/{tg_id}')
    ikb = [
        [InlineKeyboardButton(text='ЗАПУСТИТЬ', web_app=web_app)],
        [InlineKeyboardButton(text='Создать клуб', callback_data='create_club')] if is_admin else [InlineKeyboardButton(text='Выгрузить данные', callback_data='download_clu_data')],
        [InlineKeyboardButton(text='Случайное знакомство', url='https://t.me/test_1_questionnaire_bot')],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard


def get_back_button() -> InlineKeyboardMarkup:
    """Get back button."""
    ikb = [
        [InlineKeyboardButton(text="Отменить", callback_data="back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard
