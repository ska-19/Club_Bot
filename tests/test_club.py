import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac


def test_create_club_good():
    data = {
        "id": 1,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }

    response = client.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "owner": 1,
        "name": "string",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = client.post("/club/create_club", json=data)
    assert response.status_code == 200
    assert response.json()['data']['owner'] == 1
    assert response.json()['data']['name'] == "string"
    assert response.json()['data']['dest'] == "string"
    assert response.json()['data']['photo'] == "string"
    assert response.json()['data']['bio'] == "string"
    assert response.json()['data']['links'] == "string"
    assert response.json()['data']['channel_link'] == "string"
    assert response.json()['data']['comfort_time'] == "string"
    assert response.json()['data']['date_created'] == "2021-01-01"

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.post("/club/delete_club", params={"club_id": 1})
    assert response.status_code == 200
    response = client.post("/club/get_club", params={"club_id": 1})
    assert response.status_code == 404

    response = client.post("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404






