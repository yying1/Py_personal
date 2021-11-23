#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Frank Yue Ying
#2021-11-21
#Homework 4 Question 2


# In[11]:


import sqlite3
import pandas as pd


# In[2]:


connection = sqlite3.connect("LeeBooks.db")
cursor = connection.cursor()


# In[10]:


print("-"*10+"#1"+"-"*10)
try:
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
        rows_1 = cursor.execute("pragma table_info({})".format(row[0])).fetchall()
        rows_1 = cursor.execute("PRAGMA table_info("+row[0]+")").fetchall()
        for row_1 in rows_1:
            print(row_1)
except Exception as e:
    print(e)


# In[16]:


print("-"*10+"#2"+"-"*10)
rows_2 = cursor.execute("SELECT LASTNAME,FIRSTNAME,STATE FROM CUSTOMERS").fetchall()
customerDF = pd.DataFrame(rows_2, columns = [name[0] for name in cursor.description])
print(customerDF)
print(customerDF.sort_values(by=["STATE","LASTNAME"]))


# In[25]:


print("-"*10+"#3"+"-"*10)
rows_3 = cursor.execute("SELECT ORDERNUM,QUANTITY,PAIDEACH FROM ORDERITEMS").fetchall()
orderItemsDF = pd.DataFrame(rows_3, columns = [name[0] for name in cursor.description])
print(orderItemsDF)
orderItemsDF["TOTAL"] = orderItemsDF["QUANTITY"]*orderItemsDF["PAIDEACH"]
print(orderItemsDF)
print("Total is ${}".format(orderItemsDF["TOTAL"].sum()))


# In[23]:


print("-"*10+"#4"+"-"*10)
create_booklist = """
CREATE TABLE IF NOT EXISTS BOOKLIST AS 
    SELECT LNAME, FNAME,TITLE 
    FROM AUTHOR 
    JOIN BOOKAUTHOR ON AUTHOR.AUTHORID = BOOKAUTHOR.AUTHORID
    JOIN BOOKS ON BOOKS.ISBN = BOOKAUTHOR.ISBN;
"""
cursor.execute(create_booklist)
rows_4 = cursor.execute("SELECT * FROM BOOKLIST").fetchall()
for row_4 in rows_4:
    print(row_4)


# In[24]:


print("-"*10+"#5"+"-"*10)
booklistDF = pd.DataFrame(rows_4, columns = [name[0] for name in cursor.description])
print(booklistDF)
print(booklistDF.sort_values(by=["LNAME","FNAME"]))
print(booklistDF.groupby("LNAME")["LNAME"].count())

