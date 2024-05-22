import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac


def test_init():
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

    data5 = {
        "id": 43,
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
        "id": 44,
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

    data = {
        "club_id": 1,
        "user_id": 49,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)

    data = {
        "club_id": 2,
        "user_id": 42,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)

    data = {
        "club_id": 1,
        "user_id": 43,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)

    data = {
        "club_id": 2,
        "user_id": 44,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)



def test_add_reward_good():
    data = {
        "info": "test",
        "exp": 10,
        "admin_id": 40,
        "club_id": 1
    }
    response = client.post("/reward/add_reward", json=data)
    assert response.status_code == 200


async def test_add_reward_good_async(ac):
    data = {
        "info": "test_async",
        "exp": 10,
        "admin_id": 48,
        "club_id": 2
    }
    response = await ac.post("/reward/add_reward", json=data)
    assert response.status_code == 200


def test_add_reward_admin_no_exist():
    data = {
        "info": "test",
        "exp": 10,
        "admin_id": 41,
        "club_id": 1
    }
    response = client.post("/reward/add_reward", json=data)
    assert response.status_code == 404


async def test_add_reward_admin_no_exist_async(ac):
    data = {
        "info": "test_async",
        "exp": 10,
        "admin_id": 41,
        "club_id": 1
    }
    response = await ac.post("/reward/add_reward", json=data)
    assert response.status_code == 404


def test_add_reward_club_no_exist():
    data = {
        "info": "test",
        "exp": 10,
        "admin_id": 40,
        "club_id": 2
    }
    response = client.post("/reward/add_reward", json=data)
    assert response.status_code == 404


async def test_add_reward_club_no_exist_async(ac):
    data = {
        "info": "test_async",
        "exp": 10,
        "admin_id": 40,
        "club_id": 2
    }
    response = await ac.post("/reward/add_reward", json=data)
    assert response.status_code == 404


def test_add_reward_admin_has_no_permission():
    data = {
        "info": "test",
        "exp": 10,
        "admin_id": 49,
        "club_id": 1
    }
    response = client.post("/reward/add_reward", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User has no permission to create/update reward"


async def test_add_reward_admin_has_no_permission_async(ac):
    data = {
        "info": "test_async",
        "exp": 10,
        "admin_id": 49,
        "club_id": 1
    }
    response = await ac.post("/reward/add_reward", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User has no permission to create/update reward"


def test_update_reward_good():
    data = {
        "info": "test_updated",
        "exp": 10,
        "admin_id": 40,
        "club_id": 1
    }
    response = client.post("/reward/update_reward", params={'reward_id': 1}, json=data)


async def test_update_reward_good_async(ac):
    data = {
        "info": "test_updated_async",
        "exp": 10,
        "admin_id": 48,
        "club_id": 2
    }
    response = await ac.post("/reward/update_reward", params={'reward_id': 2}, json=data)


def test_update_reward_admin_no_exist():
    data = {
        "info": "test_updated",
        "exp": 10,
        "admin_id": 41,
        "club_id": 1
    }
    response = client.post("/reward/update_reward", params={'reward_id': 1}, json=data)
    assert response.status_code == 404


async def test_update_reward_admin_no_exist_async(ac):
    data = {
        "info": "test_updated_async",
        "exp": 10,
        "admin_id": 41,
        "club_id": 1
    }
    response = await ac.post("/reward/update_reward", params={'reward_id': 1}, json=data)
    assert response.status_code == 404



def test_update_reward_club_no_exist():
    data = {
        "info": "test_updated",
        "exp": 10,
        "admin_id": 40,
        "club_id": 100
    }
    response = client.post("/reward/update_reward", params={'reward_id': 1}, json=data)
    assert response.status_code == 404



async def test_update_reward_club_no_exist_async(ac):
    data = {
        "info": "test_updated_async",
        "exp": 10,
        "admin_id": 40,
        "club_id": 100
    }
    response = await ac.post("/reward/update_reward", params={'reward_id': 1}, json=data)
    assert response.status_code == 404



def test_update_reward_admin_has_no_permission():
    data = {
        "info": "test_updated",
        "exp": 10,
        "admin_id": 49,
        "club_id": 1
    }
    response = client.post("/reward/update_reward", params={'reward_id': 1}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User has no permission to create/update reward"


async def test_update_reward_admin_has_no_permission_async(ac):
    data = {
        "info": "test_updated_async",
        "exp": 10,
        "admin_id": 49,
        "club_id": 1
    }
    response = await ac.post("/reward/update_reward", params={'reward_id': 1}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User has no permission to create/update reward"



def test_update_reward_reward_no_exist():
    data = {
        "info": "test_updated",
        "exp": 10,
        "admin_id": 40,
        "club_id": 1
    }
    response = client.post("/reward/update_reward", params={'reward_id': 100}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"



async def test_update_reward_reward_no_exist_async(ac):
    data = {
        "info": "test_updated_async",
        "exp": 10,
        "admin_id": 40,
        "club_id": 1
    }
    response = await ac.post("/reward/update_reward", params={'reward_id': 100}, json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"



def test_get_reward_good():
    response = client.get("/reward/get_reward", params={'reward_id': 1})
    assert response.status_code == 200 and response.json()['data']['info'] == 'test_updated'


async def test_get_reward_good_async(ac):
    response = await ac.get("/reward/get_reward", params={'reward_id': 2})
    assert response.status_code == 200 and response.json()['data']['info'] == 'test_updated_async'


def test_get_reward_reward_no_exist():
    response = client.get("/reward/get_reward", params={'reward_id': 100})
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"


async def test_get_reward_reward_no_exist_async(ac):
    response = await ac.get("/reward/get_reward", params={'reward_id': 100})
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"


def test_add_reward_to_user_good():
    data = {
        "admin_id": 40,
        "user_id": 49,
        "reward_id": 1
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 200


async def test_add_reward_to_user_good_async(ac):
    data = {
        "admin_id": 48,
        "user_id": 42,
        "reward_id": 2
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 200


def test_add_reward_to_user_admin_no_exist():
    data = {
        "admin_id": 41,
        "user_id": 49,
        "reward_id": 1
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404


async def test_add_reward_to_user_admin_no_exist_async(ac):
    data = {
        "admin_id": 41,
        "user_id": 42,
        "reward_id": 2
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404


def test_add_reward_to_user_user_no_exist():
    data = {
        "admin_id": 40,
        "user_id": 100,
        "reward_id": 1
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404


async def test_add_reward_to_user_user_no_exist_async(ac):
    data = {
        "admin_id": 48,
        "user_id": 100,
        "reward_id": 2
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404


def test_add_reward_to_user_reward_no_exist():
    data = {
        "admin_id": 40,
        "user_id": 49,
        "reward_id": 100
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"


async def test_add_reward_to_user_reward_no_exist_async(ac):
    data = {
        "admin_id": 48,
        "user_id": 42,
        "reward_id": 100
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"


def test_add_reward_to_user_admin_has_no_permission():
    data = {
        "admin_id": 49,
        "user_id": 43,
        "reward_id": 1
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User has no permission to create/update reward"


async def test_add_reward_to_user_admin_has_no_permission_async(ac):
    data = {
        "admin_id": 42,
        "user_id": 44,
        "reward_id": 2
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User has no permission to create/update reward"



def test_add_reward_to_user_user_has_reward():
    data = {
        "admin_id": 40,
        "user_id": 49,
        "reward_id": 1
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User already has this reward"


async def test_add_reward_to_user_user_has_reward_async(ac):
    data = {
        "admin_id": 48,
        "user_id": 42,
        "reward_id": 2
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "User already has this reward"


def test_add_reward_to_user_reward_not_in_club(): #TODO: мб про этот фидбек стоит подумать
    data = {
        "admin_id": 40,
        "user_id": 43,
        "reward_id": 2
    }
    response = client.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "This user not in this club"



async def test_add_reward_to_user_reward_not_in_club_async(ac):
    data = {
        "admin_id": 48,
        "user_id": 44,
        "reward_id": 1
    }
    response = await ac.post("/reward/add_reward_to_user", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == "This user not in this club"



def test_get_users_by_reward_good():
    response = client.get("/reward/get_users_by_reward", params={'reward_id': 1})
    assert response.status_code == 200 and len(response.json()['data']) == 1


async def test_get_users_by_reward_good_async(ac):
    response = await ac.get("/reward/get_users_by_reward", params={'reward_id': 2})
    assert response.status_code == 200 and len(response.json()['data']) == 1


def test_get_users_by_reward_reward_no_exist():
    response = client.get("/reward/get_users_by_reward", params={'reward_id': 100})
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"


async def test_get_users_by_reward_reward_no_exist_async(ac):
    response = await ac.get("/reward/get_users_by_reward", params={'reward_id': 100})
    assert response.status_code == 404 and response.json()['detail']['data'] == "Reward not found"


def test_get_reward_by_user_good():
    response = client.get("/reward/get_reward_by_user", params={'user_id': 49})
    assert response.status_code == 200 and len(response.json()['data']) == 1


async def test_get_reward_by_user_good_async(ac):
    response = await ac.get("/reward/get_reward_by_user", params={'user_id': 42})
    assert response.status_code == 200 and len(response.json()['data']) == 1


def test_get_reward_by_user_user_no_exist():
    response = client.get("/reward/get_reward_by_user", params={'user_id': 100})
    assert response.status_code == 404 and response.json()['detail']['data'] == "User not found"


async def test_get_reward_by_user_user_no_exist_async(ac):
    response = await ac.get("/reward/get_reward_by_user", params={'user_id': 100})
    assert response.status_code == 404 and response.json()['detail']['data'] == "User not found"






