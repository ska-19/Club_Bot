from tests.conftest import client, ac


def test_create_user_good():
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
    assert response.json()['data']['id'] == 1


    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200

    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"


async def test_create_user_good_async(ac):
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
    print(response.json())
    assert response.json()['data']['id'] == 1
    assert response.json()['data']['username'] == 'test_async'
    assert not response.json()['data']['mentor']
    assert response.json()['data']['email'] == 'string'
    assert response.json()['data']['name'] == 'string'
    assert response.json()['data']['surname'] == 'string'
    assert response.json()['data']['is_active']
    assert not response.json()['data']['is_superuser']
    assert not response.json()['data']['is_verified']
    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"


def test_create_user_same_id():
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
    response = client.post("/user_profile/create_user", json=data)
    assert response.status_code == 409
    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"


async def test_create_user_same_id_async(ac):
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
    response = await ac.post("/user_profile/create_user", json=data)
    assert response.status_code == 409
    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"



def test_create_user_bad():
    data = {
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
    assert response.status_code == 422
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"


async def test_create_user_bad_async(ac):
    data = {
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
    assert response.status_code == 422
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"



def test_get_user():
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
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()['data']['id'] == 1
    assert response.json()['data']['username'] == 'test'
    assert not response.json()['data']['mentor']
    assert response.json()['data']['email'] == 'string'
    assert response.json()['data']['name'] == 'string'
    assert response.json()['data']['surname'] == 'string'
    assert response.json()['data']['is_active']
    assert not response.json()['data']['is_superuser']
    assert not response.json()['data']['is_verified']
    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"



async def test_get_user_async(ac):
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
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()['data']['id'] == 1
    assert response.json()['data']['username'] == 'test'
    assert not response.json()['data']['mentor']
    assert response.json()['data']['email'] == 'string'
    assert response.json()['data']['name'] == 'string'
    assert response.json()['data']['surname'] == 'string'
    assert response.json()['data']['is_active']
    assert not response.json()['data']['is_superuser']
    assert not response.json()['data']['is_verified']
    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"




def test_get_user_not_found():
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"


async def test_get_user_not_found_async(ac):
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.status_code == 404
    assert response.json()['detail']['data'] == "User not found"

def test_update_profile_good():
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
        "bio": "new_bio",
        "dob": "2021-01-01",
        "city": "new_city",
        "education": "new_education",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 1}, json=data)
    if response.status_code != 200:
        code = response.status_code
        response = client.post("/user_profile/delete_user", params={"user_id": 1})
        assert response.status_code == 200
        response = client.get("/user_profile/get_user", params={"user_id": 1})
        assert response.json()['detail']['data'] == "User not found"
        assert code == 200
    assert response.status_code == 200
    assert response.json()['data']['bio'] == "new_bio"
    assert response.json()['data']['city'] == "new_city"
    assert response.json()['data']['education'] == "new_education"
    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"


async def test_update_profile_good_async(ac):
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
        "bio": "new_bio",
        "dob": "2021-01-01",
        "city": "new_city",
        "education": "new_education",
    }
    response = await ac.post("/user_profile/update_user", params={"user_id": 1}, json=data)
    if response.status_code != 200:
        code = response.status_code
        response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
        assert response.status_code == 200
        response = await ac.get("/user_profile/get_user", params={"user_id": 1})
        assert response.json()['detail']['data'] == "User not found"
        assert code == 200
    assert response.json()['data']['bio'] == "new_bio"
    assert response.json()['data']['city'] == "new_city"
    assert response.json()['data']['education'] == "new_education"
    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"


def test_update_profile_user_not_found():
    data = {
        "name": "new_name",
        "surname": "new_surname",
        "email": "new_email",
        "tel": "new_tel",
        "photo": "new_photo",
        "comfort_time": "new_comfort_time",
        "course": "new_course",
        "faculty": "new_faculty",
        "links": "new_links",
        "bio": "new_bio",
        "dob": "2021-01-01",
        "city": "new_city",
        "education": "new_education",
    }
    response = client.post("/user_profile/update_user", params={"user_id": 1}, json=data)
    assert response.status_code == 404


async def test_update_profile_user_not_found_async(ac):
    data = {
        "name": "new_name",
        "surname": "new_surname",
        "email": "new_email",
        "tel": "new_tel",
        "photo": "new_photo",
        "comfort_time": "new_comfort_time",
        "course": "new_course",
        "faculty": "new_faculty",
        "links": "new_links",
        "bio": "new_bio",
        "dob": "2021-01-01",
        "city": "new_city",
        "education": "new_education",
    }
    response = await ac.post("/user_profile/update_user", params={"user_id": 1}, json=data)
    assert response.status_code == 404


def test_delete_user_good():
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
    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = client.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"



async def test_delete_user_good_async(ac):
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
    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 200
    response = await ac.get("/user_profile/get_user", params={"user_id": 1})
    assert response.json()['detail']['data'] == "User not found"



def test_delete_user_user_not_found():
    response = client.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 404


async def test_delete_user_user_not_found_async(ac):
    response = await ac.post("/user_profile/delete_user", params={"user_id": 1})
    assert response.status_code == 404

















