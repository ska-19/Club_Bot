from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Get main command keyboard."""
    kb = [
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/quest")],
        [KeyboardButton(text="/dice")],
    ]
    if is_admin:
        kb.append([KeyboardButton(text="/admin_exp_csv")])
        kb.append([KeyboardButton(text="/admin_exp_xlsx")])

    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    return keyboard


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

def get_back_button() -> InlineKeyboardMarkup:
    """Get back button."""
    ikb = [
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard
