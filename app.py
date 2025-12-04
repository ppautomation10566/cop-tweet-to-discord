import os
import requests
import re
import time

# Environment variables
BEARER = os.getenv("X_BEARER_TOKEN")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
USER_ID = os.getenv("X_USER_ID")  # numeric ID of target account

# Keywords/regex filter
KEYWORDS = ["leaf", "cardboard", "garbage"]
REGEX = re.compile("|".join(KEYWORDS), re.IGNORECASE)

# Track last seen tweet
LAST_SEEN_FILE = "last_seen.txt"

def get_last_seen():
    if os.path.exists(LAST_SEEN_FILE):
        with open(LAST_SEEN_FILE, "r") as f:
            return f.read().strip()
    return None

def set_last_seen(tweet_id):
    with open(LAST_SEEN_FILE, "w") as f:
        f.write(tweet_id)

def get_tweets():
    url = f"https://api.x.com/2/users/{USER_ID}/tweets"
    headers = {"Authorization": f"Bearer {BEARER}"}
    params = {"max_results": 5}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

def post_to_discord(text, url=None):
    payload = {"content": text}
    if url:
        payload["content"] += f"\n{url}"
    requests.post(DISCORD_WEBHOOK, json=payload)

def main():
    last_seen = get_last_seen()
    tweets = get_tweets()

    for tweet in reversed(tweets):  # oldest first
        tid = tweet["id"]
        text = tweet["text"]

        if last_seen and tid <= last_seen:
            continue

        if REGEX.search(text):
            post_to_discord(text, f"https://x.com/{USER_ID}/status/{tid}")
            set_last_seen(tid)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)  # poll every minute