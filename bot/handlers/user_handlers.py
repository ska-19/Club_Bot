from aiogram.filters import Command
from aiogram import Router, types
from aiogram import F

from bot.config import BotConfig
from bot.keyboards.user_keyboards import get_main_kb, get_main_ikb, get_calc_ikb

user_router = Router()
user_data = {}

async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_calc_ikb()
    )

@user_router.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_calc_ikb())

@user_router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()

@user_router.message(Command("reply"))
async def cmd_reply(message: types.Message):
    """The function replies to your message"""

    await message.reply('Reply message replies! 😻', reply_markup = get_main_ikb())


@user_router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """The function answers dice to your message"""

    await message.answer_dice(emoji="🎲")


@user_router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer(text = "You are an admin.")
    else:
        await message.answer("You are not an admin.")


@user_router.message(Command("start"))
async def cmd_start(message: types.Message, config: BotConfig):
    await message.answer(text = config.welcome_message, reply_markup = get_main_kb())
