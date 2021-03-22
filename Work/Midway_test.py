#!/usr/bin/env python
# coding: utf-8
# created by yingyy on 2020/12/12
# In[17]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import os


# In[2]:


chrome_options = Options()
chrome_path = os.environ['USERPROFILE']+r'\AppData\Local\Google\Chrome\User Data\Default'
chrome_options.add_argument("user-data-dir="+chrome_path)
driver = webdriver.Chrome(options=chrome_options) 


# In[3]:


driver.get('https://midway-auth.amazon.com/login?html_only_ui=1&next=%2F')


# In[43]:


df_midway = pd.read_excel("Midway_keys.xlsx")
midway_key = ''
for index, row in df_midway.iterrows():
    if row['Status'] == 'used':
        print(row['Midway'].strip()+" used")
    else:
        midway_key = row['Midway'].strip()
        print(midway_key+" try")
        df_midway.loc[index,'Status'] = 'used'
        break
df_midway.to_excel("Midway_keys.xlsx", index = False)


# In[44]:


midway_key


# In[7]:


driver.find_element_by_xpath('//*[@id="user_name"]').clear()
driver.find_element_by_xpath('//*[@id="user_name"]').send_keys('yingyy')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('Wywdzy123!')
driver.find_element_by_xpath('//*[@id="otp"]').send_keys(midway_key+"\n")


# In[8]:


driver.get('https://selection.amazon.com')
while 'midway' in driver.current_url:
    time.sleep(20)
    print('Failed')
driver.quit()

