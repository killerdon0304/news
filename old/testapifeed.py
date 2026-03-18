import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# Load message from data.json
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# message = data["message"]
message = "जिगना गांव में पोल से लटकता तार में बिजली करंट की चपेट में आने से एक महिला की मौत हो गई। जो यह घटना बुधवार की शाम 6 बजे की बताई जाती है। जानकारी के मुताबिक चांद थाना क्षेत्र के जिगना गांव निवासी राधेश्याम राम की 45 वर्ष से पत्नी जोखनी देवी बताई जाती है। पोस्टमार्टम हाउस पहुंचे पूर्व सभापति मलाई सिंह ने बताया कि महिला घर से बाहर निकल रही थी।"


# Facebook Graph API URL
url = f"https://graph.facebook.com/{PAGE_ID}/feed"

# Payload
payload = {
    "message": message,
    "access_token": ACCESS_TOKEN
}

# Make the POST request
response = requests.post(url, data=payload)

# Check response
if response.status_code == 200:
    print("✅ Post successful!")
    print("Post ID:", response.json()["id"])
    print(response.json)
else:
    print("❌ Post failed:")
    print(response.text)
