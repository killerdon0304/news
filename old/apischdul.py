import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Load env
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# Load caption
with open("/json/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

IMAGE_PATH = os.path.join("image", "sp_x2qaalo9o7ylw.png")
CAPTION = "Br45 News"
scheduled_time = int((datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp())

# ✅ Step 1: Upload photo (unpublished)
with open(IMAGE_PATH, "rb") as image_file:
    files = {
        'source': image_file
    }
    payload = {
        'access_token': ACCESS_TOKEN,
        'published': 'false'
    }
    upload_url = f"https://graph.facebook.com/{PAGE_ID}/photos"
    upload_response = requests.post(upload_url, files=files, data=payload)

if upload_response.status_code == 200:
    photo_id = upload_response.json().get("id")
    print("✅ Image uploaded successfully. Photo ID:", photo_id)

    # ✅ Step 2: Create scheduled post referencing uploaded image
    feed_url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        'access_token': ACCESS_TOKEN,
        'message': CAPTION,
        'published': 'false',
        'scheduled_publish_time': str(scheduled_time),
        'attached_media': json.dumps([{"media_fbid": photo_id}])
    }
    feed_response = requests.post(feed_url, data=payload)

    if feed_response.status_code == 200:
        post_id = feed_response.json().get("id")
        print("✅ Post scheduled successfully!")
        print("Post ID:", post_id)
    else:
        print("❌ Failed to schedule post:")
        print(feed_response.text)
else:
    print("❌ Failed to upload image:")
    print(upload_response.text)
