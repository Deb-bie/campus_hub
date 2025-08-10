import os
import requests # type: ignore
from flask import jsonify # type: ignore


def get_user_by_email(user_email, token):
    try:
        profile_url = f"{os.getenv("API_GATEWAY_URL")}/api/user-profile/users/profile/email/{user_email}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(profile_url, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "User not found"})
        
        user_data = response.json()
        return user_data

    except Exception as e:
        print("Exception while reading JSON:", e)
        print("Raw response:", response.text)
        return jsonify({"error": str(e)})


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