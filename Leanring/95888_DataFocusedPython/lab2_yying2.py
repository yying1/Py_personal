# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 19:53:43 2021

    95888_C2
    Lab 2
@author: Frank Yue Ying (yying2@)
"""
## Question 1:

#a
for i in range(50,101):
    print (i)
#b
for i in range(100,49,-1):
    print(i, end=' ')
print()
#c
for i in range(50,101):
    if i%2 == 0:
        print(i,end =' ')
print()
#d
for i in range(50,101):
    if i%7 == 0 or i%8 == 0:
        print(i,end =' ')
print()
#e
sumi = 0
for i in range(50,101):
    sumi+=i
print(sumi)

## Question 2:
#a
a = [i for i in range(50,101)]
print(a)
#b
b = [(i,i**2,i**3) for i in range(1,21)]
print(b)
#c
c = [chr(i) for i in range(65,65+26)]
print(c)
#d
d = [c[:i] for i in range(1,11)]
print(d)
#e
e=list()
for i in range(10):
    if i==0:
        e.append(a[0])
    else:
        e.append(b[i-1][0]+a[i])
print(e)
### after getting the first element from a, next element in the list will be the sum of current element in a and the element in b at index -1
### basically its the equivalent of return even numbers of the first element of a

## Question 3:
#a
k = {i+1:v for i,v in enumerate(['dog', 'cat', 'gopher', 'hyrax', 'capybara'])}
print(k)
#b
num = input("Please input a integer to get animal: ")
if int(num) in k:
    print(k[int(num)])
else:
    print("Error")
#c
k[6] = "badger"
k[7] = "groundhog"
k[8] = "mole rat"
print(k)
#d
while True:
    num = input("Please input a integer to get animal: ")
    if int(num) == -1:
        break
    elif int(num) in k:
        print(k[int(num)])
    else:
        print("Error")

## Question 4:
#a
f = open("gradebook.txt",'r')
for i in f:
    list_fields = i.split(",")
    list_fields = [s.strip() for s in list_fields]
    t = (list_fields[0],list_fields[1],list_fields[2])
    print(t)
f.close()
#b
students =[]
f = open("gradebook.txt",'r')
for i in f:
    list_fields = i.split(",")
    list_fields = [s.strip() for s in list_fields]
    t = (list_fields[0],list_fields[1],list_fields[2])
    students.append(t)
f.close()
print(students)
#c
students = [('Name','ID','Score')] + students
for s in students:
    print('%10s %5s %5s'%(s[0],s[1],s[2]))
#d
students =[]
f = open("gradebook.txt",'r')
for i in f:
    list_fields = i.split(",")
    list_fields = [s.strip() for s in list_fields]
    t = (list_fields[0],list_fields[1],int(list_fields[2]))
    students.append(t)
f.close()
print('%10s %5s %5s'%('Name','ID','Score'))
for s in students:
    print('%10s %5s %5d'%(s[0],s[1],s[2]))

## Question 5:
#a
A = {x for x in range(0,6)}
B = {x for x in range(3,11)}
print(A)
print(B)
#b
C = A & B
print(C)
#c
D = A | B
print(D)
#d
E = B - A
print(E)
