# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:49:35 2021

@author: Frank Yue Ying
login: yying2
"""

from note import Note

def main():
    n1 = Note()
    n2 = Note()
    n1.setContent("Meeting tomorrow at 11 ")
    n2.setContent("See me before you leave today ")
    print(n1.getContent())
    print(n2.getContent())
    n1.append("Lunch provided.")
    print(n1.getContent())
    n2.erase()
    print(n2.getContent())
    
if __name__ == "__main__":
    main()