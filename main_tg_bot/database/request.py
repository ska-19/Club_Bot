import requests
from bot_instance import URL


async def set_user(user_data):
    rq_user_data = {
        "id": int(user_data["tg_id"]),  # ToDo падает если tg_id > 10^8
        "username": str(user_data["username"]),
        "name": str('') if user_data["name"] is None or 'None' else str(user_data["name"]),
        "surname": str('') if user_data["surname"] is None or 'None' else str(user_data["surname"]),
        "mentor": False,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    url = f'{str(URL)}/user_profile/create_user'

    response = requests.post(url=url, json=rq_user_data, headers=headers)
    print(response)
    print(rq_user_data)
    if response.status_code == 409:
        response = requests.post(url=f'{str(URL)}/user_profile/update_create_user',
                                 json=rq_user_data,
                                 headers=headers,)
    return response


async def set_club(tg_id, club_data):
    if club_data['channel_link'][0] == '@':
        club_data['channel_link'] = 'https://t.me/'+club_data['channel_link'][1:]

    rq_club_data = {
        "owner": int(tg_id),
        "name": str(club_data['name']),
        "dest": str(club_data['dest']),
        "bio": str(club_data['bio']),
        "channel_link": str(club_data['channel_link']),
    }

    headers = {
        "Content-Type": "application/json"
    }
    url = str(URL)+'/club/create_club'

    response = requests.post(url, json=rq_club_data, headers=headers)
    return response


async def is_user_club_admin(tg_id):
    headers = {
        "Content-Type": "application/json"
    }
    url = f'{str(URL)}/join/get_clubs_by_user?user_id={str(tg_id)}'
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        for club in response.json()['data']:
            if club['owner'] == tg_id:
                return club['id']
    return -1


async def club_data_links(tg_id, club_id, data_type):
    headers = {
        "Content-Type": "application/json"
    }
    if data_type == 'club_data':
        url = f'{str(URL)}/statitics/get_club_statistics?user_id={str(tg_id)}&club_id={str(club_id)}'
    elif data_type == 'events_data':
        url = f'{str(URL)}/statitics/get_events_statistics?user_id={str(tg_id)}&club_id={str(club_id)}'

    response = requests.get(url=url, headers=headers)
    return response