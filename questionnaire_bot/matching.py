import asyncio
import os
import io
from database.models import Questionnaire, async_session
from aiogram.types import BufferedInputFile
from sqlalchemy import select

from bot_instance import bot
from database import requests as rq
from keyboards.user_keyboards import get_main_ikb, get_ask_for_take_part_ikb, get_ask_for_meeting_ikb
from handlers.rc_handlers import users_rc_ready, user_rc_pair, take_part_state

import pandas as pd

async def ask_for_take_part():
    users_rc_ready.clear()
    user_rc_pair.clear()
    users_tg_id = await rq.get_users()
    take_part_state.set_state(True)
    for user_tg_id in users_tg_id:
        await bot.send_message(user_tg_id, text="Хотите завести новое знакомство на неделе? \n",
                               reply_markup=get_ask_for_take_part_ikb())


async def suggest_new_meeting(ml: bool = False):
    take_part_state.set_state(False)
    if ml:

        df = pd.DataFrame()
        active_users = []
        for user_tg_id, ready in users_rc_ready.items():
            if ready:
                active_users.append(user_tg_id)
        try:
            async with async_session() as session:
                query = select(Questionnaire).where(Questionnaire.tg_id.in_(active_users))
                result = await session.execute(query)
                data = result.scalars().all()
                data = [q.__dict__ for q in data[1:]]
                df = pd.DataFrame(data)
        except Exception as e:
            print("Error accessing file:", e)
        with io.BytesIO() as temp_buffer:
            df.to_csv(temp_buffer, index=False)
            temp_buffer.seek(0)
            await bot.send_document(52786051,
                                    document=BufferedInputFile(temp_buffer.getvalue(),
                                                               filename='data.csv'))


    pair = None
    for user_tg_id, ready in users_rc_ready.items():
        if ready:
            if pair is None:
                pair = user_tg_id
            else:
                user_rc_pair[user_tg_id] = pair
                user_rc_pair[pair] = user_tg_id
                pair = None

        if pair is not None:
            await bot.send_message(pair, text="К сожалению, на этой неделе не удалось найти вам пару :с")
            users_rc_ready[pair] = False

    for user_tg_id in user_rc_pair.keys():
        week_pair_id = user_rc_pair[user_tg_id]
        user_quest_data = await rq.get_user(week_pair_id)
        user_tg_data = await bot.get_chat(week_pair_id)
        await bot.send_message(user_tg_id, text=f"Ваша пара на неделю: {user_tg_data.first_name}\n"
                                                f"Напишите @{user_tg_data.username} в личные сообщения"
                                                f" и договоритесь о встрече!")


async def remind_about_meeting():
    for user_tg_id, ready in users_rc_ready.items():
        if ready:
            await bot.send_message(user_tg_id, text=f"Вы уже встретились с вашей парой на этой неделе?",
                                   reply_markup=get_ask_for_meeting_ikb())
