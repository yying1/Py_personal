#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langdetect import detect
from langdetect import detect_langs
import pandas as pd
import re


# In[ ]:


## this is an example 
s1 = "本篇博客主要介绍两款语言探测工具，用于区分文本到底是什么语言，"
s2 = 'We are pleased to introduce today a new technology – Record Matching –that automatically finds relevant historical records for every family tree on MyHerit'
s3 = "Javigator：Java代码导读及分析管理工具的设计"

print(detect(s1))
print(detect(s2))
print(detect(s3))     # detect()输出探测出的语言类型
print(detect_langs(s3))


# In[8]:


df = pd.read_excel(r"C:\Users\yingyy\Desktop\DE2FR_Bullet_AGL.xlsx")


# In[9]:


for index, row in df.iterrows(): 
    for col in df.columns.tolist():
        if str(col).lower != 'asin':
            try:
                row[col].value = re.sub('^[=/-]+', '', row[col].value)
            except:
                pass


# In[11]:


df.head()


# In[10]:


for col in df.columns.tolist():
    if col != 'asin':
        df[col+'_result'] = ''


# In[12]:


for index, row in df.iterrows(): 
    for col in df.columns.tolist():
        if 'asin' not in str(col).lower and '_result' not in str(col):
            try:
                print(col)
                if row[col].strip() != '':
                    print (detect_langs(row[col].strip()))
                    row[col+'_result'] = detect_langs(row[col].strip())
            except:
                row[col+'_result'] = 'Error'


# In[13]:


df.to_excel(r"C:\Users\yingyy\Desktop\DE2FR_Bullet_AGL.xlsx",encoding="utf-8",index = False)

