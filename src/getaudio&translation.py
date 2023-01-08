import pandas as pd
import os
import time
from pytube import YouTube
import whisper

### LOAD CSV ###

df = pd.read_csv("./data/videos.csv")

df["Corrected Title"]=df["Title"].str.extract(r"([\w{1,}\s:]+)")

### AUDIO DOWNLOAD WITH PYTUBE AND TRANSCRIPTION WITH WHISPER ###

counter = 1

for i,j in zip(df["Link"], df["Corrected Title"]):
    
    # Video Url
    yt = YouTube(i)
  
    # Extract only audio
    video = yt.streams.filter(only_audio=True).first()
  
    # Check for destination to save file
    destination = "./"
    
    try:
        # Download the file
        print(f"Downloading audio from video #{counter}...")
        out_file = video.download(output_path=destination)
    
        # Save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        # Audio translation
        print("Transcribing and translating the audio...")
        model = whisper.load_model("medium")
        result = model.transcribe(new_file, task="translate")
        
        # Save text into a file
        print("Saving the text file...")
        text_file = open(f"./translatedfiles/{j}.txt", "w")
        text_file.write(result["text"])
        text_file.close()

        # Remove mp3 file once finished
        print("Removing audio file from the system")
        os.remove(new_file)

        #Relax and repeat
        print(f"Text file successfully generated for {j} ({counter}/668)")
        counter = counter + 1
        time.sleep(2)

    except:
        print("Connection problems")

