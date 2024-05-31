from typing import List, AsyncGenerator

from tests.conftest import client, ac


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



def test_create_event_good():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    response = client.post("/events/delete_event", params={"event_id": 1})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": 1})
    assert response.status_code == 404

    delete(1, clubs_id)



async def test_create_event_good_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event_async",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_create_event_user_no_exist():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_create_event_user_no_exist_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_create_event_club_no_exist():
    data = {
        "name": "test_event",
        "club_id": 1,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404


async def test_create_event_club_no_exist_async(ac):
    data = {
        "name": "test_event",
        "club_id": 1,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404


def test_create_event_club_no_permission():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]
    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 403

    delete(2, clubs_id)


async def test_create_event_club_no_permission_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]
    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 403

    await adelete(2, clubs_id, ac)


def test_create_event_user_not_in_club():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]
    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_create_event_user_not_in_club_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]
    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_get_event_good():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    delete(1, clubs_id)


async def test_get_event_good_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    await adelete(1, clubs_id, ac)



def test_get_event_no_exist():
    response = client.get("/events/get_event", params={"event_id": 1})
    assert response.status_code == 404


async def test_get_event_no_exist_async(ac):
    response = await ac.get("/events/get_event", params={"event_id": 1})
    assert response.status_code == 404


def test_update_event_good():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "club_id": clubs_id[0],
        "host_id": 1,
        "name": "test_event",
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/update_event", params={"event_id": event_id}, json=data)
    assert response.status_code == 200

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_update_event_good_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "club_id": clubs_id[0],
        "host_id": 1,
        "name": "test_event",
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/update_event", params={"event_id": event_id}, json=data)
    assert response.status_code == 200

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_update_event_user_no_exist():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "club_id": clubs_id[0],
        "host_id": 2,
        "name": "test_event",
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/update_event", params={"event_id": event_id}, json=data)
    assert response.status_code == 404

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_update_event_user_no_exist_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "club_id": clubs_id[0],
        "host_id": 2,
        "name": "test_event",
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/update_event", params={"event_id": event_id}, json=data)
    assert response.status_code == 404

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_update_event_club_no_exist():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": -1,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 404

    delete(1, clubs_id)



async def test_update_event_club_no_exist_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": -1,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_update_event_club_no_permission():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]
    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 403

    delete(2, clubs_id)


async def test_update_event_club_no_permission_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]
    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 2,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 403

    await adelete(2, clubs_id, ac)


def test_event_reg():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_reg_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)



def test_event_reg_user_no_exist():
    clubs_id = create(1, 1)
    club_id = clubs_id[0]

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 404

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_event_reg_user_no_exist_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 404

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_event_reg_event_no_exist():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "user_id": 2,
        "event_id": 1,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_reg_event_no_exist_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "user_id": 2,
        "event_id": 1,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_event_reg_user_not_in_club():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 404

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_reg_user_not_in_club_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 404

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_event_reg_now_reg():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 409

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_reg_now_reg_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 409

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_get_event_club_good():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = client.get("/events/get_event_club", params={"club_id": clubs_id[0]})
    assert response.status_code == 200

    print(response.json())

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_get_event_club_good_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = await ac.get("/events/get_event_club", params={"club_id": clubs_id[0]})
    assert response.status_code == 200

    print(response.json())

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_get_event_club_no_exist():
    response = client.get("/events/get_event_club", params={"club_id": 1})
    assert response.status_code == 404


async def test_get_event_club_no_exist_async(ac):
    response = await ac.get("/events/get_event_club", params={"club_id": 1})
    assert response.status_code == 404


def test_event_disreg_good():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = client.post("/events/event_disreg", params={"user_id": 2, "event_id": event_id})
    assert response.status_code == 200

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_disreg_good_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = await ac.post("/events/event_disreg", params=data)
    assert response.status_code == 200

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_event_disreg_user_no_exist():
    clubs_id = create(1, 1)
    club_id = clubs_id[0]

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = client.post("/events/event_disreg", params={"user_id": 2, "event_id": event_id})
    assert response.status_code == 404

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_event_disreg_user_no_exist_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = await ac.post("/events/event_disreg", params={"user_id": 2, "event_id": event_id})
    assert response.status_code == 404

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_event_disreg_event_no_exist():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = client.post("/events/event_disreg", params={"user_id": 2, "event_id": 1})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_disreg_event_no_exist_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    response = await ac.post("/events/event_disreg", params={"user_id": 2, "event_id": 1})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_event_disreg_user_not_reg_event():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = client.post("/events/event_disreg", params={"user_id": 2, "event_id": event_id})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User has not registration in this event"

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_event_disreg_user_not_reg_event_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = await ac.post("/events/event_disreg", params={"user_id": 2, "event_id": event_id})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User has not registration in this event"

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_delete_event_good():
    clubs_id = create(1, 1)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(1, clubs_id)


async def test_delete_event_good_async(ac):
    clubs_id = await acreate(1, 1, ac)

    data = {
        "name": "test_event",
        "club_id": clubs_id[0],
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(1, clubs_id, ac)


def test_delete_event_no_exist():
    response = client.post("/events/delete_event", params={"event_id": 1})
    assert response.status_code == 404


async def test_delete_event_no_exist_async(ac):
    response = await ac.post("/events/delete_event", params={"event_id": 1})
    assert response.status_code == 404


def test_get_users_by_event():
    clubs_id = create(2, 1)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = client.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = client.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = client.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = client.get("/events/get_users_by_event", params={"event_id": event_id})
    assert response.status_code == 200

    for user in response.json()['data']:
        assert (user['id'] == 2 or user['id'] == 1)

    response = client.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = client.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    delete(2, clubs_id)


async def test_get_users_by_event_async(ac):
    clubs_id = await acreate(2, 1, ac)
    club_id = clubs_id[0]

    data = {
        "club_id": club_id,
        "user_id": 2,
        "role": "member",
        "balance": 993
    }

    response = await ac.post("/join/join_club", json=data)
    assert response.status_code == 200

    data = {
        "name": "test_event",
        "club_id": club_id,
        "host_id": 1,
        "date": "2021-01-01",
        "sinopsis": "string",
        "contact": "string",
        "speaker": "string",
    }

    response = await ac.post("/events/create_event", json=data)
    assert response.status_code == 200

    event_id = response.json()['data']['id']

    data = {
        "user_id": 2,
        "event_id": event_id,
    }

    response = await ac.post("/events/event_reg", json=data)
    assert response.status_code == 200

    response = await ac.get("/events/get_users_by_event", params={"event_id": event_id})
    assert response.status_code == 200

    for user in response.json()['data']:
        assert (user['id'] == 2 or user['id'] == 1)

    response = await ac.post("/events/delete_event", params={"event_id": event_id})
    assert response.status_code == 200

    response = await ac.get("/events/get_event", params={"event_id": event_id})
    assert response.status_code == 404

    await adelete(2, clubs_id, ac)


def test_get_users_by_event_no_exist():
    response = client.get("/events/get_users_by_event", params={"event_id": 1})
    assert response.status_code == 404


async def test_get_users_by_event_no_exist_async(ac):
    response = await ac.get("/events/get_users_by_event", params={"event_id": 1})
    assert response.status_code == 404

