import json, re
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from fbimage import schedule_facebook_posts
from image import create_news_image
from req import fetch_feed

image_folder='image'
def date():
    india_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    return india_time.strftime("%d-%m")

def load_existing_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"feed": []}  # Default structure if file not found
extIds=[]
def alredy_exit():
    time =date()
    data = "json/deta.json"
    if os.path.exists(data):
        with open(data, "r", encoding="utf-8") as f:
            a = json.load(f)
            # print(a["time"])
            if a["time"] == time:
                print('alredy data hai')
                return a
            else:
                extIds.extend(entry['id'] for entry in a['data'])
                # --- Delete all files in the image folder ---
                if os.path.exists(image_folder):
                    for filename in os.listdir(image_folder):
                        file_path = os.path.join(image_folder, filename)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                print(f"🗑️ Deleted: {file_path}")
                        except Exception as e:
                            print(f"⚠️ Error deleting {file_path}: {e}")
                else:
                    print(f"📂 Folder '{image_folder}' does not exist.")
                return {"time":time,"data": []}
    else:
        print("File does not exist.")
        return {"time":time,"data": []}

def saveJson(name, data):
    with open(os.path.join("json",f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    # d = load_existing_json("feed_data.json")
    blockCodes = ['BR_KM_BHABUA']
    for block in blockCodes:
        d= fetch_feed(block= block)

        a = d['data']['card_list']
        deta = alredy_exit()
        # print(deta)
        for item in a:
            if "kaimur" in item.get("by_line", "").lower():
                ids = [entry['id'] for entry in deta['data']]
                if item['id'] not in ids and item['id'] not in extIds and item['summary_text'] != '':
                    deta['data'].append({
                        "id": item['id'],
                        "title": re.sub(r'<[^>]+>', '', item['title']),
                        "summary_text": item['summary_text'],
                        "location": item['by_line'],
                        "post": True
                    })
                    create_news_image(
                        banner_head=item['by_line'],
                        headline=item['summary_text'],
                        id=item['id']
                    )
                    print("new data mila hai")
                # print(item['id']+ item['title'])
        saveJson(name='deta', data= deta)
        print(extIds)
    

if __name__ == "__main__":
  main()
  schedule_facebook_posts()