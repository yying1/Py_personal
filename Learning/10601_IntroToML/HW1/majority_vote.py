#!/usr/bin/env python
# coding: utf-8

# In[30]:


# 2022-01-26 Homework 1 | yying2@
import sys


# In[31]:


#Referenced from https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
def most_frequent(List):
    return max(set(List), key = List.count)


# In[32]:


def train(trainfile,trainout):
    train_data = []
    train_label = []
    with open(trainfile, 'r') as f:
        rows = f.readlines()
        for row in rows[1:]:
            train_label.append(row[row.rfind("\t"):].strip())
            data = row[:row.rfind('\t')].replace("\t"," ")
            train_data.append(data)
    label = most_frequent(train_label)
    with open(trainout, 'w') as f_out:
        for i in range(len(train_label)):
            f_out.write(label+"\n")
    train_error = 1 - len([x for x in train_label if x == label])/float(len(train_label))
    if train_error == 0.5:
        train_label_unique = list(set(train_label))
        label = sorted(train_label_unique)[-1]
    return label,train_error


# In[41]:


#train("education_test.tsv","1.labels")


# In[33]:


def test(testfile,testout,label):
    test_label = []
    with open(testfile, 'r') as f:
        rows = f.readlines()
        for row in rows[1:]:
            test_label.append(row[row.rfind("\t"):].strip())
    with open(testout, 'w') as f_out:
        for i in range(len(test_label)):
            f_out.write(label+"\n")
    test_error = 1 - len([x for x in test_label if x == label])/float(len(test_label))
    return test_error


# In[34]:


def main(trainfile,testfile,trainout,testout,metrics):
    label,train_error = train(trainfile,trainout)
    test_error = test(testfile,testout,label)
    with open(metrics, 'w') as f_m:
        f_m.write("error(train): "+str(train_error)+"\n")
        f_m.write("error(test): "+str(test_error))


# In[35]:


#main("politicians_train.tsv","politicians_test.tsv","pol_train.labels","pol_test.labels","pol_metrics.txt")


# In[36]:


if __name__ == '__main__':
    import sys
#     infile = sys.argv[1]
#     outfile = sys.argv[2]
#     print("The input file is: %s" % (infile))
#     print("The output file is: %s" % (outfile))
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

