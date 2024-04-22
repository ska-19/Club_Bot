from aiogram.filters import Command, CommandStart
from aiogram import Router, types
from aiogram import F

from keyboards.user_keyboards import get_main_kb, get_main_ikb
from confige import BotConfig

#config
from confige import BotConfig

import io
from sqlalchemy import select
from database.models import Questionnaire, async_session
from aiogram.types import BufferedInputFile
import pandas as pd

router = Router()

@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """The function answers dice to your message"""

    await message.answer_dice(emoji="🎲")

    await message.delete()


@router.message(CommandStart())
async def cmd_start(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        is_admin = True
    await message.answer(
        text="<b>Привет! Я бот-анкета, собирающий данные для умного старшего брата.</b> \n\n Давай начнем!",
        reply_markup=get_main_kb(is_admin)
    )


@router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer(text="You are an admin.")
    else:
        await message.answer("You are not an admin.")

    await message.delete()



@router.message(Command("admin_exp_csv"))
async def cmd_admin_export_db(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        try:
            async with async_session() as session:
                query = select(Questionnaire)
                result = await session.execute(query)
                data = result.scalars().all()
                data = [q.__dict__ for q in data[1:]]
                df = pd.DataFrame(data)

            with io.BytesIO() as temp_buffer:
                df.to_csv(temp_buffer, index=False)
                temp_buffer.seek(0)
                await message.answer_document(
                    BufferedInputFile(temp_buffer.getvalue(), filename='data.csv'))
        except Exception as e:
            print("Error accessing file:", e)
    else:
        await message.answer("You are not an admin.")

    await message.delete()


@router.message(Command("admin_exp_xlsx"))
async def cmd_admin_export_db(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        try:
            async with async_session() as session:
                query = select(Questionnaire)
                result = await session.execute(query)
                data = result.scalars().all()
                data = [q.__dict__ for q in data[1:]]
                df = pd.DataFrame(data)

            with io.BytesIO() as temp_buffer:  # Change this to StringIO
                df.to_excel(temp_buffer, index=False)
                temp_buffer.seek(0)
                await message.answer_document(
                    BufferedInputFile(temp_buffer.getvalue(), filename='data.xlsx'))
        except Exception as e:
            print("Error accessing file:", e)
    else:
        await message.answer("You are not an admin.")

    await message.delete()
