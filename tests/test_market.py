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






# def test_add_product_good():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#     assert response.json()['data']['name'] == "test_product"
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_add_product_good_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#     assert response.json()['data']['name'] == "test_product"
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_add_product_no_user_exist():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 2,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "User not found"
#
#     delete(1, clubs_id)
#
#
# async def test_add_product_no_user_exist_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 2,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "User not found"
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_add_product_no_club_exist():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": -1
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Club not found"
#
#     delete(1, clubs_id)
#
#
# async def test_add_product_no_club_exist_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": -1
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Club not found"
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_add_product_user_no_in_club():
#     clubs_id = create(2,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 2,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "This user not in this club"
#
#     delete(2, clubs_id)
#
#
# async def test_add_product_user_no_in_club_async(ac):
#     clubs_id = await acreate(2,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 2,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "This user not in this club"
#
#     await adelete(2, clubs_id, ac)
#
#
# def test_update_product_good():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     data = {
#         "id": product_id,
#         "user_id": 1,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = client.post("/market/update_product", json=data)
#     assert response.status_code == 200
#     assert response.json()['data']['name'] == "test_product_upd"
#     assert response.json()['data']['price'] == 11
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_update_product_good_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     data = {
#         "id": product_id,
#         "user_id": 1,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = await ac.post("/market/update_product", json=data)
#     assert response.status_code == 200
#     assert response.json()['data']['name'] == "test_product_upd"
#     assert response.json()['data']['price'] == 11
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_update_product_no_user_exist():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     data = {
#         "id": product_id,
#         "user_id": 2,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = client.post("/market/update_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "User not found"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_update_product_no_user_exist_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     data = {
#         "id": product_id,
#         "user_id": 2,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = await ac.post("/market/update_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "User not found"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_update_product_user_not_in_club():
#     clubs_id = create(2,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     data = {
#         "id": product_id,
#         "user_id": 2,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = client.post("/market/update_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "This user not in this club"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(2, clubs_id)
#
#
# async def test_update_product_user_not_in_club_async(ac):
#     clubs_id = await acreate(2,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     data = {
#         "id": product_id,
#         "user_id": 2,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = await ac.post("/market/update_product", json=data)
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "This user not in this club"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(2, clubs_id, ac)
#
#
# def test_update_product_no_product_exist():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "id": 1,
#         "user_id": 1,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = client.post("/market/update_product", json=data)
#     assert response.status_code == 404
#
#
#     delete(1, clubs_id)
#
#
# async def test_update_product_no_product_exist_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "id": 1,
#         "user_id": 1,
#         "name": "test_product_upd",
#         "price": 11,
#         "description": "string",
#         "quantity": 1
#     }
#
#     response = await ac.post("/market/update_product", json=data)
#     assert response.status_code == 404
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_get_product_good():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.get("/market/get_product", params={"product_id": product_id})
#     assert response.status_code == 200
#     assert response.json()['data']['name'] == "test_product"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_get_product_good_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.get("/market/get_product", params={"product_id": product_id})
#     assert response.status_code == 200
#     assert response.json()['data']['name'] == "test_product"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_get_product_no_product_exist():
#     response = client.get("/market/get_product", params={"product_id": 1})
#     assert response.status_code == 404
#
#
# async def test_get_product_no_product_exist_async(ac):
#     response = await ac.get("/market/get_product", params={"product_id": 1})
#     assert response.status_code == 404
#
#
# def test_buy_product_good():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.get("/market/get_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     quantity_prev = response.json()['data']['quantity']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.get("/market/get_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     quantity_after = response.json()['data']['quantity']
#
#     assert quantity_after == quantity_prev - 1
#
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_buy_product_good_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.get("/market/get_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     quantity_prev = response.json()['data']['quantity']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.get("/market/get_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     quantity_after = response.json()['data']['quantity']
#
#     assert quantity_after == quantity_prev - 1
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_buy_product_user_no_exist():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 2})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "User not found"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_buy_product_user_no_exist_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 2})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "User not found"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_buy_product_no_product_exist():
#     response = client.post("/market/buy_product", params={"product_id": 1, "user_id": 1})
#     assert response.status_code == 404
#
#
# async def test_buy_product_no_product_exist_async(ac):
#     response = await ac.post("/market/buy_product", params={"product_id": 1, "user_id": 1})
#     assert response.status_code == 404
#
#
# def test_buy_product_no_money():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "User balance is not enough"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_buy_product_no_money_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 993,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "User balance is not enough"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_accept_request_good():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#     print(product_id)
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_accept_request_good_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#     print(product_id)
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_accept_request_no_req():
#     clubs_id = create(2,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Request not found"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(2, clubs_id)
#
#
# async def test_accept_request_no_req_async(ac):
#     clubs_id = await acreate(2,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Request not found"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(2, clubs_id, ac)
#
#
# def test_accept_request_was_solved():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "Forbidden"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_accept_request_was_solved_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "Forbidden"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_reject_request_admin():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.post("/market/reject_request_admin", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_reject_request_admin_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/reject_request_admin", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_reject_request_no_req():
#     clubs_id = create(2,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/reject_request_admin", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Request not found"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(2, clubs_id)
#
#
# async def test_reject_request_no_req_async(ac):
#     clubs_id = await acreate(2,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/reject_request_admin", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Request not found"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(2, clubs_id, ac)
#
#
# def test_reject_request_was_solved():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = client.post("/market/reject_request_admin", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "Forbidden"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_reject_request_was_solved_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/reject_request_admin", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "Forbidden"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_reject_request_user():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.post("/market/reject_request_user", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_reject_request_user_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/reject_request_user", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_reject_request_user_no_req():
#     clubs_id = create(2,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/reject_request_user", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Request not found"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(2, clubs_id)
#
#
# async def test_reject_request_user_no_req_async(ac):
#     clubs_id = await acreate(2,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/reject_request_user", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 404
#     assert response.json()['detail']['data'] == "Request not found"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(2, clubs_id, ac)
#
#
# def test_reject_request_user_was_solved():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = client.post("/market/reject_request_user", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "Forbidden"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)
#
#
# async def test_reject_request_user_was_solved_async(ac):
#     clubs_id = await acreate(1,1, ac)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = await ac.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = await ac.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/accept_request", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 200
#
#     response = await ac.post("/market/reject_request_user", params={"admin_id": 1, "user_id": 1, "product_id": product_id})
#     assert response.status_code == 403
#     assert response.json()['detail']['data'] == "Forbidden"
#
#     response = await ac.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     await adelete(1, clubs_id, ac)
#
#
# def test_get_items_by_club():
#     clubs_id = create(1,1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.get("/market/get_item_by_club", params={"club_id": club_id})
#     assert response.status_code == 200
#     assert response.json()['data'][0]['name'] == "test_product"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)


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


# def test_get_admin_history_active():
#     clubs_id = create(1, 1)
#     club_id = clubs_id[0]
#
#     data = {
#         "name": "test_product",
#         "price": 0,
#         "user_id": 1,
#         "description": "string",
#         "quantity": 1,
#         "club_id": club_id
#     }
#
#     response = client.post("/market/add_product", json=data)
#     assert response.status_code == 200
#
#     product_id = response.json()['data']['id']
#
#     response = client.post("/market/buy_product", params={"product_id": product_id, "user_id": 1})
#     assert response.status_code == 200
#
#     response = client.get("/market/get_admin_history_active", params={"club_id": 1})
#     assert response.status_code == 200
#     assert len(response.json()['data']) == 1
#     assert response.json()['data'][0]['name'] == "test_product"
#
#     response = client.post("/market/delete_product", params={"product_id": product_id})
#     assert response.status_code == 200
#
#     delete(1, clubs_id)




