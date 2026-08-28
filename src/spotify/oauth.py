import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

SCOPE = " ".join(
    (
        "user-follow-read",
        "user-library-read",
        "user-read-recently-played",
        "user-top-read",
    )
)

load_dotenv()


def get_spotify_secrets() -> dict:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    if client_id is None or client_secret is None or redirect_uri is None:
        raise RuntimeError("ENV variables are not fully set")
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }


def get_access_token() -> str:
    secrets = get_spotify_secrets()
    cache_path = os.getenv("SPOTIFY_CACHE_PATH", ".spotify-cache")

    auth_manager = SpotifyOAuth(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        redirect_uri=secrets["redirect_uri"],
        scope=SCOPE,
        cache_path=cache_path,
    )

    token_info = auth_manager.get_cached_token()

    if token_info is None:
        auth_url = auth_manager.get_authorize_url()
        print(f"Open this URL:\n{auth_url}")

        response_url = input("Paste redirected URL: ")

        code = auth_manager.parse_response_code(response_url)

        token_info = auth_manager.get_access_token(
            code,
            check_cache=False,
        )

    elif auth_manager.is_token_expired(token_info):
        token_info = auth_manager.refresh_access_token(token_info["refresh_token"])

    return token_info["access_token"]
