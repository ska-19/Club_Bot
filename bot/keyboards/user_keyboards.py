from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Get main keyboard."""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Button_1', callback_data='callback_button_1')],
    ])
    return ikb
