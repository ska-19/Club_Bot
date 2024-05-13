import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac

def test_create_user_good():
    data = {
        "id": 1,
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


async def test_create_user_good_async(ac):
    data = {
        "id": 2,
        "username": "test_async",
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

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 200


def test_create_user_same_id():
    data = {
        "id": 1,
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
    assert response.status_code == 409


async def test_create_user_same_id_async(ac):
    data = {
        "id": 2,
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

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 409


def test_create_user_without_id():  # TODO: падает, уточнить у тимоши должно ли так быть
    data = {
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
    assert response.status_code == 422


async def test_create_user_without_id_async(ac):
    data = {
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
    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 422


def test_create_user_bad():
    data = {
        "id": 'zxc',
        "username": 1,
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
    assert response.status_code == 422


async def test_create_user_bad_async(ac):
    data = {
        "id": 'zxc',
        "username": 2,
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
    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 422


def test_get_user_good():
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 200


async def test_get_user_good_async(ac):
    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 200


def test_get_user_no_id_exist():
    response = client.get("/user_profile/get_user", params={"user_id": 3})
    assert response.status_code == 404


async def test_get_user_no_id_exist_async(ac):
    response = await ac.get("/user_profile/get_user", params={"user_id": 4})
    assert response.status_code == 404


def test_get_user_without_id_exist():
    response = client.get("/user_profile/get_user", params={})
    assert response.status_code == 422


async def test_get_user_without_id_async(ac):
    response = await ac.get("/user_profile/get_user", params={})
    assert response.status_code == 422


def test_get_user_bad():
    response = client.get("/user_profile/get_user", params={"user_id": 'zxc'})
    assert response.status_code == 422


async def test_get_user_bad_async(ac):
    response = await ac.get("/user_profile/get_user", params={"user_id": 'zxc'})
    assert response.status_code == 422


def test_get_attrs_good():
    response = client.get("/user_profile/get_attr", params={"user_id": 1, 'col': 'username'})
    assert response.status_code == 200 and response.json()['data'] == 'test'


async def test_get_attrs_good_async(ac):
    response = await ac.get("/user_profile/get_attr", params={"user_id": 2, 'col': 'username'})
    assert response.status_code == 200 and response.json()['data'] == 'test_async'


def test_get_attrs_no_id_exist():
    response = client.get("/user_profile/get_attr", params={"user_id": 3, 'col': 'username'})
    assert response.status_code == 404


async def test_get_attrs_no_id_exist_async(ac):
    response = await ac.get("/user_profile/get_attr", params={"user_id": 4, 'col': 'username'})
    assert response.status_code == 404


def test_get_attrs_without_id():
    response = client.get("/user_profile/get_attr", params={'col': 'username'})
    assert response.status_code == 422


async def test_get_attrs_without_id_async(ac):
    response = await ac.get("/user_profile/get_attr", params={'col': 'username'})
    assert response.status_code == 422


def test_get_attrs_no_col_exist():  # TODO: мб добавить отдельную ошибку что колонка с таким именем существует
    response = client.get("/user_profile/get_attr", params={"user_id": 1, 'col': 'zxc'})
    assert response.status_code == 422


async def test_get_attrs_no_col_exist_async(ac):
    response = await ac.get("/user_profile/get_attr", params={"user_id": 2, 'col': 'zxc'})
    assert response.status_code == 422


def test_get_attrs_without_col():
    response = client.get("/user_profile/get_attr", params={"user_id": 1})
    assert response.status_code == 422


async def test_get_attrs_without_col_async(ac):
    response = await ac.get("/user_profile/get_attr", params={"user_id": 2})
    assert response.status_code == 422


def test_get_attrs_bad():
    response = client.get("/user_profile/get_attr", params={"user_id": 'zxc', 'col': 'username'})
    assert response.status_code == 422


async def test_get_attrs_bad_async(ac):
    response = await ac.get("/user_profile/get_attr", params={"user_id": 'zxc', 'col': 'username'})
    assert response.status_code == 422


def test_update_user_good():  # TODO: возможно еррор
    data = {
        "name": "updated",
        "surname": "updated",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 1, 'update_data': data})
    assert response.status_code == 200 and response.json()['data']['username'] == 'test_update'


async def test_update_user_good_async(ac):
    data = {
        "name": "updated_async",
        "surname": "updated_async",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = await ac.post("/user_profile/update_user", params={"user_id": 2, 'update_data': data})
    assert response.status_code == 200 and response.json()['data']['username'] == 'test_update_async'


def test_update_user_no_id_exist():
    data = {
        "name": "updated",
        "surname": "updated",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 3, 'update_data': data})
    assert response.status_code == 404


async def test_update_user_no_id_exist_async(ac):
    data = {
        "name": "updated_async",
        "surname": "updated_async",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = await ac.post("/user_profile/update_user", params={"user_id": 4, 'update_data': data})
    assert response.status_code == 404


def test_update_user_without_id():
    data = {
        "name": "updated",
        "surname": "updated",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = client.post("/user_profile/update_user", params={'update_data': data})
    assert response.status_code == 422


async def test_update_user_without_id_async(ac):
    data = {
        "name": "updated_async",
        "surname": "updated_async",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = await ac.post("/user_profile/update_user", params={'update_data': data})
    assert response.status_code == 422


def test_update_user_bad():
    data = {
        "name": "updated",
        "surname": "updated",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 'zxc', 'update_data': data})
    assert response.status_code == 422


async def test_update_user_bad_async(ac):
    data = {
        "name": "updated_async",
        "surname": "updated_async",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    print(datetime.datetime.utcnow())
    response = await ac.post("/user_profile/update_user", params={"user_id": 'zxc', 'update_data': data})
    assert response.status_code == 422


def test_update_user_no_col_exist():
    data = {
        "zxc": "updated",
        "name": "updated",
        "surname": "updated",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 1, 'update_data': data})
    assert response.status_code == 422


async def test_update_user_no_col_exist_async(ac):
    data = {
        "zxc": "updated_async",
        "name": "updated_async",
        "surname": "updated_async",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = await ac.post("/user_profile/update_user", params={"user_id": 2, 'update_data': data})
    assert response.status_code == 422


def test_update_user_without_col():
    data = {
        "surname": "updated",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 1, 'update_data': data})
    assert response.status_code == 422


async def test_update_user_without_col_async(ac):
    data = {
        "surname": "updated_async",
        "email": "string",
        "tel": "string",
        "photo": "string",
        "comfort_time": "string",
        "course": "string",
        "faculty": "string",
        "links": "string",
        "bio": "string",
        "dob": datetime.datetime.utcnow(),
        "city": "string",
        "education": "string",
    }
    response = await ac.post("/user_profile/update_user", params={"user_id": 2, 'update_data': data})
    assert response.status_code == 422


def test_update_xp_good():
    response = client.post("/user_profile/update_xp", params={"user_id": 1, 'update_xp': 1})
    assert response.status_code == 200 and response.json()['data']['xp'] == 1


async def test_update_xp_good_async(ac):
    response = await ac.post("/user_profile/update_xp", params={"user_id": 2, 'update_xp': 1})
    assert response.status_code == 200 and response.json()['data']['xp'] == 1


def test_update_xp_no_id_exist():
    response = client.post("/user_profile/update_xp", params={"user_id": 3, 'update_xp': 1})
    assert response.status_code == 404


async def test_update_xp_no_id_exist_async(ac):
    response = await ac.post("/user_profile/update_xp", params={"user_id": 4, 'update_xp': 1})
    assert response.status_code == 404


def test_update_xp_without_id():
    response = client.post("/user_profile/update_xp", params={'update_xp': 1})
    assert response.status_code == 422


async def test_update_xp_without_id_async(ac):
    response = await ac.post("/user_profile/update_xp", params={'update_xp': 1})
    assert response.status_code == 422


def test_update_xp_bad():
    response = client.post("/user_profile/update_xp", params={"user_id": 'zxc', 'update_xp': 1})
    assert response.status_code == 422


async def test_update_xp_bad_async(ac):
    response = await ac.post("/user_profile/update_xp", params={"user_id": 'zxc', 'update_xp': 1})
    assert response.status_code == 422


def test_update_ach_good(): #TODO: надо чекнуть
    response = client.post("/user_profile/update_achievment", params={"user_id": 1, 'achievment': 'first'})
    assert response.status_code == 200 and response.json()['data']['first'] == 1


async def test_update_ach_good_async(ac):
    response = await ac.post("/user_profile/update_achievment", params={"user_id": 2, 'achievment': 'first'})
    assert response.status_code == 200 and response.json()['data']['first'] == 1


def test_update_ach_no_id_exist():
    response = client.post("/user_profile/update_achievment", params={"user_id": 3, 'achievment': 'first'})
    assert response.status_code == 404


async def test_update_ach_no_id_exist_async(ac):
    response = await ac.post("/user_profile/update_achievment", params={"user_id": 4, 'achievment': 'first'})
    assert response.status_code == 404


def test_update_ach_without_id():
    response = client.post("/user_profile/update_achievment", params={'achievment': 'first'})
    assert response.status_code == 422


async def test_update_ach_without_id_async(ac):
    response = await ac.post("/user_profile/update_achievment", params={'achievment': 'first'})
    assert response.status_code == 422



def test_update_ach_bad():
    response = client.post("/user_profile/update_achievment", params={"user_id": 'zxc', 'achievment': 'first'})
    assert response.status_code == 422


async def test_update_ach_bad_async(ac):
    response = await ac.post("/user_profile/update_achievment", params={"user_id": 'zxc', 'achievmnet': 'first'})
    assert response.status_code == 422



