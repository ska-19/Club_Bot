from aiogram import Bot, Dispatcher
import asyncio

import handlers

bot = Bot(token='')

def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""
    dp.include_routers(handlers.router)

async def main():
    dp = Dispatcher()
    register_routers(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')
