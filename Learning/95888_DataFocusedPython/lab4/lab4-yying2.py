#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Frank Yue Ying
#2021-11-09


# In[1]:


#Problem 1
print("Problem 1")
sentence = "Create a str variable named sentence and set it to the words in this sentence"
words = sentence.split(" ")
with open("words.txt",'w') as f:
    for w in words:
        f.write(w+"\n")


# In[6]:


#Problem 2
print("Problem 2")
mywords = []
with open("words.txt",'r') as f:
    for w in f:
        mywords.append(w.strip())
print(mywords)
print(words==mywords)


# In[7]:


#Problem 3
print("Problem 3")
mylist = [ ('dog', 'cat', 'mouse'), ('tetra', 'goldfish', 'trout'), ('hyrax','wombat', 'gopher')]
with open("mylist.csv",'w') as f:
    for tu in mylist:
        f.write(",".join(tu)+"\n")


# In[10]:


#Problem 4
print("Problem 4")
newlist = list()
with open("mylist.csv",'r') as f:
    for line in f:
        newlist.append(tuple(line.strip().split(",")))
print(newlist)
print(mylist==newlist)


# In[13]:


#Problem 5
print("Problem 5")
import pickle
data = {15:'book', 27:'pen', 12:'tablet', 48:'ink', 44:'pencil', 30:'eraser',72:'wombat'}
print(data)
print(data.keys())
print(data.values())
with open("mydata.bin",'wb') as f:
    pickle.dump(data,f)


# In[17]:


#Problem 6
print("Problem 6")
with open("mydata.bin",'rb') as f:
    newdata = pickle.load(f)
print(newdata)
print(data==newdata)
print(newdata.keys())
print(newdata.values())


# In[52]:


#Problem 7
print("Problem 7")
import numpy as np
A = np.array([4, 0, -1, 9]) # A
B = np.array([10, 3, -2, -2]) # B
C = np.array([ [2, 4], [1, 1] ]) # C
D = np.array([ [1, -1], [-1, 0] ]) # D
names = ["A","B","C","D"]
for i,v in enumerate([A,B,C,D]):
    print("Array "+names[i]+":")
    print("   Array value:",v)
    print("   Array shape:",v.shape)
    print("   Array dimension:",v.ndim)
    
print("C's first row:")
print(C[0,:])
##print(C[0][:])

print("D's first Column:")
print(D[:,0])


# In[48]:


#Problem 8
print("Problem 8")
print("a. Sum and different of A and B")
print(A+B)
print(A-B)
print("b. Sum and different of C and D")
print(C+D)
print(C-D)
print("c. Sum of A and C")
try:
    print(A+C)
except:
    print("Cannot do sum of A and C because the shape is different.")
print("d. multiplication of A and B")
print(A*B)
print(B*A)
print("e. multiplication of C and D")
print(C*D)
print(D*C)
print("f. multiplication of C and B")
try:
    print(C*B)
except:
    print("Cannot do multiplication of C and B because the shape is different")

