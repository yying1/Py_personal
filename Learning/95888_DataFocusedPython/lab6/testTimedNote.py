# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:21:50 2021

@author: Frank Yue Ying
login: yying2
"""

from timedNote import TimedNote

def main():
    n1 = TimedNote()
    n2 = TimedNote()
    n1.setContent("You are fired ")
    n2.setContent("You can\"t fire me,I quit ")
    n1.setAuthor("The Boss")
    n2.setAuthor("Barrett")
    n1.setSendTo("Barrett")
    n2.setSendTo("The Boss")
    n1.setDateTime("2/27/20 1:00 pm")
    n2.setDateTime("2/28/20 8:30 am")
    n1.displayNote()
    n2.displayNote()
    
    
if __name__ == "__main__":
    main()
