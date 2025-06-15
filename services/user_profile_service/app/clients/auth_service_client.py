import httpx # type: ignore
import os
from app.config import settings

class AuthServiceClient:
    base_url = settings.API_GATEWAY

    async def update_user(self, user_id: int, data: dict, token):
        url = f"{AuthServiceClient.base_url}/api/auth/update/{user_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        

    async def delete_user(self, user_id: int, token):
        url = f"{AuthServiceClient.base_url}/api/auth/delete/{user_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        print("headers")
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            # response.raise_for_status()
            print(response.json())
            return response.json()
