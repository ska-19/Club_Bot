from aiogram import types, Dispatcher

from bot.keyboards.user_keyboards import get_main_keyboard
async def start_handler(msg: types.Message) -> None:
    reply_text = f'Hello {msg.from_user.first_name}!'
    await msg.answer(text=reply_text, reply_markup=get_main_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    """Register user handlers."""
    dp.register_message_handler(start_handler, commands=['start'])