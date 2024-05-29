import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from bot_instance import bot
from handlers import user_handlers, questionnaire_handlers, rc_handlers
from confige import BotConfig

from database.models import async_main
from database import requests as rq
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from keyboards.user_keyboards import get_main_ikb, get_ask_for_take_part_ikb, get_ask_for_meeting_ikb

from handlers.rc_handlers import users_rc_ready, user_rc_pair, take_part_state


def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""
    dp.include_routers(user_handlers.router, questionnaire_handlers.router, rc_handlers.router)


async def ask_for_take_part():
    users_rc_ready.clear()
    user_rc_pair.clear()
    users_tg_id = await rq.get_users()
    take_part_state.set_state(True)
    for user_tg_id in users_tg_id:
        await bot.send_message(user_tg_id, text="Хотите завести новое знакомство на неделе? \n",
                               reply_markup=get_ask_for_take_part_ikb())


async def suggest_new_meeting():
    take_part_state.set_state(False)
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

    for user_tg_id in users_rc_ready.keys():
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


async def main() -> None:
    """Entry point of the program."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    await async_main()

    config = BotConfig(
        admin_ids=[52786051],
        welcome_message="Привет! Я бот-анкета, собирающий данные для умного старшего брата. \n\n <b>Давай начнем!</b>"
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp["config"] = config

    register_routers(dp)

    scheduler = AsyncIOScheduler()

    # Задания для тестирования каждую минуту
    scheduler.add_job(ask_for_take_part, 'interval', minutes=1, start_date=datetime.now() + timedelta(seconds=5),
                      id='ask_for_take_part')
    scheduler.add_job(suggest_new_meeting, 'interval', minutes=1, start_date=datetime.now() + timedelta(seconds=10),
                      id='suggest_new_meeting')
    scheduler.add_job(remind_about_meeting, 'interval', minutes=1, start_date=datetime.now() + timedelta(seconds=15),
                      id='remind_about_meeting')

    # Задание на каждую среду в 10:00
    # scheduler.add_job(ask_for_feedback, 'cron', day_of_week='wed', hour=10)
    # Задание на каждую субботу в 18:00
    # scheduler.add_job(collect_feedback, 'cron', day_of_week='sat', hour=18)

    try:
        scheduler.start()
        await dp.start_polling(bot, skip_updates=True)
    except Exception as _ex:
        print(f'Exception: {_ex}')


if __name__ == '__main__':
    asyncio.run(main())
