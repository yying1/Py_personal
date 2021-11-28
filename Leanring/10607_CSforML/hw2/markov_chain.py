# no imports beyond numpy should be used in answering this question
import numpy as np

def calc_p_xt_from_p_xt_minus1(p_xt_minus1, p_xt_given_xt_minus1):
    """
    You have been given P(X_{t-1}) for some arbitrary t > 2.
    Compute P(X_t).

    You have also been given P(X_t | X_{t-1}).

    Input:
    p_xt_minus1: NumPy ndarray shape (3,) where p_xt_minus1[i]
        represents P(X_{t-1} = i)
    p_xt_given_xt_minus1: NumPy ndarray shape (3,3) where 
        p_xt_given_xt_minus1[i,j] represents P(X_t = j | X_{t-1} = i)

    Return:
    p_xt: NumPy ndarray shape (3,) where p_xt[i] represents
        P(X_t = i)
    """
    # Code to make sure the input has the correct size
    assert p_xt_minus1.shape == (3,)
    assert p_xt_given_xt_minus1.shape == (3,3)

    ### BEGIN YOUR CODE ###

    p_xt = np.dot(p_xt_minus1,p_xt_given_xt_minus1)

    ### END YOUR CODE ###

    # Code to make sure the output has the correct shape
    assert p_xt.shape == (3,)
    return p_xt

def calc_p_xt(t, p_x1, p_xt_given_xt_minus1):
    """
    Compute P(X_t) for any t >= 1.
    Hint: make use of calc_p_xt_from_p_xt_minus1

    You been given P(X_1) and P(X_t | X_{t-1}).

    Input:
    t: Integer greater than or equal to 1
    p_x1: NumPy ndarray shape (3,) where p_x1[i] represents
        P(X_1 = i)
    p_xt_given_xt_minus1: NumPy ndarray shape (3,3) where 
        p_xt_given_xt_minus1[i,j] represents P(X_t = j | X_{t-1} = i)

    Return:
    p_xt: NumPy ndarray shape (3,) where p_xt[i] represents
        P(X_t = i)
    """
    # Code to make sure the input has the correct size
    assert p_x1.shape == (3,)
    assert p_xt_given_xt_minus1.shape == (3,3)

    ### BEGIN YOUR CODE ###

    if t == 1:
        return p_x1
    else:
        p_xt =  calc_p_xt_from_p_xt_minus1(calc_p_xt(t-1,p_x1, p_xt_given_xt_minus1),p_xt_given_xt_minus1)

    ### END YOUR CODE ###

    # Code to make sure the output has the correct shape
    assert p_xt.shape == (3,)
    return p_xt

if __name__ == '__main__':
    
    p_x1 = np.array([0.1, 0.3, 0.6])
    p_xt_given_xt_minus1 = np.array([
        [0.3, 0.5, 0.2],
        [0.37, 0.33, 0.3],
        [0.3, 0.5, 0.2]])


    # P(X_2)
    result_a = calc_p_xt_from_p_xt_minus1(p_x1, p_xt_given_xt_minus1)
    print('P(X_2):')
    print('Using calc_p_xt_from_p_xt_minus1:', result_a)

    result_b = calc_p_xt(2, p_x1, p_xt_given_xt_minus1)
    print('Using calc_p_xt:', result_b)
    print()

    # P(X_3)
    result = calc_p_xt(3, p_x1, p_xt_given_xt_minus1)
    print('P(X_3):', result)

    # P(X_5)
    result = calc_p_xt(5, p_x1, p_xt_given_xt_minus1)
    print('P(X_5):', result)

    # P(X_100)
    result = calc_p_xt(100, p_x1, p_xt_given_xt_minus1)
    print('P(X_100):', result)

    # P(X_900)
    result = calc_p_xt(900, p_x1, p_xt_given_xt_minus1)
    print('P(X_900):', result)

