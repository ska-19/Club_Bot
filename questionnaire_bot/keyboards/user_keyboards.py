from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Get main command keyboard."""
    kb = [
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


def get_ask_for_take_part_ikb() -> InlineKeyboardMarkup:
    ikb = [
        [InlineKeyboardButton(text="Принять участие", callback_data="take_part")],
        [InlineKeyboardButton(text="Отказаться", callback_data="decline")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard


def get_ask_for_meeting_ikb() -> InlineKeyboardMarkup:
    ikb = [
        [InlineKeyboardButton(text="Уже встретились!", callback_data="meeting_done")],
        [InlineKeyboardButton(text="Познакомились, встретимся позже)", callback_data="meeting_later")],
        [InlineKeyboardButton(text="Собеседник не отвечает :c", callback_data="meeting_notdone")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard
