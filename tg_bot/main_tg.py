import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tg_bot.bot_instance import bot
from tg_bot.bot.handlers import user_handlers
from tg_bot.bot.handlers import user_registration

from tg_bot.bot.config import BotConfig

def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""

    dp.include_routers(user_handlers.router, user_registration.router)
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
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f'Exception: {_ex}')


if __name__ == '__main__':
    asyncio.run(main())
