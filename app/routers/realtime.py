import os

import requests
from fastapi import APIRouter

router = APIRouter(prefix="/realtime")


def get_access_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    access_token_url = "https://mvdapi-auth.montevideo.gub.uy/auth/realms/pci/protocol/openid-connect/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {
        "User-Agent": "curl/7.81.0",  # idk
    }

    response = requests.post(access_token_url, data=payload, headers=headers)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info["access_token"]
        expires_in = token_info["expires_in"]
        return access_token, expires_in
    else:
        raise Exception(str(response.content))


@router.get("/")
def get_realtime():
    try:
        token, _expires_in = get_access_token()
    except Exception as e:
        return str(e)

    response = requests.get(
        "https://api.montevideo.gub.uy/api/transportepublico/buses",
        headers={"User-Agent": "curl/7.81.0", "Authorization": f"Bearer {token}"},
    )

    print(response.json())
    return response.json()
