# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:56:12 2021

@author: Frank Yue Ying
login: yying2
"""

class NoteKeeper:
    def __init__(self):
        self._nodeList = []
        self._counter = 0
    def __str__(self):
        return self._nodeList+", "+self._counter
    def add(self,n):
        self._nodeList.append(n)
        self._counter+=1
    def display(self):
        print(self._counter)
        for i in range(self._counter):
            print(i)
            self._nodeList[i].displayNote()