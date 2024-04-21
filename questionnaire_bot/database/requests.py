from database.models import Questionnaire, async_session
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Questionnaire).where(Questionnaire.tg_id == tg_id))

        if not user:
            session.add(Questionnaire(tg_id=tg_id))
            # await session.commit()
        await session.commit()


# async def get_categories():
#     async with async_session() as session:
#         return await session.scalars(select(Category))


# async def get_items(category_id):
#     async with async_session() as session:
#         return await session.scalars(select(Item).where(Item.category == category_id))


# async def get_item(item_id):
#     async with async_session() as session:
#         return await session.scalar(select(Item).where(Item.id == item_id))


# async def set_item_basket(tg_id, item_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         session.add(Basket(user=user.id, item=item_id))
#         await session.commit()

async def set_user_questionnaire(tg_id, user_questionnaire_data):
    async with async_session() as session:
        questionnaire = await session.scalar(select(Questionnaire).where(Questionnaire.tg_id == tg_id))

        questionnaire.choosing_knew_interest_clubs = user_questionnaire_data['chosen_knew_interest_clubs']
        questionnaire.choosing_readiness_new_meetings = user_questionnaire_data['chosen_readiness_new_meetings']
        questionnaire.choosing_expectations = user_questionnaire_data['chosen_expectations']
        questionnaire.choosing_meeting_format = user_questionnaire_data['chosen_meeting_format']
        questionnaire.choosing_hobbies = user_questionnaire_data['chosen_hobbies']
        questionnaire.tell_hobbies = user_questionnaire_data['tell_hobbies']
        questionnaire.tell_expectations = user_questionnaire_data['tell_expectations']
        questionnaire.choosing_stay_in_touch = user_questionnaire_data['chosen_stay_in_touch']

        await session.commit()

# async def set_questionnaire(tg_id, choosing_knew_interest_clubs, choosing_readiness_new_meetings, choosing_expectations,
#                             choosing_meeting_format, choosing_hobbies, tell_hobbies, tell_expectations, choosing_stay_in_touch):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         session.add(Questionnaire(tg_id=user.id, choosing_knew_interest_clubs=choosing_knew_interest_clubs,
#                                   choosing_readiness_new_meetings=choosing_readiness_new_meetings,
#                                   choosing_expectations=choosing_expectations, choosing_meeting_format=choosing_meeting_format,
#                                   choosing_hobbies=choosing_hobbies, tell_hobbies=tell_hobbies,
#                                   tell_expectations=tell_expectations, choosing_stay_in_touch=choosing_stay_in_touch))
#         await session.commit()

# async def get_my_basket(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         basket_items = await session.scalars(select(Basket).where(Basket.user == user.id))
#         return basket_items