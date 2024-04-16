from aiogram.filters import Command
from aiogram import Router, types
from aiogram import F

from keyboards.user_keyboards import get_main_kb, get_main_ikb
from confige import BotConfig


router = Router()


@router.message(Command("user_menu"))
async def cmd_user_menu(message: types.Message):
    await message.answer("User menu", reply_markup=get_main_ikb())

    await message.delete()


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """The function answers dice to your message"""

    await message.answer_dice(emoji="🎲")

    await message.delete()


@router.message(Command("start"))
async def cmd_start(message: types.Message, config: BotConfig):
    await message.answer(text=config.welcome_message, reply_markup=get_main_kb())


# @router.message(Command("admin_info"))
# async def cmd_admin_info(message: types.Message, config: BotConfig):
#     if message.from_user.id in config.admin_ids:
#         await message.answer(text = "You are an admin.")
#     else:
#         await message.answer("You are not an admin.")
#
#     await message.delete()
