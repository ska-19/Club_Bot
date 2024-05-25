from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards.simple_kb import make_colum_keyboard
from keyboards.user_keyboards import get_main_ikb, get_back_button

from database import requests as rq

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
             "Для начала укажите название:",
        reply_markup=get_back_button()
    )
    await rq.set_user(callback.message.from_user.id)
    await state.set_state(CreateClub.enter_name)



@router.message(StateFilter("HobbiesQuest:choosing_hobbies"))
async def quest_chosen_incorrectly_hobbies(message: Message):
    await message.answer(
        text="😭 Я не понимаю такого ответа.\n\nПожалуйста, выберите один из вариантов "
             "из списка:",
    )

@router.message(StateFilter("HobbiesQuest:tell_expectations"))
async def quest_tell_expectations_incorrectly(message: Message):
    await message.answer(
        text="😇 Пожалуйста, опишите ваши ожидания от клуба, немного подробней!",
        reply_markup=ReplyKeyboardRemove()
    )

#
# @router.message(HobbiesQuest.choosing_stay_in_touch, F.text.in_(available_stay_in_touch))
# async def quest_chosen(message: Message, state: FSMContext):
#     # await state.update_data(chosen_stay_in_touch=message.text.lower())
#     chosen_stay_in_touch = message.text.lower()
#     for i in range(len(available_stay_in_touch)):
#         if available_stay_in_touch[i].lower() == chosen_stay_in_touch:
#             await state.update_data(chosen_stay_in_touch=i)
#     user_data = await state.get_data()
#     await message.answer(
#         text="🎉 <b>Вы прошли все вопросы! Спасибо за ответы!</b> ❤️\n\n"
#              "Создателям очень важно собрать как можно больше ответов, чтобы воплотить в жизнь свой замысел!\n\n"
#              "Вы можете помочь нам! Заодно поучаствовать в <b>розыгрыше призов</b>, опросив своего хорошего друга!\n"
#              "Ещё раз нажав на /quest\n\n\n"
#              "p.s. Как вы могли заметить вопросы простые и их не много)\n"
#              "Уверены, что вы знаете увлечения своих друзей "
#              "и сможете заполнить анкету ещё раз, даже если их нет рядом.",
#
#         reply_markup=get_main_kb()
#     )
#     await rq.set_user_tell_questionnaire(message.from_user.id, user_data),
#     await state.clear()


# @router.message(HobbiesQuest.choosing_stay_in_touch)
# async def quest_chosen_incorrectly(message: Message):
#     await send_error_message(message, available_stay_in_touch)
