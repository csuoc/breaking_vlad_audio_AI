import pandas as pd
import time
import requests
import os
from dotenv import load_dotenv

### ID COLUMN ###

df = pd.read_csv("./data/videos.csv")

idlist = [i.split("=")[1] for i in df["Link"]]

df["ID"] = idlist

### API CONNECTION ###

load_dotenv()
token_rapidkey = os.getenv("rapidkey")
token_rapidhost = os.getenv("rapidhost")

urllist = []

headers = {
    "X-RapidAPI-Key": token_rapidkey,
    "X-RapidAPI-Host": token_rapidhost
}

for i in idlist:

    url = "https://youtube-mp36.p.rapidapi.com/dl"
    querystring = {"id":i}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    time.sleep(2)

    try:
        mp3=response["link"]
        urllist.append(mp3)
    except:
        break

df["Download MP3"] = urllist

df.to_csv("./data/videos.csv", index=False)