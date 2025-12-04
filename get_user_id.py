import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BEARER = os.getenv("X_BEARER_TOKEN")

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["id"]

if __name__ == "__main__":
    username = input("Enter X username (without @): ")
    user_id = get_user_id(username)
    print(f"Numeric ID for @{username}: {user_id}")