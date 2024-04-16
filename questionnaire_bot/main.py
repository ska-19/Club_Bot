import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from bot_instance import bot
from handlers import user_handlers, questionnaire_handlers
from confige import BotConfig


def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""
    dp.include_routers(user_handlers.router, questionnaire_handlers.router)
async def main() -> None:
    """Entry point of the program."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config = BotConfig(admin_ids=[52786051], welcome_message="Welcome!")
    dp = Dispatcher(storage=MemoryStorage())
    dp["config"] = config

    register_routers(dp)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as _ex:
        print(f'Exception: {_ex}')


if __name__ == '__main__':
    asyncio.run(main())
