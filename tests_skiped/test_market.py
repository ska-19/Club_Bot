import datetime

import pytest
from sqlalchemy import insert, select

from src.user_profile.models import user
from conftest import client, async_session_maker_test, ac

def create(a, b):
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


def delete(a, clubs_id):
    for i in clubs_id:
        response = client.delete("/club/delete_club/", params={"club_id": i})
        assert response.status_code == 200
    for i in range(1, a+1):
        response = client.delete("/user_profile/delete_user/", params={"user_id": i})
        assert response.status_code == 200






def test_add_product_good():
    clubs_id = create(1,1)
    club_id = clubs_id[0]
    data = {
        "name": "test_product",
        "price": 993,
        "user_id": 1,
        "description": "string",
        "quantity": 1,
        "club_id": club_id
    }

    response = client.post("/market/add_product", json=data)
    assert response.status_code == 200
    assert response.json()['data']['name'] == "test_product"

    product_id = response.json()['data']['id']

    response = client.get("/market/get_product", params={"product_id": product_id})
    assert response.status_code == 200

    delete(1, clubs_id)










