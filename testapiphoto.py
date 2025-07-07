import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# Load message from data.json
with open("json/deta.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ✅ 1. Local Image Path
IMAGE_PATH = os.path.join("image", "sp_gyvi3wy10obtq.png")

# ✅ 2. Caption for the photo
CAPTION = "भभुआ: भभुआ नप सभापति ने अपने कार्यालय में पेट्रोल कर्मी की हत्या पर पत्नी को पेंशन स्वीकृति का पत्र दिया #bhabua"

# ✅ 3. Upload Photo to Facebook
with open(IMAGE_PATH, "rb") as image_file:
    files = {
        'source': image_file
    }
    payload = {
        'access_token': ACCESS_TOKEN,
        'caption': CAPTION
    }
    url = f"https://graph.facebook.com/122102804192907654/photos"
    response = requests.post(url, files=files, data=payload)

# ✅ 4. Check response
if response.status_code == 200:
    print("✅ Image post successful!")
    print("Post ID:", response.json()["post_id"])
else:
    print("❌ Failed to post image:")
    print(response.text)