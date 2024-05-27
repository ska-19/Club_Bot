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
        "name": str(user_data["name"]),
        "surname": str(user_data["surname"]),
    }

    headers = {
        "Content-Type": "application/json"
    }
    url = str(URL)+'/user_profile/create_user'

    response = requests.post(url, json=rq_user_data, headers=headers)
    return response


async def set_club(tg_id, club_data):

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

