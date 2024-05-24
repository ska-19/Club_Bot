import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac


def test_create_user():
    data = {
        "id": 10,
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
    assert response.status_code == 200


def test_create_club_good():  # TODO: оч сильно не хватает метода delete_user
    data = {
        "owner": 10,
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
    assert response.status_code == 200


async def test_create_club_good_async(ac):
    data = {
        "owner": 10,
        "name": "test_club_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200


def test_crate_club_same_name():
    data = {
        "owner": 10,
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
    assert response.status_code == 409


async def test_create_club_same_name_async(ac):
    data = {
        "owner": 10,
        "name": "test_club_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 409

def test_create_club_owner_not_exist():
    data = {
        "owner": 11,
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
    assert response.status_code == 404


async def test_create_club_owner_not_exist_async(ac):
    data = {
        "owner": 11,
        "name": "test_club_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 404


def test_create_club_without_name():
    data = {
        "owner": 10,
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/create_club", json=data)
    assert response.status_code == 422


async def test_create_club_without_name_async(ac):
    data = {
        "owner": 10,
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 422


def test_create_club_without_owner():
    data = {
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
    assert response.status_code == 422


async def test_create_club_without_owner_async(ac):
    data = {
        "name": "test_club_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 422


def test_get_club_good():
    response = client.get("/club/get_club", params={"club_id": 1})
    assert response.status_code == 200


async def test_get_club_good_async(ac):
    response = await ac.get("/club/get_club", params={"club_id": 1})
    assert response.status_code == 200


def test_get_club_not_exist():
    response = client.get("/club/get_club", params={"club_id": 1000})
    assert response.status_code == 404


async def test_get_club_not_exist_async(ac):
    response = await ac.get("/club/get_club", params={"club_id": 1000})
    assert response.status_code == 404


def test_get_club_without_id():
    response = client.get("/club/get_club", params={})
    assert response.status_code == 422


async def test_get_club_without_id_async(ac):
    response = await ac.get("/club/get_club", params={})
    assert response.status_code == 422



def test_update_club_good():
    data = {
        "name": "test_club_updated",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 200



async def test_update_club_good_async(ac):
    data = {
        "name": "test_club_updated_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/update_club", params={"club_id": 2}, json=data)
    assert response.status_code == 200


def test_update_club_not_exist():
    data = {
        "name": "test_club_updated",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/update_club", params={"club_id": 1000}, json=data)
    assert response.status_code == 404



async def test_update_club_not_exist_async(ac):
    data = {
        "name": "test_club_updated_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/update_club", params={"club_id": 1000}, json=data)
    assert response.status_code == 404



def test_update_club_without_name():
    data = {
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 422


async def test_update_club_without_name_async(ac):
    data = {
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 422


def test_update_club_without_id():
    data = {
        "name": "test_club_updated",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/update_club", params={}, json=data)
    assert response.status_code == 422


async def test_update_club_without_id_async(ac):
    data = {
        "name": "test_club_updated",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/update_club", params={}, json=data)
    assert response.status_code == 422


def test_update_club_same_name_was(): #TODO: такое наверное хотим пофиксить
    data = {
        "name": "test_club_updated",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 200


async def test_update_club_same_name_was_async(ac):
    data = {
        "name": "test_club_updated_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/update_club", params={"club_id": 2}, json=data)
    assert response.status_code == 200


def test_update_club_same_name():
    data = {
        "name": "test_club_updated_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = client.post("/club/update_club", params={"club_id": 1}, json=data)
    assert response.status_code == 409


async def test_update_club_same_name_async(ac):
    data = {
        "name": "test_club_updated",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": '2021-01-01'
    }
    response = await ac.post("/club/update_club", params={"club_id": 2}, json=data)
    assert response.status_code == 409






