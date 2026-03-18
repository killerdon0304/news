import requests
import json
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

def schedule_facebook_reels():
    # ✅ Load environment variables
    load_dotenv()
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    PAGE_ID = os.getenv("PAGE_ID")

    if not ACCESS_TOKEN or not PAGE_ID:
        print("❌ ACCESS_TOKEN or PAGE_ID missing in environment variables.")
        return

    # ✅ Load data from JSON
    JSON_PATH = "json/deta.json"
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except Exception as e:
        print("❌ Failed to load JSON:", e)
        return

    # ✅ Base time (now + 30 min)
    base_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    scheduled_count = 0

    for item in all_data.get("data", []):
        if not item.get("post", False):
            continue

        post_id = item["id"]
        location = item["location"].split(",")[0].strip()

        VIDEO_PATH = f"reel/{post_id}.mp4"
        CAPTION = f"{item['title']}\n\n#kaimurnews #kaimur #{location} #{location}news"

        scheduled_time = int(
            (base_time + timedelta(minutes=30 * scheduled_count)).timestamp()
        )

        if not os.path.exists(VIDEO_PATH):
            print(f"❌ Video not found: {VIDEO_PATH}")
            continue

        print(f"⏳ Scheduling video: {VIDEO_PATH}")

        upload_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/videos"

        payload = {
            "access_token": ACCESS_TOKEN,
            "description": CAPTION,
            "published": "false",
            "scheduled_publish_time": str(scheduled_time),
        }

        try:
            with open(VIDEO_PATH, "rb") as video_file:
                files = {"source": video_file}
                response = requests.post(upload_url, data=payload, files=files)
                response.raise_for_status()

            resp = response.json()
            fb_video_id = resp.get("id")
            print(f"✅ Reel scheduled — Video ID: {fb_video_id}")

            # ✅ Mark as posted
            item["post"] = False
            scheduled_count += 1

        except requests.exceptions.RequestException as e:
            print("❌ Failed to upload video")
            print(e)
            print("Response:", response.text)

        time.sleep(5)  # Facebook video rate-limit safe

    # ✅ Save updated JSON
    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print("✅ JSON updated successfully")
    except Exception as e:
        print("❌ Failed to save JSON:", e)


# ▶ RUN
if __name__ == "__main__":
    schedule_facebook_reels()
