from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb() -> ReplyKeyboardMarkup:
    """Get main command keyboard."""
    kb = [
        [KeyboardButton(text="/user_menu")],
        [KeyboardButton(text="/reply")],
        [KeyboardButton(text="/dice")],
        [KeyboardButton(text="/numbers")],
        [KeyboardButton(text="/admin_info")],
    ]
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


def get_club_info() -> InlineKeyboardMarkup:
    """Get club_info keyboard."""
    ikb = [
        [InlineKeyboardButton(text="Наша команда", callback_data="club_info_team")],
        [InlineKeyboardButton(text="Наши спикеры", callback_data="club_info_speakers")],
        [InlineKeyboardButton(text="Наши партнеры", callback_data="club_info_partners")],
        [InlineKeyboardButton(text="Наши ценности", callback_data="club_info_values")],
        [InlineKeyboardButton(text="История клуба", callback_data="club_info_history")],
        [InlineKeyboardButton(text="Назад", callback_data="club_info_back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard


def get_user_profile_ikb() -> InlineKeyboardMarkup:
    """Get user_profile keyboard."""
    ikb = [
        [InlineKeyboardButton(text="Получить Coins", callback_data="user_profile_change_coins")],
        [InlineKeyboardButton(text="Редактировать", callback_data="user_profile_change")],
        [InlineKeyboardButton(text="Пригласить друга", callback_data="user_profile_invite")],
        [InlineKeyboardButton(text="Назад", callback_data="user_profile_back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard


def get_events_ikb() -> InlineKeyboardMarkup:
    """Get events keyboard."""
    ikb = [
        [InlineKeyboardButton(text="Ближайшие мероприятия", callback_data="events_upcoming")],
        [InlineKeyboardButton(text="Прошедшие мероприятия", callback_data="events_past")],
        [InlineKeyboardButton(text="Подписаться", callback_data="events_subscribe")],
        [InlineKeyboardButton(text="Назад", callback_data="events_back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard

def get_feedback_ikb() -> InlineKeyboardMarkup:
    """Get feedback keyboard."""
    ikb = [
        [InlineKeyboardButton(text="Предложить идею", callback_data="feedback_idea")],
        [InlineKeyboardButton(text="Сообщить о проблеме", callback_data="feedback_problem")],
        [InlineKeyboardButton(text="Пожаловаться", callback_data="feedback_complaint")],
        [InlineKeyboardButton(text="Назад", callback_data="feedback_back")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard

def get_calc_ikb() -> InlineKeyboardMarkup:
    """Get calc keyboard."""
    ikb = [
        [
            InlineKeyboardButton(text="-1", callback_data="num_decr"),
            InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard
