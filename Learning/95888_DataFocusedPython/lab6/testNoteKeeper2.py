# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:33:39 2021

@author: Frank Yue Ying
login: yying2
"""

from note import Note
from noteKeeper import NoteKeeper
from timedNote import TimedNote

def main():
    n1 = Note()
    n2 = TimedNote()
    n1.setContent("Meeting tomorrow at 11 ")
    n2.setContent("See me before you leave today ")
    n1.setAuthor("n1")
    n2.setAuthor("n2")
    n2.setSendTo("The Boss")
    n2.setDateTime("2/27/20 1:00 pm")
    nk = NoteKeeper()
    nk.add(n1)
    nk.add(n2)
    nk.display()
    
    
if __name__ == "__main__":
    main()