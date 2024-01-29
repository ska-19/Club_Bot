import asyncio
import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from bot_instance import bot
from bot.handlers.user_handlers import user_router


def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""

    dp.include_router(user_router)
async def main() -> None:
    """Entry point of the program."""

    dp = Dispatcher()

    register_routers(dp)

    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f'Exception: {_ex}')


if __name__ == '__main__':
    asyncio.run(main())
