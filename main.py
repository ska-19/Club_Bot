import asyncio
import os
# import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from bot.handlers.user_handlers import register_user_handlers

def register_handlers(dp: Dispatcher) -> None:
    """Register handlers."""
    register_user_handlers(dp)
async def main() -> None:
    """Entry point of the program."""
    load_dotenv('.env')

    token = os.getenv('TOKEN_API')
    bot = Bot(token)
    dp = Dispatcher(bot)

    register_handlers(dp)

    try:
        await dp.start_polling()
    except Exception as _ex:
        print(f'Exception: {_ex}')


if __name__ == '__main__':
    asyncio.run(main())
