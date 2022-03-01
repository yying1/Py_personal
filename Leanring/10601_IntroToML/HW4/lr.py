#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 2022-02-28 yying2@
import numpy as np


# In[2]:


def read_data(f):
    dataset = np.loadtxt(f, delimiter='\t', comments=None, encoding='utf-8',dtype=np.float64)
    return dataset


# In[26]:


def prepare_data(data):
    theta = np.zeros(data.shape[1],dtype=np.float64)
    y_actual = data[:, 0].copy()
    data[:,0] = 1
    return theta,y_actual,data.copy()


# In[13]:


def sigmoid(theta, x):
    dotprod_output = np.dot(x, theta)
    e = np.exp(dotprod_output)
    return e / (1 + e)


# In[28]:


def predict(theta, X):
    # TODO: Implement `predict` using vectorization
    prediction = np.zeros(X.shape[0])
    for i in range(X.shape[0]):
        if sigmoid(theta,X[i]) > 0.5:
            prediction[i] = 1
    return prediction


# In[31]:


def train(theta, X, y, num_epoch, learning_rate):
    # TODO: Implement `train` using vectorization
    N = X.shape[0]
    for ep in range(int(num_epoch)):
        for i in range(len(X)):
            J_theta_d = - X[i].T.dot(y[i]-sigmoid(theta,X[i]))
            theta = theta - learning_rate*J_theta_d
    return theta


# In[42]:


def compute_error(y_pred, y):
    # TODO: Implement `compute_error` using vectorization
    total = len(y)
    error = 0.0
    for i in range(total):
        if round(float(y[i]),5) != round(float(y_pred[i]),5):
            error+=1
    return '{:.6f}'.format(round(error/total,6))


# In[ ]:


def main(train_in,val_in,test_in,train_out,test_out,metric_out,epoch,rate):
    data_input = [train_in,test_in]
    data_output = [train_out,test_out]
    errors = []
    for i in range(len(data_input)):
        dt = read_data(data_input[i])
        theta_original,y,X = prepare_data(dt)
        if i == 0:
            theta_final = train(theta_original, X, y, int(epoch), float(rate))
        y_hat= predict(theta_final,X)
        error = compute_error(y_hat,y)
        errors.append(error)
        np.savetxt(data_output[i], y_hat, delimiter=",",fmt="%i")
    with open(metric_out, 'w') as f_out:
        f_out.write("error(train): "+str(errors[0])+"\n")
        f_out.write("error(test): "+str(errors[1]))


# In[ ]:


if __name__ == '__main__':
    import sys
    import numpy as np
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8])

