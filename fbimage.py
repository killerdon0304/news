import requests
import json
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

def schedule_facebook_posts():
    # ✅ Load environment variables
    load_dotenv()
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    PAGE_ID = os.getenv("PAGE_ID")

    if not ACCESS_TOKEN or not PAGE_ID:
        print("❌ ACCESS_TOKEN or PAGE_ID missing in environment variables.")
        return

    # ✅ Load data from JSON file
    JSON_PATH = "json/deta.json"
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except Exception as e:
        print("❌ Failed to load JSON:", e)
        return

    # ✅ Base time: now + 30 minutes
    base_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    scheduled_count = 0

    # ✅ Loop through posts
    for index, item in enumerate(all_data.get("data", [])):
        if not item.get("post", False):
            continue

        image_filename = f"{item['id']}.png"
        location=item['location'].split(',')[0].strip()
        IMAGE_PATH = os.path.join("image", image_filename)
        CAPTION = f"{item["title"]} #kaimurnews #kaimur #{location} #{location}news"
        scheduled_time = int((base_time + timedelta(minutes=30 * scheduled_count)).timestamp())

        if not os.path.exists(IMAGE_PATH):
            print(f"❌ Image not found: {IMAGE_PATH}")
            continue

        # ✅ Step 1: Upload photo
        with open(IMAGE_PATH, "rb") as image_file:
            files = {'source': image_file}
            payload = {
                'access_token': ACCESS_TOKEN,
                'message': CAPTION,
                'published': 'false',
                'scheduled_publish_time': str(scheduled_time)
            }
            upload_url = f"https://graph.facebook.com/{PAGE_ID}/photos"
            try:
                upload_response = requests.post(upload_url, files=files, data=payload)
                upload_response.raise_for_status()
                response_data = upload_response.json()
                post_id = response_data.get("id")
                print(f"✅ Scheduled post — Post ID: {post_id}")

                # ✅ Mark post as scheduled
                item["post"] = False
                scheduled_count += 1

            except requests.exceptions.RequestException as e:
                print("❌ Failed to upload image:")
                print(e)
                print("Response:", upload_response.text)

        time.sleep(2)  # avoid API rate limits

    # ✅ Save the updated JSON
    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print("✅ JSON file updated and saved.")
    except Exception as e:
        print("❌ Failed to save updated JSON:", e)

# 🔄 Run function
if __name__ == "__main__":
    schedule_facebook_posts()
