from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb() -> ReplyKeyboardMarkup:
    """Get main keyboard."""
    kb = [
        [KeyboardButton(text="/reply")],
        [KeyboardButton(text="/dice")],
        [KeyboardButton(text="/numbers")],
        [KeyboardButton(text="/admin_info")],
        [KeyboardButton(text="/start")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    return keyboard


def get_main_ikb() -> InlineKeyboardMarkup:
    """Get main keyboard."""
    ikb = [
        [
            InlineKeyboardButton(text="X", callback_data="c"),
            InlineKeyboardButton(text="Y", callback_data="cc")
        ],
        [InlineKeyboardButton(text="Z", callback_data="ccc")]
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard

def get_calc_ikb() -> InlineKeyboardMarkup:
    """Get main keyboard."""
    ikb = [
        [
            InlineKeyboardButton(text="-1", callback_data="num_decr"),
            InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard