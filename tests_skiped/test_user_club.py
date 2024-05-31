from tests.conftest import client, ac



def test_join_to_the_club_good():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 0
    }


    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

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


async def test_join_to_the_club_async(ac):
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 0
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200
    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_join_to_the_club_no_exist():
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
        "id": 2,
        "username": "test2",
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
        "club_id": -1,
        "user_id": 2,
        "role": "member",
        "balance": 0
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 404

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



async def test_join_to_the_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": -1,
        "user_id": 2,
        "role": "member",
        "balance": 0
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404




def test_join_to_the_club_user_no_exist():
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 0
    }

    response = client.post("/club/join_to_the_club", json=data)
    assert response.status_code == 404

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_join_to_the_club_user_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 0
    }

    response = await ac.post("/club/join_to_the_club", json=data)
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


def test_get_balance_good():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.get("/join/get_balance", params={"club_id": club_id, "user_id": 2})
    assert response.status_code == 200
    assert response.json()['data'] == 993

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


async def test_get_balance_good_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.get("/join/get_balance", params={"club_id": club_id, "user_id": 2})
    assert response.status_code == 200
    assert response.json()['data'] == 993

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404



def test_get_balance_user_no_exist():
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

    response = client.get("/join/get_balance", params={"club_id": club_id, "user_id": 2})
    assert response.status_code == 404

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404



async def test_get_balance_user_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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

    club_id = response.json()['data']['id']

    response = await ac.get("/join/get_balance", params={"club_id": club_id, "user_id": 2})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


def test_get_balance_club_no_exist():
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

    response = client.get("/join/get_balance", params={"club_id": -1, "user_id": 1})
    assert response.status_code == 404

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404



async def test_get_balance_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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

    club_id = response.json()['data']['id']

    response = await ac.get("/join/get_balance", params={"club_id": -1, "user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404



def test_disjoin_club_good():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.post("/join/disjoin_club", json={"club_id": club_id, "user_id": 2})
    assert response.status_code == 200

    response = client.get("/join/get_users_in_club", params={"club_id": club_id})
    assert response.status_code == 200

    print(response.json()['data'])

    for usr in response.json()['data']:
        assert usr['id'] != 2

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


async def test_disjoin_club_good_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.post("/join/disjoin_club", json={"club_id": club_id, "user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/join/get_users_in_club", params={"club_id": club_id})
    assert response.status_code == 200

    print(response.json()['data'])

    for usr in response.json()['data']:
        assert usr['id'] != 2

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404



def test_disjoin_club_user_no_in_club():
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
        "id": 2,
        "username": "test2",
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

    response = client.post("/join/disjoin_club", json={"club_id": club_id, "user_id": 2})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "This user not in this club"


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


async def test_disjoin_club_user_no_in_club_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    response = await ac.post("/join/disjoin_club", json={"club_id": club_id, "user_id": 2})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "This user not in this club"


    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_disjoin_club_no_exist():
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
        "id": 2,
        "username": "test2",
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

    response = client.post("/join/disjoin_club", json={"club_id": -1, "user_id": 2})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "Club not found"

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


async def test_disjoin_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    response = await ac.post("/join/disjoin_club", json={"club_id": -1, "user_id": 2})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "Club not found"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_disjoin_club_user_no_exist():
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

    response = client.post("/join/disjoin_club", json={"club_id": club_id, "user_id": 2})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_disjoin_club_user_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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

    club_id = response.json()['data']['id']

    response = await ac.post("/join/disjoin_club", json={"club_id": club_id, "user_id": 2})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


def test_role_update():
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
        "id": 2,
        "username": "test2_async",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.post("/join/role_update", params={"user_id": 2, "club_id": club_id})
    if response.status_code != 200:
        #print(response.json())
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

    assert response.status_code == 200

    # response = client.get("/join/get_users_with_role", params={"club_id": club_id, "role": "admin"})
    # assert response.status_code == 200
    # print(response.json())
    #
    # for usr in response.json()['data']:
    #     if usr['id'] == 2:
    #         assert usr['role'] == "admin"

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


async def test_role_update_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "club_id": club_id,
        "user_id": 2,
        "new_role": "admin",
    }

    response = await ac.post("/join/role_update", params={"user_id": 2, "club_id": club_id})
    if response.status_code != 200:
        response = await ac.post("/club/delete_club", params={"club_id": club_id})
        assert response.status_code == 200

        response = await ac.get("/club/get_club", params={"club_id": club_id})
        assert response.status_code == 404

        response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
        assert response.status_code == 200

        response = await ac.get("/user_profile/get_user", params={"user_id": 1})
        assert response.status_code == 404

        response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
        assert response.status_code == 200

        response = await ac.get("/user_profile/get_user", params={"user_id": 2})
        assert response.status_code == 404

    assert response.status_code == 200

    # response = await ac.get("/join/get_users_with_role", params={"club_id": club_id, "role": "admin"})
    # assert response.status_code == 200
    #
    # for usr in response.json()['data']:
    #     if usr['id'] == 2:
    #         assert usr['role'] == "admin"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_role_update_user_no_in_club():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "new_role": "admin",
    }

    response = client.post("/join/role_update", params={"user_id": 2, "club_id": club_id})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "This user not in this club"


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


async def test_role_update_user_no_in_club_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "new_role": "admin",
    }

    response = await ac.post("/join/role_update", params={"user_id": 2, "club_id": club_id})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "This user not in this club"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_role_update_user_no_exist():
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
        "club_id": club_id,
        "user_id": 2,
        "new_role": "admin",
    }

    response = client.post("/join/role_update", params={"user_id": 2, "club_id": club_id})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_role_update_user_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "new_role": "admin",
    }

    response = await ac.post("/join/role_update", params={"user_id": 2, "club_id": club_id})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


def test_role_update_club_no_exist():
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
        "id": 2,
        "username": "test2",
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
        "club_id": -1,
        "user_id": 2,
        "new_role": "admin",
    }

    response = client.post("/join/role_update", params={"user_id": 2, "club_id": -1})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "Club not found"

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


async def test_role_update_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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
        "club_id": -1,
        "user_id": 2,
        "new_role": "admin",
    }

    response = await ac.post("/join/role_update", params={"user_id": 2, "club_id": -1})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "Club not found"

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_update_balance():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "club_id": club_id,
        "user_id": 2,
        "plus_balance": -7,
    }

    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 200

    responce = client.get("/join/get_balance", params={"club_id": club_id, "user_id": 2})
    assert responce.status_code == 200
    assert responce.json()['data'] == 986

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


async def test_update_balance_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "club_id": club_id,
        "user_id": 2,
        "plus_balance": -7,
    }

    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 200

    responce = await ac.get("/join/get_balance", params={"club_id": club_id, "user_id": 2})
    assert responce.status_code == 200
    assert responce.json()['data'] == 986

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_update_balance_user_no_in_club():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "plus_balance": -7,
    }

    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "This user not in this club"

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


async def test_update_balance_user_no_in_club_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "plus_balance": -7,
    }

    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "This user not in this club"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_update_balance_user_no_exist():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 3,
        "plus_balance": -7,
    }

    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code


async def test_update_balance_user_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 3,
        "plus_balance": -7,
    }

    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200


def test_update_balance_club_no_exist():
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
        "id": 2,
        "username": "test2",
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
        "club_id": -1,
        "user_id": 2,
        "plus_balance": -7,
    }

    response = client.post("/join/update_balance", json=data)
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "Club not found"

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


async def test_update_balance_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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
        "club_id": -1,
        "user_id": 2,
        "plus_balance": -7,
    }

    response = await ac.post("/join/update_balance", json=data)
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "Club not found"

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_get_users_in_club_good():
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
        "id": 2,
        "username": "test2",
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.get("/join/get_users_in_club", params={"club_id": club_id})
    assert response.status_code == 200

    for usr in response.json()['data']:
        assert (usr['id'] == 1 or usr['id'] == 2)

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


async def test_get_users_in_club_good_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.get("/join/get_users_in_club", params={"club_id": club_id})
    assert response.status_code == 200

    for usr in response.json()['data']:
        assert (usr['id'] == 1 or usr['id'] == 2)

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_get_users_in_club_no_exist():
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
        "id": 2,
        "username": "test2",
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

    response = client.get("/join/get_users_in_club", params={"club_id": -1})
    assert response.status_code == 404

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


async def test_get_users_in_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    response = await ac.get("/join/get_users_in_club", params={"club_id": -1})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404



def test_get_usert_with_role_good():
    data = {
        "id": 1,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False,
    }

    response = client.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "id": 2,
        "username": "test2",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": False,
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.get("/join/get_users_with_role", params={"club_id": club_id, "role": "member"})
    assert response.status_code == 200
    print(response.json())
    assert response.json()['data'][0]['id'] == 2

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


async def test_get_users_with_role_good_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
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
        "id": 2,
        "username": "test2_async",
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.get("/join/get_users_with_role", params={"club_id": club_id, "role": "member"})
    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == 2

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_get_users_with_role_club_no_exist():
    data = {
        "id": 1,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False,
    }

    response = client.post("/user_profile/create_user", json=data)
    assert response.status_code == 200

    data = {
        "id": 2,
        "username": "test2",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": False,
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
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.get("/join/get_users_with_role", params={"club_id": -1, "role": "member"})
    assert response.status_code == 404

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


async def test_get_users_with_role_club_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False,
    }

    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 200


    data = {
        "id": 2,
        "username": "test2_async",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": False,
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

    club_id = response.json()['data']['id']

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.get("/join/get_users_with_role", params={"club_id": -1, "role": "member"})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 2})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 2})
    assert response.status_code == 404


def test_get_clubs_by_user():
    data = {
        "id": 1,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
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
        "owner": 1,
        "name": "test_club2",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-02"
    }

    response = client.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id2 = response.json()['data']['id']

    response = client.get("/join/get_clubs_by_user", params={"user_id": 1})
    assert response.status_code == 200

    for clubs in response.json()['data']:
        assert (clubs['id'] == club_id or clubs['id'] == club_id2)

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/club/delete_club", params={"club_id": club_id2})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id2})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_get_clubs_by_user_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
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

    club_id = response.json()['data']['id']

    data = {
        "owner": 1,
        "name": "test_club2_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-02"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id2 = response.json()['data']['id']

    response = await ac.get("/join/get_clubs_by_user", params={"user_id": 1})
    assert response.status_code == 200

    for clubs in response.json()['data']:
        assert (clubs['id'] == club_id or clubs['id'] == club_id2)

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id2})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id2})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


def test_get_clubs_by_user_no_exist():
    data = {
        "id": 1,
        "username": "test",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
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
        "owner": 1,
        "name": "test_club2",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-02"
    }

    response = client.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id2 = response.json()['data']['id']

    response = client.get("/join/get_clubs_by_user", params={"user_id": 2})
    assert response.status_code == 404

    response = client.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = client.post("/club/delete_club", params={"club_id": club_id2})
    assert response.status_code == 200

    response = client.get("/club/get_club", params={"club_id": club_id2})
    assert response.status_code == 404

    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_get_clubs_by_user_no_exist_async(ac):
    data = {
        "id": 1,
        "username": "test_async",
        "mentor": False,
        "email": "string",
        "name": "string",
        "surname": "string",
        "is_active": True,
        "is_superuser": True,
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

    club_id = response.json()['data']['id']

    data = {
        "owner": 1,
        "name": "test_club2_async",
        "dest": "string",
        "photo": "string",
        "bio": "string",
        "links": "string",
        "channel_link": "string",
        "comfort_time": "string",
        "date_created": "2021-01-02"
    }

    response = await ac.post("/club/create_club", json=data)
    assert response.status_code == 200

    club_id2 = response.json()['data']['id']

    response = await ac.get("/join/get_clubs_by_user", params={"user_id": 2})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id})
    assert response.status_code == 404

    response = await ac.post("/club/delete_club", params={"club_id": club_id2})
    assert response.status_code == 200

    response = await ac.get("/club/get_club", params={"club_id": club_id2})
    assert response.status_code == 404

    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404






















