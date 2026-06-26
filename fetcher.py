import requests


URL = "https://remoteok.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_jobs():
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        print(f"Connection error: {e}")
        return None