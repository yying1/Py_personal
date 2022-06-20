#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv
import numpy as np
VECTOR_LEN = 300   # Length of word2vec vector
MAX_WORD_LEN = 64  # Max word length in dict.txt and word2vec.txt


# In[4]:


def load_tsv_dataset(file):
    dataset = np.loadtxt(file, delimiter='\t', comments=None, encoding='utf-8',dtype='l,O')
    return dataset


# In[5]:


def load_dictionary(file):
    dict_map = np.loadtxt(file, comments=None, encoding='utf-8',dtype=f'U{MAX_WORD_LEN},l')
    return {word: index for word, index in dict_map}


# In[6]:


def load_feature_dictionary(file):
    word2vec_map = dict()
    with open(file) as f:
        read_file = csv.reader(f, delimiter='\t')
        for row in read_file:
            word, embedding = row[0], row[1:]
            word2vec_map[word] = np.array(embedding, dtype=float)
    return word2vec_map


# In[ ]:


def convert_bw(dt,dict_bw):
    for i in range(len(dt)):
        label = dt[i][0]
        word_list = list(set(list(filter(None, dt[i][1].split()))))
        row_array = np.zeros((len(dict_bw)+1,), dtype=int)
        row_array[0] = label
        for w in word_list:
            if w in dict_bw.keys():
                index = dict_bw[w]
                row_array[1+index] = 1
        if i == 0:
            result_array = np.copy(row_array)
        else:
            result_array = np.vstack([result_array, row_array])
    return result_array


# In[27]:


# array_bw = convert_bw(dt,dict_bw)


# In[31]:


# np.savetxt("1.tsv", array_bw, delimiter="\t",fmt='%i')


# In[52]:


def convert_we(dt,dict_fd):
    for i in range(len(dt)):
        label = dt[i][0]
        word_list = list(filter(None, dt[i][1].split()))
        row_vector = np.zeros((VECTOR_LEN,), dtype=float)
        counter = 0
        for w in word_list:
            if w in dict_fd.keys():
                row_vector = row_vector + dict_fd[w]
                counter+=1
        row_vector = row_vector/counter
        row_vector = np.insert(row_vector, 0, float(label))
        if i == 0:
            result_array = np.copy(row_vector)
        else:
            result_array = np.vstack([result_array, row_vector])
    return result_array


# In[53]:


# array_we = convert_we(dt,dict_fd)


# In[55]:


# np.savetxt("2.tsv", array_we, delimiter="\t",fmt='%.6f')


# In[ ]:


def main(train_in,val_in,test_in,dict_in,fd_in,ftrain_out,fval_out,ftest_out,f_flag):
    data_input = [train_in,val_in,test_in]
    data_output = [ftrain_out,fval_out,ftest_out]
    dict_bw = load_dictionary(dict_in)
    dict_fd = load_feature_dictionary(fd_in)
    for i in range(len(data_input)):
        dt = load_tsv_dataset(data_input[i])
        if int(f_flag) == 1:
            result = convert_bw(dt,dict_bw)
            format_s = "%i"
        else:
            result = convert_we(dt,dict_fd)
            format_s = '%.6f'
        np.savetxt(data_output[i], result, delimiter="\t",fmt=format_s)


# In[ ]:


if __name__ == '__main__':
    import sys
    import csv
    import numpy as np
    VECTOR_LEN = 300   # Length of word2vec vector
    MAX_WORD_LEN = 64  # Max word length in dict.txt and word2vec.txt
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9])

