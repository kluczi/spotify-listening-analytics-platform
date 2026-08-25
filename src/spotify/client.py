import httpx

from .oauth import get_access_token

BASE_URL = "https://api.spotify.com/v1"


def spotify_get(endpoint: str, params: dict | None = None) -> dict:
    access_token = get_access_token()

    with httpx.Client() as client:
        response = client.get(
            f"{BASE_URL}/{endpoint}",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            timeout=30,
        )
    response.raise_for_status()
    return response.json()
