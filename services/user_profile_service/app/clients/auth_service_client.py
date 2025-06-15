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
