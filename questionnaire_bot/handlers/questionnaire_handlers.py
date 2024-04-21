from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_kb import make_colum_keyboard
from keyboards.user_keyboards import get_main_kb

router = Router()

available_knew_interest_clubs = ["Ни когда не слышал", "Слышал, но не состоял", "Состоял/Состою"]
available_readiness_new_meetings = ["Да!", "Зависит от настроения", "Не люблю знакомиться с новыми людьми"]
available_expectations = ["100% фана", "75% фана, немного серьезности", "50% фана, 50% серьезности",
                          "25% фана, 75% серьезности", "0% фана, только деловые беседы"]
available_meeting_format = ["Готов очно", "Только дистанционно"]
available_hobbies = ["Ведение соцсетей и блогов", "Путешествия", "Музыка", "Книги", "Кино и сериалы", "Видеоигры",
                     "Игра на музыкальных инструментах", "Кулинария", "Искусство и рукоделие", "Коллекционирование",
                     "Техника и автомобили", "Среди этих нет моих хобби"]
available_stay_in_touch = ["Да", "Нет"]


class HobbiesQuest(StatesGroup):
    choosing_knew_interest_clubs = State()
    choosing_readiness_new_meetings = State()
    choosing_expectations = State()
    choosing_meeting_format = State()
    choosing_hobbies = State()
    tell_hobbies = State()
    tell_expectations = State()
    invite_friends = State()
    choosing_stay_in_touch = State()


async def send_error_message(message: Message, keyboard_options: list[str],
                             error_text: str = "Я не понимаю такого ответа.\n\nПожалуйста, выберите один из вариантов "
                                               "из списка ниже:"):
    await message.answer(
        text=error_text,
        reply_markup=make_colum_keyboard(keyboard_options)
    )


@router.message(StateFilter(None), Command("quest"))
async def cmd_quest(message: Message, state: FSMContext):
    await message.answer(
        text="Вы когда-нибудь слышали о клубах по интересам?\n <b>Выберете один из вариантов:</b>",
        reply_markup=make_colum_keyboard(available_knew_interest_clubs)
    )
    await state.set_state(HobbiesQuest.choosing_knew_interest_clubs)


@router.message(HobbiesQuest.choosing_knew_interest_clubs, F.text.in_(available_knew_interest_clubs))
async def quest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_knew_interest_clubs=message.text.lower())
    await message.answer(
        text="Готовы ли вы к новым знакомствам?",
        reply_markup=make_colum_keyboard(available_readiness_new_meetings)
    )
    await state.set_state(HobbiesQuest.choosing_readiness_new_meetings)


@router.message(StateFilter("HobbiesQuest:choosing_knew_interest_clubs"))
async def quest_chosen_incorrectly_clubs(message: Message):
    await send_error_message(message, available_knew_interest_clubs)


@router.message(HobbiesQuest.choosing_readiness_new_meetings, F.text.in_(available_readiness_new_meetings))
async def quest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_readiness_new_meetings=message.text.lower())
    await message.answer(
        text="Какие у вас ожидания от клуба?",
        reply_markup=make_colum_keyboard(available_expectations)
    )
    await state.set_state(HobbiesQuest.choosing_expectations)


@router.message(StateFilter("HobbiesQuest:choosing_readiness_new_meetings"))
async def quest_chosen_incorrectly_readiness(message: Message):
    await send_error_message(message, available_readiness_new_meetings)


@router.message(HobbiesQuest.choosing_expectations, F.text.in_(available_expectations))
async def quest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_expectations=message.text.lower())
    await message.answer(
        text="Как вы предпочитаете встречи?",
        reply_markup=make_colum_keyboard(available_meeting_format)
    )
    await state.set_state(HobbiesQuest.choosing_meeting_format)


@router.message(StateFilter("HobbiesQuest:choosing_expectations"))
async def quest_chosen_incorrectly_expectations(message: Message):
    await send_error_message(message, available_expectations)


@router.message(HobbiesQuest.choosing_meeting_format, F.text.in_(available_meeting_format))
async def quest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_meeting_format=message.text.lower())
    await message.answer(
        text="Выберите ваши хобби",
        reply_markup=make_colum_keyboard(available_hobbies)
    )
    await state.set_state(HobbiesQuest.choosing_hobbies)


@router.message(StateFilter("HobbiesQuest:choosing_meeting_format"))
async def quest_chosen_incorrectly_format(message: Message):
    await send_error_message(message, available_meeting_format)


@router.message(HobbiesQuest.choosing_hobbies, F.text.in_(available_hobbies))
async def quest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_hobbies=message.text.lower())
    await message.answer(
        text="Какие у вас хобби?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(HobbiesQuest.tell_hobbies)


@router.message(StateFilter("HobbiesQuest:choosing_hobbies"))
async def quest_chosen_incorrectly_hobbies(message: Message):
    await send_error_message(message, available_hobbies)


@router.message(HobbiesQuest.tell_hobbies, lambda message: len(message.text) > 5)
async def tell_hobbies(message: Message, state: FSMContext):
    await state.update_data(tell_hobbies=message.text.lower())
    await message.answer(
        text="Какие у вас ожидания от клуба?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(HobbiesQuest.tell_expectations)


@router.message(StateFilter("HobbiesQuest:tell_hobbies"))
async def quest_tell_hobbies_incorrectly(message: Message):
    await message.answer(
        text="Пожалуйста, опишите ваши хобби, немного подробней!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(HobbiesQuest.tell_expectations, lambda message: len(message.text) > 5)
async def invite_friends(message: Message, state: FSMContext):
    await state.update_data(tell_expectations=message.text.lower())
    await message.answer(
        text="Вы хотите остаться с нами на связи?",
        reply_markup=make_colum_keyboard(available_stay_in_touch)
    )
    await state.set_state(HobbiesQuest.choosing_stay_in_touch)


@router.message(StateFilter("HobbiesQuest:tell_expectations"))
async def quest_tell_expectations_incorrectly(message: Message):
    await message.answer(
        text="Пожалуйста, опишите ваши ожидания от клуба, немного подробней!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(HobbiesQuest.choosing_stay_in_touch, F.text.in_(available_stay_in_touch))
async def quest_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_stay_in_touch=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы {user_data['chosen_knew_interest_clubs']} о клубах по интересам.\n"
             f"Готовы к новым знакомствам: {user_data['chosen_readiness_new_meetings']}.\n"
             f"Ожидания от клуба: {user_data['chosen_expectations']}.\n"
             f"Предпочтение встреч: {user_data['chosen_meeting_format']}.\n"
             f"Ваши хобби: {user_data['chosen_hobbies']}.\n"
             f"Описание хобби: {user_data['tell_hobbies']}.\n"
             f"Ожидания от клуба: {user_data['tell_expectations']}.\n"
             f"Оставаться на связи: {message.text.lower()}.\n",
        reply_markup=get_main_kb()
    )
    await state.clear()


@router.message(HobbiesQuest.choosing_stay_in_touch)
async def quest_chosen_incorrectly(message: Message):
    await send_error_message(message, available_stay_in_touch)
