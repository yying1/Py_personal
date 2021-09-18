# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 11:57:43 2021

@author: yingy
"""

# 2021-09-17
# Trying with segment tree 
from math import ceil, log2;
ori = [1,2,3]

# First, we build a tree of sums
""" Function to construct segment tree
from given array. This function allocates memory
for segment tree and calls constructSTUtil() to
fill the allocated memory """
def constructST(arr, n) :
 
    # Allocate memory for the segment tree
 
    # Height of segment tree
    x = (int)(ceil(log2(n)));#this means taking the power of 2 closest to n and >=n?
    
    
    # Maximum size of segment tree
    max_size = 2 * (int)(2**x) - 1;
     
    # Allocate memory
    st = [0] * max_size;
 
    # Fill the allocated memory st
    constructSTUtil(arr, 0, n - 1, st, 0);
 
    # Return the constructed segment tree
    return st;

# A recursive function that constructs, meaning from leaf node (bottom) to top
# Segment Tree for array[ss..se].
# si is index of current node in segment tree st
def constructSTUtil(arr, ss, se, st, si) :
 
    # If there is one element in array,
    # store it in current node of
    # segment tree and return
    if (ss == se) :
     
        st[si] = arr[ss];
        return arr[ss];
     
    # If there are more than one elements,
    # then recur for left and right subtrees
    # and store the sum of values in this node
    mid = getMid(ss, se);
     
    st[si] = constructSTUtil(arr, ss, mid, st, si * 2 + 1) + constructSTUtil(arr, mid + 1, se, st, si * 2 + 2);
     
    return st[si];

# A utility function to get the
# middle index from corner indexes.
def getMid(s, e) :
    return s + (e -s) // 2;


st = constructST(ori,len(ori));