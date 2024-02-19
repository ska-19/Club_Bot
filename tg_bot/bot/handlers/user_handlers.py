from aiogram.filters import Command
from aiogram import Router, types
from aiogram import F

from tg_bot.bot.config import BotConfig
from tg_bot.bot.keyboards.user_keyboards import get_main_kb, get_main_ikb, get_calc_ikb, get_user_profile_ikb, get_club_info

router = Router()
user_data = {}

async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_calc_ikb()
    )

async def back_to_main_menu(message: types.Message):
    await message.edit_text("User menu", reply_markup = get_main_ikb())


@router.message(Command("user_menu"))
async def cmd_user_menu(message: types.Message):
    await message.answer("User menu", reply_markup = get_main_ikb())

    await message.delete()

@router.callback_query(F.data == "user_profile")
async def callback_user_profile(callback: types.CallbackQuery):
    await callback.message.edit_text("User profile", reply_markup = get_user_profile_ikb())

    await callback.answer()

@router.callback_query(F.data.startswith("user_profile_"))
async def callbacks_user_profile(callback: types.CallbackQuery):
    action = callback.data.split("_")[-1]
    if action == "coins":
        await callback.message.edit_text("Coins")
    elif action == "change":
        await callback.message.edit_text("Редактирование")
    elif action == "invite":
        await callback.message.edit_text("Пригласить")
    elif action == "back":
        await back_to_main_menu(callback.message)

    await callback.answer()

@router.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_calc_ikb())

@router.callback_query(F.data.startswith("num_"))
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


@router.callback_query(F.data =="club_info")
async def callback_club_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Информация о клубе", reply_markup=get_club_info())

    await callback.answer()

@router.callback_query(F.data.startswith("club_info_"))
async def callbacks_club_info(callback: types.CallbackQuery):
    action = callback.data.split("_")[-1]
    if action == "team":
        await callback.message.edit_text("Команда")
    elif action == "speakers":
        await callback.message.edit_text("Спикеры")
    elif action == "partners":
        await callback.message.edit_text("Партнеры")
    elif action == "values":
        await callback.message.edit_text("Ценности")
    elif action == "history":
        await callback.message.edit_text("История клуба")
    elif action == "back":
        await back_to_main_menu(callback.message)

    await callback.answer()


@router.message(Command("reply"))
async def cmd_reply(message: types.Message):
    """The function replies to your message"""

    await message.reply('Reply message replies! 😻', reply_markup = get_main_ikb())


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """The function answers dice to your message"""

    await message.answer_dice(emoji="🎲")

    await message.delete()


@router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer(text = "You are an admin.")
    else:
        await message.answer("You are not an admin.")

    await message.delete()

@router.message(Command("start"))
async def cmd_start(message: types.Message, config: BotConfig):
    await message.answer(text = config.welcome_message, reply_markup = get_main_kb())
