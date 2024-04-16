from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_ikb() -> InlineKeyboardMarkup:
    """Get main keyboard."""
    ikb = [
        [InlineKeyboardButton(text="Информация о клубе", callback_data="club_info")],
        [InlineKeyboardButton(text="Профиль", callback_data="user_profile")],
        [InlineKeyboardButton(text="Мероприятия", callback_data="events")],
        [InlineKeyboardButton(text="Обратная связь", callback_data="feedback")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard