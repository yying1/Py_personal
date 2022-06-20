#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#95888-C2: Homework 1
#Frank Yue Ying (yying2@)


# In[30]:


# Problem 1
for city in ("pittsburgh.csv","chicago.csv","washington.csv"):
    f = open(city)
    raw = f.readline()
    city = raw.split(",")[0]
    date = raw.split(",")[1]
    month = {'01':'Janauary','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
    print("Weather data for "+city)
    print("%-3s %2s, %4s "%(month[date.split("/")[0]],date.split("/")[1],date.split("/")[2]))
    print("%5s %11s %8s %4s"%("Time","Temperature","Humidity","Wind"))
    print("-"*46)
    lines = f.readlines()
    temp_list=[]
    hum_list=[]
    wind_list=[]
    for line in lines:
        if line.strip() !="":
            data_list = line.split(",")
            time = str(int(data_list[0].strip())//60).zfill(2)+":"+str(int(data_list[0].strip())%60).zfill(2)
            temp = str(int(data_list[1].strip()))
            temp_list.append(int(temp))
            hum = str(int(data_list[2].strip()))
            hum_list.append(int(hum))
            wind = str(int(data_list[3].strip()))
            wind_list.append(int(wind))
            print("%5s %20s %14s %8s"%(time,temp,hum,wind))
    f.close()
    print("Today's high: %2d"%(max(temp_list)))
    print("Today's low: %2d"%(min(temp_list)))
    print("Average temperature: %2.1f"%(round(sum(temp_list)/len(temp_list),1)))
    print("Average humidity: %2.1f"%(round(sum(hum_list)/len(hum_list),1)))
    print("Average wind: %2.1f"%(round(sum(wind_list)/len(wind_list),1)))
    print()


# In[16]:


# Problem 2
city_name = input("Please input your city names (Pittsburgh, Chicago, Washington): ")
f = open(city_name.lower().strip()+".csv")
f.readline()
lines = f.readlines()
time_list=[]
temp_list=[]
hum_list=[]
wind_list=[]
def getmedian(hum_list):
    r = len(hum_list)%2
    if r != 0:
        return sorted(hum_list)[len(hum_list)//2]
    else:
        return ((sorted(hum_list)[len(hum_list)//2-1]+sorted(hum_list)[len(hum_list)//2])/2)
for line in lines:
    if line.strip() !="":
        data_list = line.split(",")
        time_list.append(int(data_list[0].strip()))
        temp = str(int(data_list[1].strip()))
        temp_list.append(int(temp))
        hum = str(int(data_list[2].strip()))
        hum_list.append(int(hum))
        wind = str(int(data_list[3].strip()))
        wind_list.append(int(wind))
f.close()
print("1: Display the original temperature data.")
print("2: Display the temperatures in sorted order. Be sure to create a new list for this, so that #1 still works.")
print("3: Display the mean, median, and mode of the humidity data.")
print("4: Display the low and high wind values.")
print("5: Quit.")
valid_count = 0
invalid_count = 0
while True:
    choice = int(input("Please input your choice (1-5): "))
    if choice not in (1,2,3,4,5):
        print("Error! Please enter a valid choice.")
        invalid_count+=1
    elif choice == 5:
        print("Quit.")
        break
    else:
        valid_count+=1
        if choice == 1:
            print(*temp_list," ")
        elif choice == 2:
            print(*sorted(temp_list)," ")
        elif choice == 3:
            print("Mean humidity: "+str(sum(hum_list)/len(hum_list)))
            print("Mode humidity: "+str(max(set(hum_list), key=hum_list.count)))
            print("Median humidity: "+str(getmedian(hum_list)))
        elif choice ==4:
            print("Low wind: "+ str(min(wind_list)))
            print("High wind: "+str(max(wind_list)))
print("You entered %1d valid choices and %1d invalid choices"%(valid_count,invalid_count))


# In[23]:


# Problem 3
import os
import shutil
print(os.getcwd())
all_files = os.listdir('.')
csv_files = [i for i in all_files if '.csv' in i]
for i,v in enumerate(csv_files):
    print("%1d : %10s"%(i+1,v.split("/")[-1]))
if len(csv_files) == 0:
    print("No csv files found.")
choice = int(input("Enter your choice: "))
file_choice = csv_files[choice-1]
print("File: "+file_choice.split("/")[-1])
f = open(file_choice)
lines = f.readlines()
starting_line = 0
for line in lines:
    if line.strip() !=0:
        starting_line+=1
        print("[ %1d ] %1s"%(starting_line,line.strip()))
f.close()
newdir = input("Input your new directory name: ")
if os.path.isdir(os.getcwd()+"\\"+newdir.strip()):
    print("Error: "+newdir.strip()+" already exists")
else:
    os.mkdir(os.getcwd()+"\\"+newdir.strip())
    shutil.copy(file_choice,os.path.join(os.getcwd(), newdir.strip()))
    os.chdir(os.getcwd()+"\\"+newdir.strip())
    all_files = os.listdir('.')
    print(*all_files," ")


# In[25]:


# Problem 4
os.chdir('..')
f = open("sample.txt")
lines = f.readlines()
sentence_list = []
word_list = []
char_list = []
for line in lines:
    if line.strip() != "":
        word_list.append(len(line.strip().split()))
        char_list.append(len(line.strip())-len(line.strip().split())+1)
        sentence_list.append(line.strip())
print("Number of sentences: %1d"%(len(sentence_list)))
print("Total numer of words: %1d"%(sum(word_list)))
print("Total number of characters: %1d"%(sum(char_list)))
print("Average number of words per sentence: %1.2f"%(sum(word_list)/len(sentence_list)))
print("Average number of characters per sentence: %1.2f"%(sum(char_list)/len(sentence_list)))
print("Average number of characters per word: %1.2f"%(sum(char_list)/sum(word_list)))
ARI = 4.71*(sum(char_list)/sum(word_list))+0.5*(sum(char_list)/len(sentence_list))-21.43
print("ARI: %1.2f"%(ARI))

