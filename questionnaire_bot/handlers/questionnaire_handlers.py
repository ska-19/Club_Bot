from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_kb import make_colum_keyboard
from keyboards.user_keyboards import get_main_kb

from database import requests as rq

router = Router()

available_knew_interest_clubs = ["Никогда не слышал", "Слышал, но не состоял", "Состоял/Состою"]
available_readiness_new_meetings = ["Да!", "Зависит от настроения", "Не люблю знакомиться с новыми людьми"]
available_expectations = ["100% фана", "75% фана, немного серьезности", "50% фана, 50% серьезности",
                          "25% фана, 75% серьезности", "0% фана, только деловые беседы"]
available_meeting_format = ["Готов вживую", "Только онлайн"]
available_zodiac_signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец",
                          "Козерог", "Водолей", "Рыбы"]
available_personality_type = ["Стратег", "Учёный", "Командир", "Полемист",
                              "Активист", "Посредник", "Тренер", "Борец",
                              "Администратор", "Защитник", "Менеджер", "Консул",
                              "Виртуоз", "Артист", "Делец", "Развлекатель"]
available_gender = ["Мужской", "Женский", "Пропустить"]

available_hobbies = ["Ведение соцсетей и блогов", "Путешествия", "Музыка", "Книги", "Кино и сериалы", "Видеоигры",
                     "Игра на музыкальных инструментах", "Кулинария", "Искусство и рукоделие", "Коллекционирование",
                     "Техника и автомобили"]
available_stay_in_touch = ["Да", "Нет"]


class HobbiesQuest(StatesGroup):
    choosing_knew_interest_clubs = State()
    choosing_readiness_new_meetings = State()
    choosing_expectations = State()
    choosing_meeting_format = State()
    choosing_zodiac_signs = State()
    choosing_personality_type = State()
    choosing_gender = State()
    choosing_hobbies = State()
    tell_hobbies = State()
    tell_what_do_you_do = State()
    tell_expectations = State()
    choosing_stay_in_touch = State()


async def send_error_message(message: Message, keyboard_options: list[str],
                             error_text: str = "😭 Я не понимаю такого ответа.\n\n"
                                               "Пожалуйста, выберите один из вариантов"
                                               "из списка ниже:"):
    await message.reply(
        text=error_text,
        reply_markup=make_colum_keyboard(keyboard_options, [])
    )


@router.message(Command("quest"))
async def cmd_quest(message: Message, state: FSMContext):
    await message.answer(
        text="🎩 <b>Вы когда-нибудь слышали о клубах по интересам?</b>\n\n"
             "Клуб по интересам - это сообщество людей, которые увлечены одной темой и хотят общаться с "
             "единомышленниками.\n\n"
             "Выберете один из вариантов:",
        reply_markup=make_colum_keyboard(available_knew_interest_clubs)
    )
    await rq.set_user(message.from_user.id)
    await state.set_state(HobbiesQuest.choosing_knew_interest_clubs)


@router.message(HobbiesQuest.choosing_knew_interest_clubs, F.text.in_(available_knew_interest_clubs))
async def quest_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_knew_interest_clubs=message.text.lower())
    chosen_knew_interest_clubs = message.text.lower()
    for i in range(len(available_knew_interest_clubs)):
        if available_knew_interest_clubs[i].lower() == chosen_knew_interest_clubs:
            await state.update_data(chosen_knew_interest_clubs=i)
    await message.answer(
        text="🙈 <b>Готовы ли вы к новым знакомствам?</b>",
        reply_markup=make_colum_keyboard(available_readiness_new_meetings)
    )
    await state.set_state(HobbiesQuest.choosing_readiness_new_meetings)


@router.message(StateFilter("HobbiesQuest:choosing_knew_interest_clubs"))
async def quest_chosen_incorrectly_clubs(message: Message):
    await send_error_message(message, available_knew_interest_clubs)


@router.message(HobbiesQuest.choosing_readiness_new_meetings, F.text.in_(available_readiness_new_meetings))
async def quest_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_readiness_new_meetings=message.text.lower())
    chosen_readiness_new_meetings = message.text.lower()
    for i in range(len(available_readiness_new_meetings)):
        if available_readiness_new_meetings[i].lower() == chosen_readiness_new_meetings:
            await state.update_data(chosen_readiness_new_meetings=i)
    await message.answer(
        text="🌟 <b>Какие у вас ожидания от клуба?</b>",
        reply_markup=make_colum_keyboard(available_expectations)
    )
    await state.set_state(HobbiesQuest.choosing_expectations)


@router.message(StateFilter("HobbiesQuest:choosing_readiness_new_meetings"))
async def quest_chosen_incorrectly_readiness(message: Message):
    await send_error_message(message, available_readiness_new_meetings)


@router.message(HobbiesQuest.choosing_expectations, F.text.in_(available_expectations))
async def quest_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_expectations=message.text.lower())
    chosen_expectations = message.text.lower()
    for i in range(len(available_expectations)):
        if available_expectations[i].lower() == chosen_expectations:
            await state.update_data(chosen_expectations=i)
    await message.answer(
        text="👨‍💻 <b>Как предпочитаете встречаться: вживую или онлайн?</b>",
        reply_markup=make_colum_keyboard(available_meeting_format)
    )
    await state.set_state(HobbiesQuest.choosing_meeting_format)


@router.message(StateFilter("HobbiesQuest:choosing_expectations"))
async def quest_chosen_incorrectly_expectations(message: Message):
    await send_error_message(message, available_expectations)


@router.message(HobbiesQuest.choosing_meeting_format, F.text.in_(available_meeting_format))
async def quest_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_meeting_format=message.text.lower())
    chosen_meeting_format = message.text.lower()
    for i in range(len(available_meeting_format)):
        if available_meeting_format[i].lower() == chosen_meeting_format:
            await state.update_data(chosen_meeting_format=i)
            await state.update_data(chosen_hobbies='')
    await message.answer(
        text="🌚 <b>Выберете свой знак зодиака</b>",
        reply_markup=make_colum_keyboard(available_zodiac_signs)
    )
    await state.set_state(HobbiesQuest.choosing_zodiac_signs)


@router.message(StateFilter("HobbiesQuest:choosing_meeting_format"))
async def quest_chosen_incorrectly_format(message: Message):
    await send_error_message(message, available_meeting_format)


@router.message(HobbiesQuest.choosing_zodiac_signs, F.text.in_(available_zodiac_signs))
async def choosing_zodiac_signs(message: Message, state: FSMContext):
    chosen_zodiac_signs = message.text.lower()
    for i in range(len(available_zodiac_signs)):
        if available_zodiac_signs[i].lower() == chosen_zodiac_signs:
            await state.update_data(chosen_zodiac_signs=i)
    await message.answer(
        text="😈 <b>Выберете свой тип личности</b>\n\n"
             "Если не знаете свой тип личности, можете выбрать по названию или почитать подробней"
             " <a href='https://www.16personalities.com/ru/tipy-lichnosti'>на сайте</a>.\n",
        reply_markup=make_colum_keyboard(available_personality_type)
    )
    await state.set_state(HobbiesQuest.choosing_personality_type)


@router.message(StateFilter("HobbiesQuest:choosing_zodiac_signs"))
async def quest_chosen_incorrectly_zodiac_signs(message: Message):
    await send_error_message(message, available_zodiac_signs)


@router.message(HobbiesQuest.choosing_personality_type, F.text.in_(available_personality_type))
async def choosing_personality_type(message: Message, state: FSMContext):
    chosen_personality_type = message.text.lower()
    for i in range(len(available_personality_type)):
        if available_personality_type[i].lower() == chosen_personality_type:
            await state.update_data(chosen_personality_type=i)
    await message.answer(
        text="🐙 <b>Выберете свой пол </b>",
        reply_markup=make_colum_keyboard(available_gender)
    )
    await state.set_state(HobbiesQuest.choosing_gender)


@router.message(StateFilter("HobbiesQuest:choosing_personality_type"))
async def quest_chosen_incorrectly_personality_type(message: Message):
    await send_error_message(message, available_personality_type)


@router.message(HobbiesQuest.choosing_gender, F.text.in_(available_gender))
async def choosing_gender(message: Message, state: FSMContext):
    chosen_gender = message.text.lower()
    for i in range(len(available_gender)):
        if available_gender[i].lower() == chosen_gender:
            await state.update_data(chosen_gender=i)
    await message.answer(
        text="🎨 <b>Выберете свои увлечения из списка</b>",
        reply_markup=make_colum_keyboard(available_hobbies)
    )
    await state.set_state(HobbiesQuest.choosing_hobbies)


@router.message(StateFilter("HobbiesQuest:choosing_gender"))
async def quest_chosen_incorrectly_hobbies(message: Message):
    await send_error_message(message, available_gender)


@router.message(HobbiesQuest.choosing_hobbies, F.text.in_(available_hobbies))
async def choosing_hobbies(message: Message, state: FSMContext):
    user_data = await state.get_data()
    chosen_hobbies_str = str(user_data['chosen_hobbies'])
    if chosen_hobbies_str is None:
        chosen_hobbies_str = ""
    chosen_hobbies = chosen_hobbies_str.lower().split(', ')

    chosen_hobbies.append(message.text.lower())
    await state.update_data(chosen_hobbies=', '.join(chosen_hobbies))
    await message.answer(
        text="👀 Вы можете выбрать еще хобби или нажать <b>'продолжить'</b>",
        reply_markup=make_colum_keyboard(available_hobbies, chosen_hobbies, continue_button=True)
    )


@router.message(HobbiesQuest.choosing_hobbies, F.text == "Продолжить")
async def tell_hobbies(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await rq.set_user_choosing_questionnaire(message.from_user.id, user_data)
    await message.answer(
        text="🏂 <b>Расскажите про ваши увлечения подробней!</b>\n\n"
             "Просто пару предложений одним сообщением о ваших интересах, взглядах, хобби)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(HobbiesQuest.tell_hobbies)


@router.message(StateFilter("HobbiesQuest:choosing_hobbies"))
async def quest_chosen_incorrectly_hobbies(message: Message):
    await message.answer(
        text="😭 Я не понимаю такого ответа.\n\nПожалуйста, выберите один из вариантов "
             "из списка:",
    )


@router.message(HobbiesQuest.tell_hobbies, lambda message: len(message.text) > 5)
async def tell_hobbies(message: Message, state: FSMContext):
    await state.update_data(tell_hobbies=message.text.lower())
    await message.answer(
        text="👨🏻‍🔬 <b>Кем вы работаете и чем занимаетесь?</b>\n\n"
             "❌ Дизайнер \n"
             "✅ Motion-дизайнер в Et-tech стартапе, занимаюсь созданием визуальным оформлением онлайн курсов.\n\n"
             "Если не работаете, расскажите на кого учитесь и чем хотите заниматься.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(HobbiesQuest.tell_what_do_you_do)


@router.message(StateFilter("HobbiesQuest:tell_hobbies"))
async def quest_tell_hobbies_incorrectly(message: Message):
    await message.answer(
        text="😇 Пожалуйста, опишите ваши хобби, немного подробней!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(HobbiesQuest.tell_what_do_you_do, lambda message: len(message.text) > 5)
async def tell_what_do_you_do(message: Message, state: FSMContext):
    await state.update_data(tell_what_do_you_do=message.text.lower())
    await message.answer(
        text="📝 <b>Если бы вы состояли в клубе, то зачем?</b>\n\n"
             "Просто пару предложений о том, что вы хотели бы получить от клуба.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(HobbiesQuest.tell_expectations)


@router.message(StateFilter("HobbiesQuest:tell_what_do_you_do"))
async def quest_tell_what_do_you_do_incorrectly(message: Message):
    await message.answer(
        text="😇 Пожалуйста, опишите чем вы занимаетесь в свободное время, немного подробней!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(HobbiesQuest.tell_expectations, lambda message: len(message.text) > 5)
async def invite_friends(message: Message, state: FSMContext):
    await state.update_data(tell_expectations=message.text.lower())
    await message.answer(
        text="🫶🏻 Вы хотите остаться с нами на связи?",
        reply_markup=make_colum_keyboard(available_stay_in_touch)
    )
    await state.set_state(HobbiesQuest.choosing_stay_in_touch)


@router.message(StateFilter("HobbiesQuest:tell_expectations"))
async def quest_tell_expectations_incorrectly(message: Message):
    await message.answer(
        text="😇 Пожалуйста, опишите ваши ожидания от клуба, немного подробней!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(HobbiesQuest.choosing_stay_in_touch, F.text.in_(available_stay_in_touch))
async def quest_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_stay_in_touch=message.text.lower())
    chosen_stay_in_touch = message.text.lower()
    for i in range(len(available_stay_in_touch)):
        if available_stay_in_touch[i].lower() == chosen_stay_in_touch:
            await state.update_data(chosen_stay_in_touch=i)
    user_data = await state.get_data()
    await message.answer(
        text="🎉 <b>Вы прошли все вопросы! Спасибо за ответы!</b> ❤️\n\n"
             "Создателям очень важно собрать как можно больше ответов, чтобы воплотить в жизнь свой замысел!\n\n"
             "Вы можете помочь нам! Заодно поучаствовать в <b>розыгрыше призов</b>, опросив своего хорошего друга!\n"
             "Ещё раз нажав на /quest\n\n\n"
             "p.s. Как вы могли заметить вопросы простые и их не много)\n"
             "Уверены, что вы знаете увлечения своих друзей "
             "и сможете заполнить анкету ещё раз, даже если их нет рядом.",

        reply_markup=get_main_kb()
    )
    await rq.set_user_tell_questionnaire(message.from_user.id, user_data),
    await state.clear()


@router.message(HobbiesQuest.choosing_stay_in_touch)
async def quest_chosen_incorrectly(message: Message):
    await send_error_message(message, available_stay_in_touch)
