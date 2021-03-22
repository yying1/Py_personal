from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from bs4 import BeautifulSoup
import os

chrome_options = Options()
chrome_path = os.environ['USERPROFILE']+r'\AppData\Local\Google\Chrome\User Data\Default'
chrome_options.add_argument("user-data-dir="+chrome_path)
driver = webdriver.Chrome(options=chrome_options) 
driver.get('https://selection.amazon.com')
print("Please authenticate chrome browse for midway and close the browser")
