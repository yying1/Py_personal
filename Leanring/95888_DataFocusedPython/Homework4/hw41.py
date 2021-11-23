#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Frank Yue Ying (yying2)
#2021-11-20
#Homework 4


# In[39]:


#Part 1
import pandas as pd
df = pd.read_csv("pop.csv", header = 0)
while True:
    choice = input("Please input your option: ")
    try:
        int(choice)
        choice = int(choice)
    except: 
        break
    if choice == 1:
        print("-"*10+"#1"+"-"*10)
        print(df)
    elif choice == 2:
        print("-"*10+"#2"+"-"*10)
        print(df[0:10])
    elif choice == 3:
        print("-"*10+"#3"+"-"*10)
        print(df[["NAME"]].sort_values(by=["NAME"]))
    elif choice == 4:
        print("-"*10+"#4"+"-"*10)
        print(df["POPULATION"].sum())
    elif choice == 5:
        print("-"*10+"#5"+"-"*10)
        print(df.groupby("REGION")["POPULATION"].sum())
    elif choice == 6:
        print("-"*10+"#6"+"-"*10)
        state = input("Please input your state name: ")
        print(df.loc[(df.NAME == state)]["POPULATION"].iat[0])
    elif choice == 7:
        print("-"*10+"#7"+"-"*10)
        print(df.sort_values(by=["NAME"]))
    elif choice == 8:
        print("-"*10+"#8"+"-"*10)
        print(df.sort_values(by=["REGION"]))
    elif choice == 9:
        print("-"*10+"#9"+"-"*10)
        print(df.sort_values(by=["POPULATION"],ascending=False))
    else:
        break

