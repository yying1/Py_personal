# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:40:21 2021

@author: Frank Yue Ying
login: yying2
"""
class Note:
    def __init__(self):
        self._content = ""
        self._author = ""
    def __str__(self):
        return self._author+", "+self._content
    def setContent(self,content):
        self._content = content
    def setAuthor(self,author):
        self._author = author
    def getContent(self):
        return self._content
    def getAuthor(self):
        return self._author
    def append(self,text):
        self._content += text
    def erase(self):
        self._content = ""
    def displayNote(self):
        print("From: ",self._author)
        print("Body:")
        print(self._content)
    
