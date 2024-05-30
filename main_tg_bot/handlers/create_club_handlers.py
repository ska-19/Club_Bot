from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards.simple_kb import make_colum_keyboard
from keyboards.user_keyboards import get_main_ikb, get_back_button

from database import request as rq

router = Router()


class CreateClub(StatesGroup):
    enter_name = State()
    enter_dest = State()
    enter_bio = State()
    enter_link_channel = State()


@router.callback_query(F.data == "create_club")
async def cmd_create(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="🎩 <b>Давайте создадим клуб</b>\n\n"
             "Для начала укажите название клуба:",
        reply_markup=get_back_button()
    )
    await state.set_state(CreateClub.enter_name)
    await callback.message.delete()


@router.message(CreateClub.enter_name)
async def cmd_enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text="2️⃣Теперь укажите направление клуба в одно-два слова\n"
             "например: 'финансы', 'программирование', 'танцы', 'спорт'",
        reply_markup=get_back_button()
    )
    await state.set_state(CreateClub.enter_dest)
    await message.delete()


@router.message(CreateClub.enter_dest)
async def cmd_enter_dest(message: Message, state: FSMContext):
    await state.update_data(dest=message.text)
    await message.answer(
        text="3️⃣Теперь укажите краткое описание клуба в одно-два предложения",
        reply_markup=get_back_button()
    )
    await state.set_state(CreateClub.enter_bio)
    await message.delete()


@router.message(CreateClub.enter_bio)
async def cmd_enter_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.answer(
        text="4️⃣Теперь укажите ссылку на канал клуба\n\n"
             "Если у вас нет канала, можете указать ссылку на ваш профиль в соц. сети",
        reply_markup=get_back_button()
    )
    await state.set_state(CreateClub.enter_link_channel)
    await message.delete()


@router.message(CreateClub.enter_link_channel)
async def cmd_enter_link_channel(message: Message, state: FSMContext):
    await state.update_data(channel_link=message.text)
    club_data = await state.get_data()
    await rq.set_club(message.from_user.id, club_data)
    await message.answer(
        text="🎉 <b>Клуб успешно создан!</b>\n\n"
             f"Название: {club_data['name']}\n"
             f"Направление: {club_data['dest']}\n"
             f"Описание: {club_data['bio']}\n"
             f"Ссылка на канал: {club_data['channel_link']}\n\n"
             "Для управления клубом используйте кнопки в профиле клуба.",
        reply_markup=get_main_ikb({'tg_id': message.from_user.id}, is_admin=True)
    )
    await state.clear()
    await message.delete()


@router.callback_query(F.data == "back")
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    is_admin = await rq.is_user_club_admin(callback.message.from_user.id)
    await callback.message.answer(
        text="<b>Вы прервали создание клуба</b>",
        reply_markup=get_main_ikb({'tg_id': callback.from_user.id}, is_admin=False)
    )
    await state.clear()

