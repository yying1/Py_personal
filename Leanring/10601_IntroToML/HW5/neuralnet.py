#!/usr/bin/env python
# coding: utf-8

# ### Homework 5 | Frank Yue Ying | yying2@

# In[1]:


import numpy as np
import argparse
import logging


# In[6]:


parser = argparse.ArgumentParser()
parser.add_argument('train_input', type=str,
                    help='path to training input .csv file')
parser.add_argument('validation_input', type=str,
                    help='path to validation input .csv file')
parser.add_argument('train_out', type=str,
                    help='path to store prediction on training data')
parser.add_argument('validation_out', type=str,
                    help='path to store prediction on validation data')
parser.add_argument('metrics_out', type=str,
                    help='path to store training and testing metrics')
parser.add_argument('num_epoch', type=int,
                    help='number of training epochs')
parser.add_argument('hidden_units', type=int,
                    help='number of hidden units')
parser.add_argument('init_flag', type=int, choices=[1, 2],
                    help='weight initialization functions, 1: random')
parser.add_argument('learning_rate', type=float,
                    help='learning rate')
parser.add_argument('--debug', type=bool, default=False,
                    help='set to True to show logging')


# In[17]:


# parser.train_input = "tiny_train_data.csv"
# parser.validation_input = "tiny_validation_data.csv"
# parser.train_out = "tiny_train_out.labels"
# parser.validation_out = "tiny_validation_out.labels"
# parser.metrics_out = "tiny_metrics_out.text"
# parser.num_epoch = 1
# parser.hidden_units = 4
# parser.init_flag = 2
# parser.learning_rate = 0.1


# In[15]:


def args2data(parser):
    """
    Parse argument, create data and label.
    :return:
    X_tr: train data (numpy array)
    y_tr: train label (numpy array)
    X_te: test data (numpy array)
    y_te: test label (numpy array)
    out_tr: predicted output for train data (file)
    out_te: predicted output for test data (file)
    out_metrics: output for train and test error (file)
    n_epochs: number of train epochs
    n_hid: number of hidden units
    init_flag: weight initialize flag -- 1 means random, 2 means zero
    lr: learning rate
    """

    # # Get data from arguments
    out_tr = parser.train_out
    out_te = parser.validation_out
    out_metrics = parser.metrics_out
    n_epochs = parser.num_epoch
    n_hid = parser.hidden_units
    init_flag = parser.init_flag
    lr = parser.learning_rate

    X_tr = np.loadtxt(parser.train_input, delimiter=',')
    y_tr = X_tr[:, 0].astype(int)
    X_tr[:, 0] = 1.0 #add bias terms

    X_te = np.loadtxt(parser.validation_input, delimiter=',')
    y_te = X_te[:, 0].astype(int)
    X_te[:, 0]= 1.0 #add bias terms


    return (X_tr, y_tr, X_te, y_te, out_tr, out_te, out_metrics,
            n_epochs, n_hid, init_flag, lr)


# In[20]:


def shuffle(X, y, epoch):
    """
    Permute the training data for SGD.
    :param X: The original input data in the order of the file.
    :param y: The original labels in the order of the file.
    :param epoch: The epoch number (0-indexed).
    :return: Permuted X and y training data for the epoch.
    """
    np.random.seed(epoch)
    N = len(y)
    ordering = np.random.permutation(N)
    return X[ordering], y[ordering]


# In[34]:


def random_init(shape):
    """
    Randomly initialize a numpy array of the specified shape
    :param shape: list or tuple of shapes
    :return: initialized weights
    """
    # DO NOT CHANGE THIS
    np.random.seed(np.prod(shape))

    # Implement random initialization here
    rand_int = np.random.uniform(-0.1, 0.1,shape)
    return rand_int
    raise NotImplementedError


# In[36]:


def zero_init(shape):
    """
    Initialize a numpy array of the specified shape with zero
    :param shape: list or tuple of shapes
    :return: initialized weights
    """
    return np.zeros(shape)
    raise NotImplementedError


# In[73]:


class NN(object):
    def __init__(self, lr, n_epoch, weight_init_fn, input_size, hidden_size, output_size):
        """
        Initialization
        :param lr: learning rate
        :param n_epoch: number of training epochs
        :param weight_init_fn: weight initialization function
        :param input_size: number of units in the input layer
        :param hidden_size: number of units in the hidden layer
        :param output_size: number of units in the output layer
        """
        self.lr = lr
        self.n_epoch = n_epoch
        self.weight_init_fn = weight_init_fn
        self.n_input = input_size
        self.n_hidden = hidden_size
        self.n_output = output_size

        # initialize weights and biases for the models
        #HINT: pay attention to bias here
        self.w1 = weight_init_fn([hidden_size, input_size]) #alpha
        self.w2 = weight_init_fn([output_size, hidden_size+1]) #beta

        # initialize parameters for adagrad
        self.epsilon = 0.00001
        self.grad_sum_w1 = np.zeros([hidden_size, input_size]) #s for alpha
        self.grad_sum_w2 = np.zeros([output_size, hidden_size+1]) #s for beta

        # feel free to add additional attributes
        self.a = 0.0
        self.z = 0.0
        self.b = 0.0

# In[131]:


# ## hidden Unit D = 4, K = 10, M = X_tr.shape[1] - 1
# print(nn.w1.shape)
# print(nn.w2.shape)
# print(g_alpha.shape)
# print(g_beta.shape)
# print(X_tr.shape[1] - 1)


# In[82]:


def linear(x,nn,i): #used for both (X,alpha) and (z,beta)
    if int(i) == 1:
        return np.dot(x,nn.w1.T)
    if int(i) == 2:
        return np.dot(x,nn.w2.T)
# return a or b


# In[68]:


def sigmoid(a): #used for activation function of a
    e = np.exp(-a)
    return e / (1 + e)
#return z


# In[69]:


def softmax(b): #used for activation function of b
    e = np.exp(b).sum()
    return np.exp(b)/e
#return y_hat


# In[70]:


def forward(X, nn):
    """
    Neural network forward computation.
    Follow the pseudocode!
    :param X: input data
    :param nn: neural network class
    :return: output probability
    """
    a = linear(X,nn,1)
    a = vector(a)
    z = sigmoid(a)
    b = linear(np.insert(z,0,1),nn,2)
    nn.a = a
    nn.z = np.insert(z,0,1)
    nn.b = b
    y_hat = softmax(b)
    return y_hat
    raise NotImplementedError


# In[248]:


# def d_crossentropy(y,y_hat):
#     y_array = np.zeros([1,10])
#     y_array[0][y] = 1
#     dl_dyhat = -1*(y_array/y_hat)
#     dyhat_db = y_hat.T*(y_array-y_hat).T
#     return np.dot(dl_dyhat,dyhat_db.T).T
# # return g_b

def d_crossentropy(y,y_hat):
    y_array = np.zeros([1,10])
    y_array[0][y] = 1.0
    dl_dyhat = np.array([y_hat-y])
    dyhat_db = y_hat.T*(y_array-y_hat).T
    return np.dot(dl_dyhat,dyhat_db.T).T
# return g_b


# In[285]:


def d_linear(x,nn,i,g): # i = 1 for alpha, i = 2 for beta
    if int(i) == 1:
        return np.dot(g.T,x.reshape(1,len(x))).T
    if int(i) == 2:
        db_dz = nn.w2[:,1:]
        g_beta = np.dot(g,x.reshape(len(x),1).T).T
        g_z = np.dot(db_dz.T,g).T
        return g_beta,g_z

#return i = 2 --> (g_beta,g_z) or i = 1 --> (g_alpha,g_x)


# In[239]:


def d_sigmoid(a,z,g_z):
    dz_da = np.exp(a)/(1+np.exp(a))**2
    return np.multiply(g_z,dz_da)
#return g_a


# In[124]:


# def backward(X, y, y_hat, nn):
#     """
#     Neural network backward computation.
#     Follow the pseudocode!
#     :param X: input data
#     :param y: label
#     :param y_hat: prediction
#     :param nn: neural network class
#     :return:
#     d_w1: gradients for w1
#     d_w2: gradients for w2
#     """
#     a = nn.a
#     z = nn.z
#     g_b = d_crossentropy(y,y_hat)
#     g_beta,g_z = d_linear(z,nn,2,g_b)
#     g_a = d_sigmoid(a,z,g_z)
#     g_alpha = d_linear(X,nn,1,g_a)
#     return g_alpha,g_beta
#     raise NotImplementedError

def backward(X, y, y_hat, nn):
    dl_dy = (y_hat-y).reshape(10,1)
    dy_db = nn.z.reshape(nn.z.shape[0],1)
    g_beta = np.dot(dl_dy,dy_db.T).T
    dy_dz = nn.w2
    dz_da = nn.z[1:]*(1-nn.z[1:])
    da_dalpha = X.reshape(len(X),1)
    dl_dz = np.dot(dl_dy.T,dy_dz[:,1:])
    dl_da = dl_dz*dz_da
    g_alpha=np.dot(dl_da.T,da_dalpha.T).T  
    return g_alpha,g_beta
    raise NotImplementedError



# In[ ]:


def avg_ce(e,X_tr, y_tr, nn, X_te, y_te,out_metrics):
    y_array_tr = np.zeros([len(y_tr),10])
    for i in range(len(y_tr)):
        y_array_tr[i][y_tr[i]] = 1
    y_array_te = np.zeros([len(y_te),10])
    for i in range(len(y_te)):
        y_array_te[i][y_te[i]] = 1
    
    a = linear(X_tr,nn,1)
    a = vector(a)
    z = sigmoid(a)
    z_bias = np.insert(z, 0, np.ones([1,z.shape[0]]), axis=1)
    b = linear(z_bias,nn,2)
    ytr_hat = softmax(b)

    tr_ce = -1.0/len(y_tr)*np.dot(y_array_tr,np.log(ytr_hat).T).sum()
    
    a = linear(X_te,nn,1)
    a = vector(a)
    z = sigmoid(a)
    z_bias = np.insert(z, 0, np.ones([1,z.shape[0]]), axis=1)
    b = linear(z_bias,nn,2)
    yte_hat = softmax(b)
    
    te_ce = -1.0/len(y_te)*np.dot(y_array_te,np.log(yte_hat).T).sum()
    result = "epoch="+str(e+1)+" crossentropy(train): "+str(tr_ce)+"\n"+"epoch="+str(e+1)+" crossentropy(validation): "+str(te_ce)
    return result


# In[ ]:


def train(X_tr, y_tr, nn, X_te, y_te,out_metrics,n_epochs):
    """
    Train the network using SGD for some epochs.
    :param X_tr: train data
    :param y_tr: train label
    :param nn: neural network class
    """
    metrics = ""
    for e in range(n_epochs):
        X_tr_shuffle,y_tr_shuffle = shuffle(X_tr,y_tr,e)
        for i in range(len(y_tr_shuffle)):
            x = X_tr_shuffle[i]
            y = y_tr_shuffle[i]
            y_hat = forward(x, nn)
            g_alpha,g_beta = backward(x, y, y_hat, nn)
            nn.grad_sum_w1+= np.multiply(g_alpha,g_alpha).T
            nn.grad_sum_w2+= np.multiply(g_beta,g_beta).T
            nn.w1 = nn.w1 - np.multiply(((nn.lr/(nn.grad_sum_w1+nn.epsilon)**0.5)),g_alpha.T)
            nn.w2 = nn.w2 - np.multiply(((nn.lr/(nn.grad_sum_w2+nn.epsilon)**0.5)),g_beta.T)
            # nn.w1 = nn.w1 - nn.lr*g_alpha
            # nn.w2 = nn.w2 - nn.lr*g_beta
        print_weights(nn)    
        metrics = metrics +"\n"+avg_ce(e,X_tr, y_tr, nn, X_te, y_te,out_metrics)
    return metrics.strip()


# In[ ]:


def test(X, y, nn):
    """
    Compute the label and error rate.
    :param X: input data
    :param y: label
    :param nn: neural network class
    :return:
    labels: predicted labels
    error_rate: prediction error rate
    """
    y_hats = np.empty(len(y), dtype=float)
    a = linear(X,nn,1)
    a = vector(a)
    z = sigmoid(a)
    z_bias = np.insert(z, 0, np.ones([1,z.shape[0]]), axis=1)
    b = linear(z_bias,nn,2)
    y_hat_array = softmax(b)
    for i in range(len(y)):
        y_hats[i] = np.argmax(y_hat_array[i])
    compare = np.equal(y,y_hats)
    error_rate = (float(len(y))-np.count_nonzero(compare))/len(y)
    return y_hats,error_rate


# In[ ]:


def print_weights(nn):
    """
    An example of how to use logging to print out debugging infos.

    Note that we use the debug logging level -- if we use a higher logging
    level, we will log things with the default logging configuration,
    causing potential slowdowns.

    Note that we log NumPy matrices on separate lines -- if we do not do this,
    the arrays will be turned into strings even when our logging is set to
    ignore debug, causing potential massive slowdowns.
    :param nn: your model
    :return:
    """
    logging.debug(f"shape of w1: {nn.w1.shape}")
    logging.debug(nn.w1)
    logging.debug(f"shape of w2: {nn.w2.shape}")
    logging.debug(nn.w2)

# In [ ]:

parser.train_input = "small_train.csv"
parser.validation_input = "small_validation.csv"
parser.train_out = "small_train_out.labels"
parser.validation_out = "small_validation_out.labels"
parser.metrics_out = "small_metrics_out.text"

# parser.train_input = "tiny_train.csv"
# parser.validation_input = "tiny_validation.csv"
# parser.train_out = "tiny_train_out.labels"
# parser.validation_out = "tiny_validation_out.labels"
# parser.metrics_out = "tiny_metrics_out.text"

parser.num_epoch = 5
parser.hidden_units = 4
parser.init_flag = 1
parser.learning_rate = 0.1    
vector = np.vectorize(np.float64)

logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)04d} %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.DEBUG)   
    
# initialize training / test data and labels
X_tr, y_tr, X_te, y_te, out_tr, out_te, out_metrics,n_epochs, n_hid, init_flag, lr = args2data(parser)
# Build model
if int(init_flag) == 1:
    nn = NN(lr,n_epochs,random_init,X_tr.shape[1],n_hid,10)
if int(init_flag) == 2:
    nn = NN(lr,n_epochs,zero_init,X_tr.shape[1],n_hid,10)
# train model
metrics = train(X_tr, y_tr, nn, X_te, y_te,out_metrics,n_epochs)
# test model and get predicted labels and errors
tran_pred, train_error = test(X_tr, y_tr, nn)
test_pred, test_error = test(X_te, y_te, nn)
print()


# In[4]:


# if __name__ == "__main__":
#     import numpy as np
#     import argparse
#     import logging
#     args = parser.parse_args()
#     if args.debug:
#         logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)04d} %(levelname)s - %(message)s',
#                             datefmt="%H:%M:%S",
#                             level=logging.DEBUG)
#     logging.debug('*** Debugging Mode ***')
#     # Note: You can access arguments like learning rate with args.learning_rate

#     # initialize training / test data and labels
#     X_tr, y_tr, X_te, y_te, out_tr, out_te, out_metrics,n_epochs, n_hid, init_flag, lr = args2data(args)
#     # Build model
#     if int(init_flag) == 1:
#         nn = NN(lr,n_epochs,random_init,X_tr.shape[1],n_hid,10)
#     if int(init_flag) == 2:
#         nn = NN(lr,n_epochs,zero_init,X_tr.shape[1],n_hid,10)
#     # train model
#     metrics = train(X_tr, y_tr, nn, X_te, y_te,out_metrics,n_epochs)
#     # test model and get predicted labels and errors
#     tran_pred, train_error = test(X_tr, y_tr, nn)
#     test_pred, test_error = test(X_te, y_te, nn)
#     # write predicted label and error into file
#     np.savetxt(out_tr, tran_pred, delimiter="\n",fmt="%i")
#     np.savetxt(out_te, test_pred, delimiter="\n",fmt="%i")
#     with open(out_metrics, 'w') as f_out: 
#         f_out.write(metrics+"\n")
#         f_out.write("error(train): "+str(train_error)+"\n")
#         f_out.write("error(validation): "+str(test_error))

