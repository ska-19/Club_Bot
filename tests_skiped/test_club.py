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
        "name": "test_club",
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
    assert response.json()['data']['name'] == "test_club"
    assert response.json()['data']['dest'] == "string"
    assert response.json()['data']['photo'] == "string"
    assert response.json()['data']['bio'] == "string"
    assert response.json()['data']['links'] == "string"
    assert response.json()['data']['channel_link'] == "string"
    assert response.json()['data']['comfort_time'] == "string"
    assert response.json()['data']['date_created'] == "2021-01-01"

    response = client.post("/club/delete_club", params={"club_id": 1})
    assert response.status_code == 200
    response = client.get("/club/get_club", params={"club_id": 1})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404



async def test_create_club_good_async(ac):
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

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "owner": 1,
        "name": "test_club_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200
    assert response.json()['data']['owner'] == 1
    assert response.json()['data']['name'] == "test_club_async"
    assert response.json()['data']['dest'] == "string"
    assert response.json()['data']['photo'] == "string"
    assert response.json()['data']['bio'] == "string"
    assert response.json()['data']['links'] == "string"
    assert response.json()['data']['channel_link'] == "string"
    assert response.json()['data']['comfort_time'] == "string"
    assert response.json()['data']['date_created'] == "2021-01-01"

    club_id = response.json()['data']['id'] # Из - за асинхронности иногда клуб может не успеть удалиться а новый уже добвиться, поэтому id предсказать невозможно

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404



def test_create_club_same_name():
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
        "name": "test_club",
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

    club_id = response.json()['data']['id']

    response = client.post("/club/create_club", json=data)
    assert response.status_code == 409

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


async def test_create_club_same_name_async(ac):
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

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "owner": 1,
        "name": "test_club",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id = response.json()['data']['id']

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 409

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404




def test_create_club_user_no_exist():
    data = {
        "owner": 1,
        "name": "test_club",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = client.post("/club/create_club", json=data)
    assert response.status_code == 404



async def test_create_club_user_no_exist_async(ac):
    data = {
        "owner": 1,
        "name": "test_club",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 404



def test_get_club_id_no_exist():
    response = client.get("/club/get_club", params={"club_id": 1})
    assert response.status_code == 404

async def test_get_club_id_no_exist(ac):
    response = await ac.get("/club/get_club", params={"club_id": 1})
    assert response.status_code == 404



def test_get_club_link_good():
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
        "name": "test_club",
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

    club_id = response.json()['data']['id']

    response = client.get("/club/get_channel_link", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_get_club_link_good_async(ac):
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

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "owner": 1,
        "name": "test_club",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id = response.json()['data']['id']

    response = await ac.get("/club/get_channel_link", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


def test_get_club_no_exist():
    response = client.get("/club/get_channel_link", params={"club_id": 1})
    assert response.status_code == 404



async def test_get_club_no_exist_async(ac):
    response = await ac.get("/club/get_channel_link", params={"club_id": 1})
    assert response.status_code == 404


def test_update_club_good():
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
        "name": "test_club",
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

    club_id = response.json()['data']['id']

    data = {
        "name": "test_club_update",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = client.post("/club/update_club", params={"club_id": club_id}, json=data)
    assert response.status_code == 200
    assert response.json()['data']['name'] == "test_club_update"

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_update_club_good_async(ac):
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

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "owner": 1,
        "name": "test_club",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id = response.json()['data']['id']

    data = {
        "name": "test_club_update",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/update_club", params={"club_id": club_id}, json=data)
    assert response.status_code == 200
    assert response.json()['data']['name'] == "test_club_update"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404



def test_update_club_no_exist():
    data = {
        "name": "test_club_update",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = client.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 404



async def test_update_club_no_exist_async(ac):
    data = {
        "name": "test_club_update",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-01"
    }

    response = await ac.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 404









