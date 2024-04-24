from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from keyboards.user_keyboards import get_main_kb

from confige import BotConfig

import io
from sqlalchemy import select
from database.models import Questionnaire, async_session
from aiogram.types import BufferedInputFile
import pandas as pd

router = Router()


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")
    await message.delete()


@router.message(CommandStart())
async def cmd_start(message: types.Message, config: BotConfig, state: FSMContext):
    is_admin = False
    if message.from_user.id in config.admin_ids:
        is_admin = True
    await message.answer(
        text="👋🏻 <b>Привет! Я бот-анкета, собирающий данные для исследования.</b> \n\n"
             "В анкете всего 12 простых простых вопросов, время прохождения ~2 минуты. \n\n"
             "Давайте начнем! 👉🏻/quest",
        reply_markup=get_main_kb(is_admin)
    )
    await state.clear()


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


# help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        text="📍 Доступные команды: \n"
             "/start - начало работы с ботом \n"
             "/quest - начать анкетирование \n"
             "/info - подробности \n"
             "/dice - кинуть кубик 🎲 \n"
             "/help - помощь \n"
    )
    await message.delete()


@router.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(
        text="👾 Бот-анкета, собирающий данные для умного старшего брата. \n\n"
             "Для прохождения анкеты нажмите /quest\n\n"
             "Бот-анкета ничего не делает кроме сбора данных.\n"
             "Отправляя данные вы соглашаетесь на их сохранение и обработку.\n"
             "Для связи с админом используйте \n/feedback"
    )
    await message.delete()


@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message):
    await message.answer(
        text="🤫 Для связи с администратором напишите пользователю: @yep_admin"
    )
    await message.delete()
