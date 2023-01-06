### IMPORT SELENIUM ###
import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

### CODE ###

url = "https://www.youtube.com/@BreakingVlad/videos"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

list_ = []
newdict = {}

with driver:
    driver.get(url)
    driver.maximize_window()
    time.sleep(7)
    
    SCROLL_PAUSE_TIME = 3

    # Get scroll height

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Find video title elements by ID
    elems = driver.find_elements(By.XPATH, '//*[@id="video-title-link"]')
    
    # For each one save the title and the associated url
    for elem in elems:

        link = elem.get_attribute("href")
        title = elem.text
        
        if link and title != None:
            newdict = {
                "Title" : title,
                "Link" : link
            }
        
        list_.append(newdict)
        
    driver.close()

df = pd.DataFrame(list_)

df.to_csv("./data/videos.csv", index=False)