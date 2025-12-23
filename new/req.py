import requests
from datetime import datetime, timedelta, timezone
import random
import json

def generate_device_id():
    return "web_" + ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=22))

def get_timestamp_ms():
    # Define IST timezone (UTC+5:30)
    ist = timezone(timedelta(hours=5, minutes=30))
    # Get current IST time
    now_ist = datetime.now(ist)
    # Convert to Unix timestamp in ms
    return int(now_ist.timestamp() * 1000)

# print(get_timestamp_ms())
# exit()

def get_user_agent():
    android_version = "8.0.0"
    device_model = "SM-G955U"
    chrome_version = "137.0.0.0"
    return (
        f"Mozilla/5.0 (Linux; Android {android_version}; {device_model} Build/R16NW) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"
    )

def get_headers(block):
    chrome_version = "137"
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
        "content-type": "application/json",
        "origin": "https://public.app",
        "referer": "https://public.app/",
        "sec-ch-ua": f'"Google Chrome";v="{chrome_version}", "Chromium";v="{chrome_version}", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": get_user_agent(),
        "x-device-id": generate_device_id(),
        "x-location-updated-at": str(get_timestamp_ms()),
        "x-location-updated-type": "IP",
        "x-region": "IN",
        "x-sub-district-code": block,
        "X-LAST-SUB-DISTRICT-CODE": block,
        "X-LOCATION-UPDATE-TYPE": "DISTRICT_CODE"
    }

def fetch_feed(block):
    url = "https://public.app/api/getFeed?max_cards=500"
    headers = get_headers(block = block)
    data = {}  # Can be extended if the API supports filters
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            # print(response.json())
            return response.json()
        except json.JSONDecodeError:
            print("⚠️ Could not parse JSON")
            return None
    else:
        print(f"❌ Failed: {response.status_code}")
        return None



if __name__ == "__main__":
    feed = fetch_feed('BR_KM_BHABUA')
    print(feed)
    # parse_feed(feed)
    # with open("feed_data.json", "w", encoding="utf-8") as f:
    #     json.dump(feed, f, ensure_ascii=False, indent=4)
