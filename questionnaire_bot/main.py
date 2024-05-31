import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from bot_instance import bot
from handlers import user_handlers, questionnaire_handlers, rc_handlers
from confige import BotConfig

from database.models import async_main
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from matching import ask_for_take_part, suggest_new_meeting, remind_about_meeting


def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""
    dp.include_routers(user_handlers.router, questionnaire_handlers.router, rc_handlers.router)


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
