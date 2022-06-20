# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 19:47:31 2021

@author: Frank Yue Ying (yying2@)
"""
#Question 1
s_speed = input("Please input your speed in mph: ")
f_speed_meterpersecond = float(s_speed)*0.447
print("%6.2f mph = %6.2f m/s"%(float(s_speed),f_speed_meterpersecond))

if f_speed_meterpersecond >= 25.0:
    print("Fast")
elif f_speed_meterpersecond < 5.0:
    print("Slow")
else:
    print("Meh")
    
s_weight= input("Please input your object weight in pounds: ")
f_weight_kg = float(s_weight)*0.4536
print("%6.2f pounds = %6.2f kg"%(float(s_weight),f_weight_kg))
if f_weight_kg > 200.0:
    print("Heavy")
elif f_weight_kg < 100.0:
    print("Light")
else:
    print("Medium")
    
f_kineticenergy = 1/2 *f_speed_meterpersecond*f_weight_kg
print("Kinetic energy = %6.2f kg-m/s^2"%(f_kineticenergy))

#Question 3
f = open('gradebook.txt', 'r')
total,count = 0,0
for line in f:
    name,id,grade = line.split(",")
    grade = int(grade)
    count+=1
    total += grade
    if 100>=grade>=90:
        letterGrade = 'A'
    elif 89>=grade>=80:
        letterGrade = 'B'
    elif 79>=grade>=70:
        letterGrade = 'C'
    elif 69>=grade>=60:
        letterGrade = 'D'
    else:
        letterGrade = 'F'
    print("Name: %10s, ID: %4s, Grade: %2d, Letter Grade: %1s"%(name,id,grade,letterGrade))

avg = float(total)/count
print("Average Grade: %5.2f"%(avg))
f.close()

# Question 4
import math as m
s_angle = input("Please input an angle in degrees: ")
theta = m.radians(float(s_angle))
print ("theta: %3.2f"%theta)
sum_of_squares = m.sin(theta)**2+m.cos(theta)**2
print ("sum of squares: %10.9f"%sum_of_squares)
if sum_of_squares == 1:
    print("Equal")
else:
    print("Not Equal")
#They were not equal, because sum of squares is float 1.00 therefore not equal to 1
    
tan_left = m.tan(theta)
tan_right = m.sin(theta)/m.cos(theta)
print(tan_left,tan_left==tan_right,tan_right)

cos_left = m.cos(theta)
cos_right = m.sin(m.pi/2 - theta)
print(cos_left,cos_left==cos_right,cos_right)

cos2_left = m.cos(theta*2)
cos2_right = (m.cos(theta))**2 - (m.sin(theta))**2
print(cos2_left,cos2_left==cos2_right,cos2_right)

sin2_left = m.sin(theta/2)
sin2_right = m.sqrt((1-m.cos(theta))/2)
print(sin2_left,sin2_left==sin2_right,sin2_right)

a = input("Please input coefficient a: ")
b = input("Please input coefficient b: ")
c = input("Please input coefficient c: ")
a = float(a)
b = float(b)
c = float(c)
if a == 0.0:
    print("No solutions")
elif b**2-4*a*c < 0.0:
    print("x1 and x2 are",str(-b/(2*a))+"+"+str(m.sqrt(-b**2+4*a*c)/(2*a))+"j")
else:
    x1,x2 = -(b/2*a)+m.sqrt(b**2-4*a*c)/(2*a),-(b/2*a)-m.sqrt(b**2-4*a*c)/(2*a)
    print("x1 = %3.2f, x2 = %3.2f"%(x1,x2))

#Question 5
sentence = "Assign the string variable sentence as this sentence"
print("Original Sentence is: %s"%sentence)
print("Capital Sentence is: %s"%sentence.upper())
print(sentence.split())
print(sentence.split('s'))
print(sentence.find('ten'))
print(sentence.find('ten',sentence.find('ten')+1))
tabby = sentence.replace(" ","\t")
print(tabby)

