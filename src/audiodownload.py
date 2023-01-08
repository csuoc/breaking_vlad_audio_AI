import pandas as pd
import os
import time
from pytube import YouTube

### LOAD CSV ###

df = pd.read_csv("./data/videos.csv")

df["Corrected Title"]=df["Title"].str.extract(r"([\w{1,}\s:]+)")

### AUDIO DOWNLOAD WITH PYTUBE ###

for i in df["Link"]:
    
    # Video Url
    yt = YouTube(i)
  
    # Extract only audio
    video = yt.streams.filter(only_audio=True).first()
  
    # Check for destination to save file
    destination = "./espaudios/"
    
    try:
        # Download the file
        out_file = video.download(output_path=destination)
    
        # Save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        time.sleep(2)
    except:
        print("Connection problems")

