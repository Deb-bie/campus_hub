import os
import requests # type: ignore


def get_user_by_email(user_email):
    profile_url = f"{os.getenv("API_GATEWAY_URL")}/api/v1/user-profile/users/profile/{user_email}"
    response = requests.get(profile_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_user_by_id(user_id):
    profile_url = f"{os.getenv("API_GATEWAY_URL")}/user-profile/api/v1/users/profile/{user_id}"
    response = requests.get(profile_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def get_current_user(token):
    profile_url = f"{os.getenv("API_GATEWAY_URL")}/user-profile/api/v1/users/profile/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(profile_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None