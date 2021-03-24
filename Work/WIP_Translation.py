#!/usr/bin/env python
# coding: utf-8


def language_detection (inflow_csv_address,result_csv_address,keep_process_result,target_mp,confidence_level):
# In[1]:


    from langdetect import detect
    from langdetect import detect_langs
    import pandas as pd
    import re


# In[2]:


##inflow_csv_address = "C:/Users/yingyy/Desktop/ES2UK_Des_T.csv"
##result_csv_address = ""
##keep_process_result = True
##target_mp = "UK"
##confidence_level = 0.99


# In[3]:


    #Build dictionary for target MP match with language tag
    MP_Language={'AU':'en','US':'en','UK':'en','SG':'en','CN':'zh-cn','FR':'fr','DE':'de','IT':'it','ES':'es'}


# In[4]:


    #read inflow csv content
    df_original = pd.read_csv(inflow_csv_address, encoding = 'utf-8')


# In[5]:


    #remove -/= from beginning of non-asin column to prevent error
    for index, row in df_original.iterrows(): 
        for col in df_original.columns.tolist():
            if str(col).lower != 'asin':
                try:
                    row[col].value = re.sub('^[=/-]+', '', row[col].value)
                except:
                    pass


# In[6]:


    #add column for language detecting content
    result_column = []
    for col in df_original.columns.tolist():
        if 'asin' not in str(col).lower():
            df_original[col+'_result'] = ''
            result_column.append(col+'_result')



# In[8]:


    #run language detection module
    for index, row in df_original.iterrows(): 
        for col in df_original.columns.tolist():
            if 'asin' not in str(col).lower() and '_result' not in str(col):
                try:
                    if row[col].strip() != '':
                        row[col+'_result'] = detect_langs(row[col].strip())
                except:
                    row[col+'_result'] = 'Error'


    #if true, then keep process result as excel file
    if keep_process_result == True:
        df_original.to_excel(inflow_csv_address.replace('.csv','_languagedetection.xlsx'),encoding="utf-8",index = False)


# In[9]:


    #identify language tag and confidence level
    if str(confidence_level)[-1] == "%":
        confidence_level = float(confidence_level[:-1]) / 100.0
    else:
        confidence_level = float(confidence_level)
    language_filter = MP_Language[target_mp.strip().upper()]+":"+str(confidence_level)


# In[10]:


    #assign new df
    df_clean = df_original


# In[11]:


    #clean content
    for index, row in df_clean.iterrows(): 
        for col in result_column:
            if language_filter not in str(row[col]):
                row[col.replace('_result','')] = ''


# In[12]:


    #delete non result column
    for col in result_column:
        df_clean.drop(columns=[col], axis=1, inplace=True)


# In[14]:


    #export to result csv
    df_clean.to_csv(result_csv_address,encoding = 'utf-8',index = False)

