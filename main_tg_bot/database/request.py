from database.models import async_session
from sqlalchemy import select, desc
import requests
from dotenv import load_dotenv
from aiogram.enums import ParseMode
import os

load_dotenv('.env')
URL = os.getenv('URL')


async def set_user(user_data):
    rq_user_data = {
        "id": int(user_data["tg_id"]),
        "username": str(user_data["username"]),
        "name": '' if user_data["name"] is None or 'None' else str(user_data["name"]),
        "surname": '' if user_data["surname"] is None or 'None' else str(user_data["surname"]),
    }

    headers = {
        "Content-Type": "application/json"
    }
    url = str(URL)+'/user_profile/create_user'

    response = requests.post(url, json=rq_user_data, headers=headers)

    if response.status_code == 409:
        response = requests.post(str(URL)+'/user_profile/update_user',
                                 json=rq_user_data,
                                 headers=headers,)
    return response


async def set_club(tg_id, club_data):
    if club_data['channel_link'][0] == '@':
        club_data['channel_link'] = 'https://t.me/'+club_data['channel_link'][1:]

    rq_club_data = {
        "owner": int(tg_id),
        "dest": str(club_data['dest']),
        "photo": str(''),
        "bio": str(club_data['bio']),
        "links": str(''),
        "channel_link": str(club_data['channel_link']),
        # comfort_time: str
        # date_created: date
    }

    headers = {
        "Content-Type": "application/json"
    }
    url = str(URL)+'/club/create_cub'

    response = requests.post(url, json=rq_club_data, headers=headers)
    return response

