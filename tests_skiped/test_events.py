import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac


def test_create_userr():
    data = {
        "id": 40,
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
        "id": 48,
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
        "id": 49,
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
        "id": 42,
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


def testt_create_club():
    data = {
        "owner": 40,
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
        "owner": 48,
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


def test_create_event_good():
    data = {
        'club_id': 1,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/create_event", json=data)
    data = {
        "club_id": 1,
        "user_id": 42,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200


async def test_create_event_good_async(ac):
    data = {
        'club_id': 1,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200


def test_create_event_club_no_exist():
    data = {
        'club_id': 100,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404


async def test_create_event_club_no_exist_async(ac):
    data = {
        'club_id': 100,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404


def test_create_event_host_no_exist():
    data = {
        'club_id': 1,
        'host_id': 100,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404



async def test_create_event_host_no_exist_async(ac):
    data = {
        'club_id': 1,
        'host_id': 100,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404


def test_create_event_host_no_in_club():
    data = {
        'club_id': 1,
        'host_id': 48,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/create_event", json=data)
    print(response.json())
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


async def test_create_event_host_no_in_club_async(ac):
    data = {
        'club_id': 1,
        'host_id': 48,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'



def test_create_event_host_no_permission():
    data = {
        'club_id': 1,
        'host_id': 42,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'


async def test_create_event_host_no_permission_async(ac):
    data = {
        'club_id': 1,
        'host_id': 42,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'


def test_create_event_host_no_permission():
    data = {
        'club_id': 1,
        'host_id': 42,
        'date': '2021-01-01',
        'sinopsis': 'string',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'



def test_get_event_good():
    response = client.get("/events/get_event", params={'event_id': 1})
    assert response.status_code == 200


async def test_get_event_good_async(ac):
    response = await ac.get("/events/get_event", params={'event_id': 1})
    assert response.status_code == 200


def test_get_event_no_exist():
    response = client.get("/events/get_event", params={'event_id': 100})
    assert response.status_code == 404


async def test_get_event_no_exist_async(ac):
    response = await ac.get("/events/get_event", params={'event_id': 100})
    assert response.status_code == 404



def test_update_event_good():
    data = {
        'club_id': 1,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 200 and response.json()['data']['sinopsis'] == 'string_updated'


async def test_update_event_good_async(ac):
    data = {
        'club_id': 1,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 200 and response.json()['data']['sinopsis'] == 'string_updated'


def test_update_event_no_exist():
    data = {
        'club_id': 1,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/update_event", params={'event_id': 100}, json=data)
    assert response.status_code == 404


async def test_update_event_no_exist_async(ac):
    data = {
        'club_id': 1,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/update_event", params={'event_id': 100}, json=data)
    assert response.status_code == 404


def test_update_event_host_no_exist():
    data = {
        'club_id': 1,
        'host_id': 100,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404


async def test_update_event_host_no_exist_async(ac):
    data = {
        'club_id': 1,
        'host_id': 100,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404



def test_update_event_another_host():
    data = {
        'club_id': 1,
        'host_id': 48,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'


async def test_update_event_another_host(ac):
    data = {
        'club_id': 1,
        'host_id': 48,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'


def test_update_event_host_no_permission():
    data = {
        'club_id': 1,
        'host_id': 42,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'


async def test_update_event_host_no_permission_async(ac):
    data = {
        'club_id': 1,
        'host_id': 42,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has no permission to create/update event'



def test_update_event_club_no_exist():
    data = {
        'club_id': 100,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = client.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404


async def test_update_event_club_no_exist_async(ac):
    data = {
        'club_id': 100,
        'host_id': 40,
        'date': '2021-01-01',
        'sinopsis': 'string_updated',
        'contact': 'string',
        'speaker': 'string'

    }
    response = await ac.post("/events/update_event", params={'event_id': 1}, json=data)
    assert response.status_code == 404



def test_event_reg_good():
    data = {
        "user_id": 42,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 200


async def test_event_reg_good_async(ac):
    data = {
        "user_id": 42,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 200


def test_event_reg_user_no_exist():
    data = {
        "user_id": 100,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 404


async def test_event_reg_user_no_exist_async(ac):
    data = {
        "user_id": 100,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 404


def test_event_reg_event_no_exist():
    data = {
        "user_id": 42,
        "event_id": 100,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 404



async def test_event_reg_event_no_exist_async(ac):
    data = {
        "user_id": 42,
        "event_id": 100,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 404



def test_event_reg_user_no_in_club():
    data = {
        "user_id": 48,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


async def test_event_reg_user_no_in_club_async(ac):
    data = {
        "user_id": 48,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'



def test_get_event_club_good():
    response = client.get("/events/get_event_club", params={'club_id': 1})
    assert response.status_code == 200


async def test_get_event_club_good_async(ac):
    response = await ac.get("/events/get_event_club", params={'club_id': 1})
    assert response.status_code == 200


def test_get_event_club_no_exist():
    response = client.get("/events/get_event_club", params={'club_id': 100})
    assert response.status_code == 404


async def test_get_event_club_no_exist_async(ac):
    response = await ac.get("/events/get_event_club", params={'club_id': 100})
    assert response.status_code == 404



def test_event_disreg_good():
    response = client.post("/events/event_disreg", params={'user_id': 42, 'event_id': 1})
    assert response.status_code == 200
    data = {
        "user_id": 42,
        "event_id": 1,
        "confirm": True,
        "reg_date": "2021-01-01"
    }
    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 200


async def test_event_disreg_good_async(ac): # пример зачем нужны одновременно обычные и асинхронные
    response = await ac.post("/events/event_disreg", params={'user_id': 42, 'event_id': 1})
    assert response.status_code == 200


def test_event_disreg_user_no_exist():
    response = client.post("/events/event_disreg", params={'user_id': 100, 'event_id': 1})
    assert response.status_code == 404


async def test_event_disreg_user_no_exist_async(ac):
    response = await ac.post("/events/event_disreg", params={'user_id': 100, 'event_id': 1})
    assert response.status_code == 404


def test_event_disreg_event_no_exist():
    response = client.post("/events/event_disreg", params={'user_id': 42, 'event_id': 100})
    assert response.status_code == 404


async def test_event_disreg_event_no_exist_async(ac):
    response = await ac.post("/events/event_disreg", params={'user_id': 42, 'event_id': 100})
    assert response.status_code == 404


def test_event_disreg_user_no_in_club():
    response = client.post("/events/event_disreg", params={'user_id': 48, 'event_id': 1})
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has not registration in this event'


async def test_event_disreg_user_no_in_club_async(ac):
    response = await ac.post("/events/event_disreg", params={'user_id': 48, 'event_id': 1})
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has not registration in this event'



def test_event_disreg_user_no_in_event():
    response = client.post("/events/event_disreg", params={'user_id': 42, 'event_id': 2})
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has not registration in this event'


async def test_event_disreg_user_no_in_event_async(ac):
    response = await ac.post("/events/event_disreg", params={'user_id': 42, 'event_id': 2})
    assert response.status_code == 404 and response.json()['detail']['data'] == 'User has not registration in this event'



def test_delete_event_good():
    response = client.post("/events/delete_event", params={'event_id': 1})
    assert response.status_code == 200


async def test_delete_event_good_async(ac):
    response = await ac.post("/events/delete_event", params={'event_id': 1})
    assert response.status_code == 200


def test_delete_event_no_exist():
    response = client.post("/events/delete_event", params={'event_id': 1})
    assert response.status_code == 404


async def test_delete_event_no_exist_async(ac):
    response = await ac.post("/events/delete_event", params={'event_id': 100})
    assert response.status_code == 404


















