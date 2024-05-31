from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Router, types

from keyboards.user_keyboards import get_main_ikb
from confige import BotConfig
from database import request as rq

router = Router()


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")
    await message.delete()


@router.message(CommandStart())
async def cmd_start(message: types.Message, config: BotConfig, state: FSMContext):
    user_data = {
        "tg_id": message.from_user.id,
        "username": message.from_user.username,
        "name": message.from_user.first_name,
        "surname": message.from_user.last_name
    }
    await message.answer(
        text=config.welcome_message,
    )
    await rq.set_user(user_data)
    is_admin = (await rq.is_user_club_admin(message.from_user.id) == -1)
    await message.answer(
        text='Готово!\n'
             'Вы можете посмотреть свой профиль по кнопке ниже',
        reply_markup=get_main_ikb(user_data, is_admin)
    )
    await state.clear()


@router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer(text="You are an admin.")
    else:
        await message.answer("You are not an admin.")

    await message.delete()

# help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        text="📍 Доступные команды: \n"
             "/dice - кинуть кубик 🎲 \n"
             "/info - подробности \n"
             "/help - помощь \n"
             "/start - начало работы с ботом, также перезапишет ваше имя и фамилию в случае изменения,"
             " без потери данных \n"
        )
    await message.delete()


@router.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(
        text="👾Бот находится на стадии активной разработки!\n"
             "Отправляя данные вы соглашаетесь на их сохранение и обработку.\n"
             "Для связи с админом используйте \n/feedback"
    )
    await message.delete()


@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message):
    await message.answer(
        text="Для связи с администратором напишите пользователю: @yep_admin"
    )
    await message.delete()
