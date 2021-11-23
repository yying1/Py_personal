# no imports beyond numpy should be used in answering this question
import numpy as np

# train datapoints: 2 features and binary output
train_separable = np.array([[2.7810836,2.550537003,-1],
    [1.465489372,2.362125076,-1],
    [3.396561688,4.400293529,-1],
    [1.38807019,1.850220317,-1],
    [3.06407232,3.005305973,-1],
    [7.627531214,2.759262235,1],
    [5.332441248,2.088626775,1],
    [6.922596716,1.77106367,1],
    [8.675418651,-0.242068655,1],
    [7.673756466,3.508563011,1]])

# train datapoints nonseparable: 2 features and binary output
train_nonseparable = np.array([[2.7810836,2.550537003,-1],
    [1.465489372,2.362125076,-1],
    [3.396561688,4.400293529,1],
    [1.38807019,1.850220317,-1],
    [3.06407232,3.005305973,-1],
    [7.627531214,2.759262235,1],
    [5.332441248,2.088626775,1],
    [6.922596716,1.77106367,-1],
    [8.675418651,-0.242068655,1],
    [7.673756466,3.508563011,1]])

# test datapoints: 2 features and binary output
test = np.array([[1.927628496,7.200103829,-1],
    [9.182983992,5.290012983,1]])

#number of epochs
n_epoch = 100

def predict(x, theta):
    """
    Predict y_hat in {-1,1} for a give input x and parameters theta

    Input:
    x: Numpy ndarray shape (2,)
    theta: NumPy ndarray shape (3,), where theta[0] is the bias term
        and theta[1:]

    Return:
    y_hat: -1 or 1
    """
    # Code to make sure the input has the correct size
    assert x.shape == (2,)
    assert theta.shape == (3,)
    # Do not edit any code in this function outside the edit region
    ### BEGIN YOUR CODE ###

    if (np.dot(np.transpose(theta)[1:], x) + np.transpose(theta)[0]) == 0:
        y_hat = 0
    elif (np.dot(np.transpose(theta)[1:], x) + np.transpose(theta)[0]) > 0:
        y_hat = 1
    elif (np.dot(np.transpose(theta)[1:], x) + np.transpose(theta)[0]) < 0:
        y_hat = -1

    ### END YOUR CODE ###
    
    return y_hat

# Run perceptron algorithm
def train(train_x, train_y, n_epoch):
    theta = np.zeros(train_x.shape[1]+1)

    # Train for a fixed number of epochs regardless of convergence
    for epoch in range(n_epoch):
        num_error = 0.0
        for i in range(train_x.shape[0]):
            x = train_x[i,:]
            y_hat = predict(x, theta)

            if train_y[i] != y_hat:
                num_error += 1

            # Update the bias term "theta[0]" and the feature-specific weights "theta[1:]" in the code block below
            ### BEGIN YOUR CODE ###
                if  train_y[i] == 1:
                    theta[0] = theta[0]+1
                    theta[1:] = theta[1:] + x
                elif train_y[i] == -1:
                    theta[0] = theta[0]-1
                    theta[1:] = theta[1:] - x
            ### END YOUR CODE ###
        
        print('epoch={}, errors={}'.format(epoch, num_error))
    return theta

if __name__ == '__main__':
    # split train data into features and predictions
    train_separable_x = train_separable[:,:-1]
    train_separable_y = train_separable[:,-1]
    
    # split non-separable train data into features and predictions
    train_nonseparable_x = train_nonseparable[:,:-1]
    train_nonseparable_y = train_nonseparable[:,-1]
    
    # split test data into features and predictions
    test_x = test[:,:-1]
    test_y = test[:,-1]

    # train theta using training data
    print('Train: separable')
    theta = train(train_separable_x, train_separable_y, n_epoch)

    # make predictions on test data and compare with groundtruth
    print('Test')
    for i in range(test.shape[0]):
        x = test_x[i,:]
        prediction = predict(x, theta)
        print("Expected={}, Predicted={}".format(test_y[i], prediction))
    print()

    # train theta using non-separable training data
    print('Train: nonseparable')
    theta = train(train_nonseparable_x, train_nonseparable_y, n_epoch)

    # make predictions on test data and compare with groundtruth
    print('Test')
    for i in range(test.shape[0]):
        x = test_x[i,:]
        y_hat = predict(x, theta)
        print("y={}, y_hat={}".format(test_y[i], y_hat))

