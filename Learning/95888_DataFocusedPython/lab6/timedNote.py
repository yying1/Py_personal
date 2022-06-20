# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:11:24 2021

@author: Frank Yue Ying
login: yying2
"""
from note import Note

class TimedNote(Note):
    def __init__(self):
        super().__init__()
        self._sendTo = ""
        self._dateTime = ""
    def __str__(self):
        return super().__str__()
    def setSendTo(self,sendto):
        self._sendTo = sendto
    def setDateTime(self,datetime):
        self._dateTime = datetime
    def getSendTo(self):
        return self._sendTo
    def getDateTime(self):
        return self._dateTime
    def displayNote(self):
        print("Date: ",self._dateTime)
        print("To: ",self._sendTo)
        super().displayNote()
        