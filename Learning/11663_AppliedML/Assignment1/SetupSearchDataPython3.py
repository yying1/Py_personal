# 11663-B Assignment 1
# Frank Yue Ying (yying2)
# 2022-01-31

#include some useful libraries
import re
import tokenize
from collections import defaultdict
import random
import csv
import pdb

# From the search data files, this script constructs an instance for each student where the class value is
# the number of words copied by the student and the predictor variable is the total number of wikipedia links clicked on.

# First tabulate the number of words copied from each copy event and index it in a dictionary called
# copydict by a tag that is the copy event's unique identifier.

print("Loading page copy events table from SQL")
copydict = defaultdict(int)  # create the copydict dictionary
f = open('tblPageCopyEvents.sql','r', encoding='cp1252')  # open up the rblPageCopyEvents table file
next(f) # skip initial line with column names
for line in f:  # iterate through the entries in the file
        elts = line.strip().split()  # split the line at white space
        action = elts[1]  # the action id is the second item in the list
        numevents = len(elts) - 2  # all but two of the items in the list will be words copied
        copydict[action] = numevents  # store the number of words in the dictionary
f.close()

# now tabulate words copied in copy events in each log

# To do that, first create the copyaccessdict that stores the total number of words copied
# in a log.  You'll do that by iterating through all the click actions looking for copy
# actions.  You'll use the action id to find the number of words copied that was stored for it
# in copydict.  Each time you find one of these for a log, you'll add it to the total number
# of words copied in that log that you have seen already.

print("Loading log action table from SQL")

copyaccessdict = defaultdict(int)  # create the copyaccessdict
f = open('tblLogAction.sql','r')  # open the tblLogAction table
next(f) # skip initial line with column names
for line in f: # iterate through the entries in the file
    elts = re.split('[^\w]',line) # split the line at whitespace
    action = elts[0] # the action id is the first element in the list
    log = elts[1] # the log id is the next item
    type = elts[2] # the type of event is next.  We want actions with type 1 because those are the copy events
    if type == "1":
        num_words = int(copydict[action])
        print(log, num_words)
        copyaccessdict[log] += num_words #add this action's wordcount to the dictionary entry for its log id
f.close()

# for each log tabulate the the total number of wikipedia pages visited.  This uses very similar code
# to the sections above.  Try to use that documentation to understand how this is working.  This is the first segment
# of code you will modify for the assignment.  You'll add a new dictionary for google page accesses and keep track of
# how many of them you had seen the same way here you see the number of wikipedia accesses being tabulated.
wikiaccessdict = defaultdict(int)  # this is a dictionary that will store the number of wikipedia page access by each
                                   # student who clicked on a wikipedia page at least once.
pageaccessdict = defaultdict(int)  # this is a dictionary that will store the total number of pages clicked by each student

googleaccessdict = defaultdict(int)

print("Loading log pages table from SQL")

f = open('tblLogPages.sql','r')
next(f) # skip header row
for line in f:
    elts = re.split('[^\w]',line)
    lognum = elts[1]
    if line.find('wikipedia') > -1:
        if lognum in wikiaccessdict: wikiaccessdict[lognum] += 1
        else: wikiaccessdict[lognum] = 1
    if line.find('google') > -1:
        if lognum in googleaccessdict: googleaccessdict[lognum] += 1
        else: googleaccessdict[lognum] = 1
    if lognum in pageaccessdict: pageaccessdict[lognum] += 1
    else: 
        pageaccessdict[lognum] = 1
f.close()



# Write each instance to the output file.  This is the second part of the code you'll need to modify.
# Just the same way you see the number of wikipedia accesses being added as a column in the output
# table, add some code to put in a column for google website accesses.

print("writing output file")

with open('output.csv', 'w', newline='') as o:   # open up the output file
    writer = csv.writer(o)           # create a python CSV writer

    # write the header row that lists the columns that will be in the file
    writer.writerow(["LogID", "NumPages", "GoogleAccesses" ,"WikiAccesses", "NumWords"])
    
    for log in sorted(pageaccessdict):  # iterate through the log entries (by their 'log' key).
        
        page_accesses = pageaccessdict[log]     # the next value in the row will be the number of page accesses
        
        if log in wikiaccessdict:               # now check if there is an entry in the wikiaccess 
            wiki_accesses = wikiaccessdict[log] # dictionary for this student.  If there is, the                    
        else:                                   # next entry will be that number, otherwise it will be 0.
            wiki_accesses = 0                   

        if log in googleaccessdict:               
            google_accesses = googleaccessdict[log]                     
        else:                                   
            google_accesses = 0     
            
        if log in copyaccessdict:               # Similarly, the next entry in the line will be the number of
            words_copied = copyaccessdict[log]  # words the student copied, if any.                            
        else:                                  
            words_copied = 0                    
        
        
        #row will be a line in the file for a single user.  It gets filled for each log here.
        # the the first entry in the row will be the logID, followed by the other values we care about.
        #this order should match the order of the header row, above.
        row = [log, page_accesses,google_accesses,wiki_accesses, words_copied]    
        writer.writerow(row)  #write this row to the output file.
    
    
