import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac

def test_create_userr():
    data = {
        "id": 20,
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
        "id": 28,
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
        "id": 29,
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
        "id": 22,
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


def test_create_club():
    data = {
        "owner": 20,
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


def test_join_club_good():
    data = {
        "club_id": 1,
        "user_id": 28,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)
    print(response.json())
    assert response.status_code == 200


async def test_join_club_good_async(ac):
    data = {
        "club_id": 1,
        "user_id": 29,
        "role": "member",
        "balance": 0
    }
    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200


def test_join_club_user_no_exist():
    data = {
        "club_id": 1,
        "user_id": 21,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)
    assert response.status_code == 404


async def test_join_club_user_no_exist_async(ac):
    data = {
        "club_id": 1,
        "user_id": 21,
        "role": "member",
        "balance": 0
    }
    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 404


def test_join_club_club_no_exist():
    data = {
        "club_id": 2,
        "user_id": 21,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)
    assert response.status_code == 404


async def test_join_club_club_no_exist_async(ac):
    data = {
        "club_id": 2,
        "user_id": 21,
        "role": "member",
        "balance": 0
    }
    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 404


def test_join_club_user_rec():
    data = {
        "club_id": 1,
        "user_id": 28,
        "role": "member",
        "balance": 0
    }
    response = client.post("/join/join_club", json=data)
    assert response.status_code == 409


async def test_join_club_user_rec_async(ac):
    data = {
        "club_id": 1,
        "user_id": 28,
        "role": "member",
        "balance": 0
    }
    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 409


def test_get_balance_good():
    response = client.get("/join/get_balance", params={"club_id": 1, "user_id": 28})
    assert response.status_code == 200
    assert response.json()['data'] == 0


async def test_get_balance_good_async(ac):
    response = await ac.get("/join/get_balance", params={"club_id": 1, "user_id": 28})
    assert response.status_code == 200
    assert response.json()['data'] == 0


def test_get_balance_user_no_exist():
    response = client.get("/join/get_balance", params={"club_id": 1, "user_id": 21})
    assert response.status_code == 404



async def test_get_balance_user_no_exist_async(ac):
    response = await ac.get("/join/get_balance", params={"club_id": 1, "user_id": 21})
    assert response.status_code == 404


def test_get_balance_club_no_exist():
    response = client.get("/join/get_balance", params={"club_id": 2, "user_id": 21})
    assert response.status_code == 404


async def test_get_balance_club_no_exist_async(ac):
    response = await ac.get("/join/get_balance", params={"club_id": 2, "user_id": 21})
    assert response.status_code == 404


def test_get_balance_user_no_rec():
    response = client.get("/join/get_balance", params={"club_id": 1, "user_id": 22})
    print(response.json())
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


async def test_get_balance_user_no_rec_async(ac):
    response = await ac.get("/join/get_balance", params={"club_id": 1, "user_id": 22})
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


def test_update_balance_good():
    data = {
        "club_id": 1,
        "user_id": 28,
        "plus_balance": 10
    }
    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 200
    response = client.get("/join/get_balance", params={"club_id": 1, "user_id": 28})
    assert response.json()['data'] == 10


async def test_update_balance_good_async(ac):
    data = {
        "club_id": 1,
        "user_id": 29,
        "plus_balance": 10
    }
    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 200
    response = await ac.get("/join/get_balance", params={"club_id": 1, "user_id": 29})
    assert response.json()['data'] == 10


def test_update_balance_user_no_exist():
    data = {
        "club_id": 1,
        "user_id": 21,
        "plus_balance": 10
    }
    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 404


async def test_update_balance_user_no_exist_async(ac):
    data = {
        "club_id": 1,
        "user_id": 21,
        "plus_balance": 10
    }
    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 404


def test_update_balance_club_no_exist():
    data = {
        "club_id": 2,
        "user_id": 21,
        "plus_balance": 10
    }
    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 404


async def test_update_balance_club_no_exist_async(ac):
    data = {
        "club_id": 2,
        "user_id": 21,
        "plus_balance": 10
    }
    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 404


def test_update_balance_user_no_rec():
    data = {
        "club_id": 1,
        "user_id": 22,
        "plus_balance": 10
    }
    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


async def test_update_balance_user_no_rec_async(ac):
    data = {
        "club_id": 1,
        "user_id": 22,
        "plus_balance": 10
    }
    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


from src.user_club.inner_func import get_role

def test_update_role_good(): #TODO: Я бы гет_рол сделал видимой +  надо чекнуть почему 500
    data = {
        "club_id": 1,
        "user_id": 28,
        "new_role": "admin"
    }
    response = client.post("/join/role_update", json=data)
    assert response.status_code == 200


async def test_update_role_good_async(ac):
    data = {
        "club_id": 1,
        "user_id": 29,
        "new_role": "admin"
    }
    response = await ac.post("/join/role_update", json=data)
    assert response.status_code == 200



def test_update_role_user_no_exist():
    data = {
        "club_id": 1,
        "user_id": 21,
        "new_role": "admin"
    }
    response = client.post("/join/role_update", json=data)
    assert response.status_code == 404


async def test_update_role_user_no_exist_async(ac):
    data = {
        "club_id": 1,
        "user_id": 21,
        "new_role": "admin"
    }
    response = await ac.post("/join/role_update", json=data)
    assert response.status_code == 404


def test_update_role_club_no_exist():
    data = {
        "club_id": 2,
        "user_id": 21,
        "new_role": "admin"
    }
    response = client.post("/join/role_update", json=data)
    assert response.status_code == 404


async def test_update_role_club_no_exist_async(ac):
    data = {
        "club_id": 2,
        "user_id": 21,
        "new_role": "admin"
    }
    response = await ac.post("/join/role_update", json=data)
    assert response.status_code == 404


def test_update_role_user_no_rec():
    data = {
        "club_id": 1,
        "user_id": 22,
        "new_role": "admin"
    }
    response = client.post("/join/role_update", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'



async def test_update_role_user_no_rec_async(ac):
    data = {
        "club_id": 1,
        "user_id": 22,
        "new_role": "admin"
    }
    response = await ac.post("/join/role_update", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'



def test_get_users_in_club_good():
    response = client.get("/join/get_users_in_club", params={"club_id": 1})
    print(response.json())
    assert response.status_code == 200 and response.json()['data'][0]['username'] == 'test' and response.json()['data'][0]['role'] == 'owner' and response.json()['data'][1]['username'] == 'test' and response.json()['data'][1]['role'] == 'member'



async def test_get_users_in_club_good_async(ac):
    response = await ac.get("/join/get_users_in_club", params={"club_id": 1})
    assert response.status_code == 200 and response.json()['data'][0]['username'] == 'test' and response.json()['data'][0]['role'] == 'owner' and response.json()['data'][1]['username'] == 'test' and response.json()['data'][1]['role'] == 'member'


def test_get_users_in_club_club_no_exist():
    response = client.get("/join/get_users_in_club", params={"club_id": 2})
    assert response.status_code == 404


async def test_get_users_in_club_club_no_exist_async(ac):
    response = await ac.get("/join/get_users_in_club", params={"club_id": 2})
    assert response.status_code == 404


def test_get_users_with_role_good():
    response = client.get("/join/get_users_with_role", params={"club_id": 1, "role": "member"})
    print(response.json())
    assert response.status_code == 200 and response.json()['data'][0]['username'] == 'test'


async def test_get_users_with_role_good_async(ac):
    response = await ac.get("/join/get_users_with_role", params={"club_id": 1, "role": "member"})
    assert response.status_code == 200 and response.json()['data'][0]['username'] == 'test'


def test_get_users_with_role_club_no_exist():
    response = client.get("/join/get_users_with_role", params={"club_id": 2, "role": "member"})
    assert response.status_code == 404


async def test_get_users_with_role_club_no_exist_async(ac):
    response = await ac.get("/join/get_users_with_role", params={"club_id": 2, "role": "member"})
    assert response.status_code == 404


def test_get_users_with_role_role_no_exist():
    response = client.get("/join/get_users_with_role", params={"club_id": 1, "role": "admin"})
    assert response.status_code == 404


async def test_get_users_with_role_role_no_exist_async(ac):
    response = await ac.get("/join/get_users_with_role", params={"club_id": 1, "role": "admin"})
    assert response.status_code == 404


def test_get_clubs_user_good():
    response = client.get("/join/get_clubs_by_user", params={"user_id": 28})
    assert response.status_code == 200 and response.json()['data'][0]['name'] == 'test_club'


async def test_get_clubs_user_good_async(ac):
    response = await ac.get("/join/get_clubs_by_user", params={"user_id": 29})
    assert response.status_code == 200 and response.json()['data'][0]['name'] == 'test_club'


def test_get_clubs_user_no_exist():
    response = client.get("/join/get_clubs_by_user", params={"user_id": 21})
    assert response.status_code == 404


async def test_get_clubs_user_no_exist_async(ac):
    response = await ac.get("/join/get_clubs_by_user", params={"user_id": 21})
    assert response.status_code == 404


def test_disjoin_club_good():
    data = {
        "club_id": 1,
        "user_id": 28
    }
    response = client.post("/join/disjoin_club", json=data)
    assert response.status_code == 200


async def test_disjoin_club_good_async(ac):
    data = {
        "club_id": 1,
        "user_id": 29
    }
    response = await ac.post("/join/disjoin_club", json=data)
    assert response.status_code == 200


def test_disjoin_club_user_no_exist():
    data = {
        "club_id": 1,
        "user_id": 21
    }
    response = client.post("/join/disjoin_club", json=data)
    assert response.status_code == 404



async def test_disjoin_club_user_no_exist_async(ac):
    data = {
        "club_id": 1,
        "user_id": 21
    }
    response = await ac.post("/join/disjoin_club", json=data)
    assert response.status_code == 404


def test_disjoin_club_club_no_exist():
    data = {
        "club_id": 2,
        "user_id": 21
    }
    response = client.post("/join/disjoin_club", json=data)
    assert response.status_code == 404


async def test_disjoin_club_club_no_exist_async(ac):
    data = {
        "club_id": 2,
        "user_id": 21
    }
    response = await ac.post("/join/disjoin_club", json=data)
    assert response.status_code == 404


def test_disjoin_club_user_no_rec():
    data = {
        "club_id": 1,
        "user_id": 22
    }
    response = client.post("/join/disjoin_club", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'


async def test_disjoin_club_user_no_rec_async(ac):
    data = {
        "club_id": 1,
        "user_id": 22
    }
    response = await ac.post("/join/disjoin_club", json=data)
    assert response.status_code == 404 and response.json()['detail']['data'] == 'This user not in this club'






















