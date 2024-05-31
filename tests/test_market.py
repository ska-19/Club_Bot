import datetime
from typing import List, AsyncGenerator

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac


def create(a: int, b: int):
    for i in range(1, a+1):
        data = {
            "id": i,
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

    clubs = []
    for i in range(1, b+1):
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
        clubs.append(response.json()['data']['id'])

    return clubs


def delete(a: int, clubs_id: List[int]):
    for i in clubs_id:
        response = client.post("/club/delete_club", params={"club_id": i})
        assert response.status_code == 200
    for i in range(1, a+1):
        response = client.post("/user_profile/delete_user", params={"user_id": i})
        assert response.status_code == 200


async def acreate(a: int, b: int, ac: AsyncGenerator):
    for i in range(1, a+1):
        data = {
            "id": i,
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

    clubs = []
    for i in range(1, b+1):
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
        clubs.append(response.json()['data']['id'])

    return clubs

async def adelete(a: int, clubs_id: List[int], ac: AsyncGenerator):
    for i in clubs_id:
        response = await ac.post("/club/delete_club", params={"club_id": i})
        assert response.status_code == 200
    for i in range(1, a+1):
        response = await ac.post("/user_profile/delete_user", params={"user_id": i})
        assert response.status_code == 200










async def test_get_items_by_club_async(ac):
    clubs_id = await acreate(1,1, ac)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = await ac.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = await ac.get("/market/get_item_by_club", params={"club_id": club_id})
    assert response.status_code == 200
    assert response.json()['data'][0]['name'] == "test_product"

    response = await ac.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    await adelete(1, clubs_id, ac)


def test_get_items_by_club_no_exist():
    response = client.get("/market/get_item_by_club", params={"club_id": 1})
    assert response.status_code == 404


async def test_get_items_by_club_no_exist_async(ac):
    response = await ac.get("/market/get_item_by_club", params={"club_id": 1})
    assert response.status_code == 404



def test_get_user_history_active():
    clubs_id = create(1,1)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = client.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = client.get("/market/get_user_history_active", params={"user_id": 1})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"

    response = client.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    delete(1, clubs_id)


async def test_get_user_history_active_async(ac):
    clubs_id = await acreate(1, 1, ac)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = await ac.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/market/get_user_history_active", params={"user_id": 1})
    assert response.status_code == 200

    assert response.json()['data'][0]['name'] == "test_product"

    response = await ac.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    await adelete(1, clubs_id, ac)


def test_get_user_history_close():
    clubs_id = create(1, 1)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = client.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
    assert response.status_code == 200

    response = client.get("/market/get_user_history_close", params={"user_id": 1})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"


    response = client.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    delete(1, clubs_id)


async def test_get_user_history_close_async(ac):
    clubs_id = await acreate(1, 1, ac)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = await ac.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
    assert response.status_code == 200

    response = await ac.get("/market/get_user_history_close", params={"user_id": 1})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"

    response = await ac.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    await adelete(1, clubs_id, ac)


def test_get_admin_history_active():
    clubs_id = create(1, 1)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = client.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = client.get("/market/get_admin_history_active", params={"club_id": club_id})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"

    response = client.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    delete(1, clubs_id)


async def test_get_admin_history_active_async(ac):
    clubs_id = await acreate(1, 1, ac)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = await ac.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/market/get_admin_history_active", params={"club_id": club_id})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"

    response = await ac.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    await adelete(1, clubs_id, ac)


def test_get_admin_history_close():
    clubs_id = create(1, 1)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = client.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
    assert response.status_code == 200

    response = client.get("/market/get_admin_history_close", params={"club_id": club_id})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"

    response = client.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    delete(1, clubs_id)


async def test_get_admin_history_close_async(ac):
    clubs_id = await acreate(1, 1, ac)
    club_id = clubs_id[0]

    data = {
        "name": "test_product",
        "price": 0,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = await ac.post("/market/add_product", json=data)
    assert response.status_code == 200

    product_id = response.json()['data']['id']

    response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
    assert response.status_code == 200

    response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
    assert response.status_code == 200

    response = await ac.get("/market/get_admin_history_close", params={"club_id": club_id})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == "test_product"

    response = await ac.post("/market/delete_product", params={"product_id": product_id})
    assert response.status_code == 200

    await adelete(1, clubs_id, ac)













