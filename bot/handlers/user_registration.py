from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bot.keyboards.simple_kb import make_row_keyboard, make_colum_keyboard

router = Router()


available_prof_status = ["Новичок", "Продолжающий", "Профессионал"]
available_achievements_status = ["🔔Включить", "🔕Выключить"]


class OrderFood(StatesGroup):
    choosing_prof_status = State()
    choosing_achievements_status = State()


@router.message(StateFilter(None), Command("reg"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Вы когда-нибудь состояли в клубах по интересам?\n <b>Выберете свой статус:</b>",
        reply_markup=make_colum_keyboard(available_prof_status)
    )
    await state.set_state(OrderFood.choosing_prof_status)


@router.message(OrderFood.choosing_prof_status, F.text.in_(available_prof_status))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_status=message.text.lower())
    await message.answer(
        text="Хотите ли вы получать уведомления о мероприятиях от других клубов?",
        reply_markup=make_colum_keyboard(available_achievements_status)
    )
    await state.set_state(OrderFood.choosing_achievements_status)


@router.message(StateFilter("OrderFood:choosing_prof_status"))
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не понимаю такого ответа.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_colum_keyboard(available_prof_status)
    )


@router.message(OrderFood.choosing_achievements_status, F.text.in_(available_achievements_status))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы {user_data['chosen_status']} в клубном деле.\n Уведомления: {message.text.lower()[:-2]}ны.\n",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(OrderFood.choosing_achievements_status)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не понимаю такого ответа!\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_achievements_status)
    )
