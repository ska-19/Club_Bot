from database.models import Questionnaire, async_session
from sqlalchemy import select, desc, distinct


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Questionnaire).where(Questionnaire.tg_id == tg_id))
        if not user:
            session.add(Questionnaire(tg_id=tg_id, questionnaire_counter=0))
        await session.commit()


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Questionnaire).where(Questionnaire.tg_id == tg_id))
        return user


async def set_user_choosing_questionnaire(tg_id, user_questionnaire_data):
    async with async_session() as session:
        last_questionnaire = await session.scalar(
            select(Questionnaire)
            .where(Questionnaire.tg_id == tg_id)
            .order_by(desc(Questionnaire.questionnaire_counter))
        )
        if last_questionnaire.choosing_stay_in_touch != -1:
            questionnaire = Questionnaire(tg_id=tg_id,
                                          questionnaire_counter=last_questionnaire.questionnaire_counter + 1)
        else:
            questionnaire = last_questionnaire
        session.add(questionnaire)

        questionnaire.choosing_knew_interest_clubs = user_questionnaire_data['chosen_knew_interest_clubs']
        questionnaire.choosing_readiness_new_meetings = user_questionnaire_data['chosen_readiness_new_meetings']
        questionnaire.choosing_expectations = user_questionnaire_data['chosen_expectations']
        questionnaire.choosing_meeting_format = user_questionnaire_data['chosen_meeting_format']
        questionnaire.choosing_zodiac_signs = user_questionnaire_data['chosen_zodiac_signs']
        questionnaire.choosing_personality_type = user_questionnaire_data['chosen_personality_type']
        questionnaire.choosing_gender = user_questionnaire_data['chosen_gender']
        questionnaire.choosing_hobbies = user_questionnaire_data['chosen_hobbies']

        await session.commit()


async def set_user_tell_questionnaire(tg_id, user_questionnaire_data):
    async with async_session() as session:
        questionnaire = await session.scalar(
            select(Questionnaire)
            .where(Questionnaire.tg_id == tg_id)
            .order_by(desc(Questionnaire.questionnaire_counter))
        )
        questionnaire.tell_hobbies = user_questionnaire_data['tell_hobbies']
        questionnaire.tell_what_do_you_do = user_questionnaire_data['tell_what_do_you_do']
        questionnaire.tell_expectations = user_questionnaire_data['tell_expectations']
        questionnaire.choosing_stay_in_touch = user_questionnaire_data['chosen_stay_in_touch']

        await session.commit()


async def get_users():
    async with async_session() as session:
        users_tg_id = await session.execute(select(distinct(Questionnaire.tg_id)))
        return users_tg_id.scalars().all()

