import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch from .env
page_id = os.getenv('PAGE_ID')
access_token = os.getenv('ACCESS_TOKEN')

# Facebook Graph API URL for posts
url = f"https://graph.facebook.com/v19.0/{page_id}/posts"

# Parameters for the GET request
params = {
    'access_token': access_token,
    'fields': 'id,message,created_time,permalink_url,full_picture,story,status_type'
}

# Send request
response = requests.get(url, params=params)

# Handle response
if response.status_code == 200:
    data = response.json()
    posts = data.get('data', [])

    print(f"✅ Total Posts Found: {len(posts)}\n")
    print(posts[0])
    # for i, post in enumerate(posts, start=1):

    #     print(f"📌 Post {i}:")
    #     print(f"🆔 ID: {post.get('id')}")
    #     print(f"🕒 Created: {post.get('created_time')}")
    #     print(f"📝 Message: {post.get('message', '(No message)')}")
    #     print(f"🔗 URL: {post.get('permalink_url')}")
    #     print("-" * 40)

else:
    print('❌ Failed to fetch posts.')
    print('Status Code:', response.status_code)
    print('Response:', response.text)
