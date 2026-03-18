

import json

import requests

def req(type, feed_id):
    url = f"https://public.app/{type}/{feed_id}"
    headers = {
        "accept": "text/x-component",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://public.app",
        "referer": url,
        "user-agent": "Mozilla/5.0",
        "cookie":"device_id=web_ju939w177364yGPImI5478735HZPC0pU; device_info=%7B%22auth_token%22%3A%22kjbm9cyxqnxc88j9gylos7j0tn1773745378739%22%2C%22reupload_photo%22%3Afalse%2C%22user_name%22%3A%22%22%2C%22is_uname_valid%22%3Atrue%2C%22fresh_chat_restore_ID%22%3A%22%22%2C%22user_display_name%22%3A%22%22%2C%22user_bio%22%3A%22%22%2C%22error_message%22%3A%22%22%2C%22full_contacts_sync%22%3Afalse%7D",

        "next-action": "7fb28e9046fe4634a5184698cabfc4f91b4b1dc311",
        "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(location)%22%2C%7B%22children%22%3A%5B%22city%22%2C%7B%22children%22%3A%5B%5B%22city_slug%22%2C%22news-in-bhabua%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
    }

    # ✅ Tumhara diya hua body
    payload = [
        {
            "type": type,
            "feedId": feed_id,
            
            "maxCards": 20
        }
    ]

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status:", response.status_code)
    response.encoding = "utf-8"
    # 🔥 Step 1: raw text ko lines me split karo
    lines = response.text.strip().split("\n")

    parsed = {}

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            try:
                parsed[key] = json.loads(value)
            except:
                pass

    # ✅ main data (line "1")
    main_data = parsed.get("1", {})

    # 🎯 card_list nikaalo
    cards = main_data.get("card_list", [])

    print("\nTotal cards:", len(cards))
    return cards



if __name__ == "__main__":
    req('https://public.app/city/news-in-bhabua')