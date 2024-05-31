import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac

def test_init():
    data = {
        "id": 50,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "dob": "2021-08-16",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "xp": 0,
        "city": "string",
        "education": "string",
        "achievments": "string",
    }

    data2 = {
        "id": 58,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "dob": "2021-08-16",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "xp": 0,
        "city": "string",
        "education": "string",
        "achievments": "string",
    }

    data3 = {
        "id": 59,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "dob": "2021-08-16",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "xp": 0,
        "city": "string",
        "education": "string",
        "achievments": "string",
    }

    data4 = {
        "id": 52,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "dob": "2021-08-16",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "xp": 0,
        "city": "string",
        "education": "string",
        "achievments": "string",
    }

    data5 = {
        "id": 53,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "dob": "2021-08-16",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "xp": 0,
        "city": "string",
        "education": "string",
        "achievments": "string",
    }

    data6 = {
        "id": 54,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "dob": "2021-08-16",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "xp": 0,
        "city": "string",
        "education": "string",
        "achievments": "string",
    }

    response = client.post("/user_profile/create_user", json=data)
    response2 = client.post("/user_profile/create_user", json=data2)
    response3 = client.post("/user_profile/create_user", json=data3)
    response4 = client.post("/user_profile/create_user", json=data4)
    response4 = client.post("/user_profile/create_user", json=data5)
    response4 = client.post("/user_profile/create_user", json=data6)

    data = {
        "owner": 50,
        "name": "test_club",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/create_club", json=data)

    data2 = {
        "owner": 58,
        "name": "test_club2",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }

    response = client.post("/club/create_club", json=data2)

    data = {
        "club_id": 1,
        "user_id": 59,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)

    data = {
        "club_id": 2,
        "user_id": 52,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)

    data = {
        "club_id": 1,
        "user_id": 53,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)

    data = {
        "club_id": 2,
        "user_id": 54,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)



def test_add_product_good():
    data = {
        "name": "test_product",
        "price": 100,
        "description": "string",
        "photo": "string",
        "quantity": 10,
        "rating": 5,
        "admin_id": 50,
        "club_id": 1
    }

    response = client.post("/market/add_product", json=data)
    assert response.status_code == 200

