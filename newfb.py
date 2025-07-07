import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read from environment
page_id = os.getenv('PAGE_ID')
access_token = os.getenv('ACCESS_TOKEN')

if not page_id or not access_token:
    raise ValueError("PAGE_ID and ACCESS_TOKEN must be set in the .env file")

# Message to post
message = 'hello good evening'

# Facebook Graph API URL
url = f'https://graph.facebook.com/{page_id}/feed'

# Parameters for the post
params = {
    'message': message,
    'access_token': access_token,
    'published': True,
    'privacy': json.dumps({"value": "EVERYONE"})
}

def send_post_request(url, params):
    """Send a POST request to the Facebook Graph API"""
    return requests.post(url, params=params)

def handle_response(response):
    """Handle the response from the Facebook Graph API"""
    if response.status_code == 200:
        print('✅ Post successful!')
        print('📌 Post ID:', response.json()['id'])
        
        # Get post details
        post_id = response.json()['id']
        post_url = f'https://graph.facebook.com/{post_id}'
        post_params = {
            'access_token': access_token,
            'fields': 'privacy'
        }
        post_response = requests.get(post_url, params=post_params)
        if post_response.status_code == 200:
            print('🔒 Post Privacy:', post_response.json()['privacy'])
        else:
            print('❌ Failed to get post details.')
            print('Status Code:', post_response.status_code)
            print('Response:', post_response.text)
    else:
        print('❌ Failed to post.')
        print('Status Code:', response.status_code)
        print('Response:', response.text)

def feed():
    response = send_post_request(url, params)
    handle_response(response)

if __name__ == "__main__":
    feed()