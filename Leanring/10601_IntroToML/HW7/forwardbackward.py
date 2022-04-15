############ Welcome to HW7 ############
# TODO: Andrew-id: 


# Imports
# Don't import any other library
import numpy as np
from utils import make_dict, parse_file, get_matrices, write_predictions, write_metrics
import argparse
import logging

# Setting up the argument parser
# don't change anything here
parser = argparse.ArgumentParser()
parser.add_argument('validation_input', type=str,
                    help='path to validation input .txt file')
parser.add_argument('index_to_word', type=str,
                    help='path to index_to_word.txt file')
parser.add_argument('index_to_tag', type=str,
                    help='path to index_to_tag.txt file')
parser.add_argument('init', type=str,
                    help='path to the learned hmm_init.txt (pi) file')
parser.add_argument('emission', type=str,
                    help='path to the learned hmm_emission.txt (A) file')
parser.add_argument('transition', type=str,
                    help='path to the learned hmm_transition.txt (B) file')
parser.add_argument('prediction_file', type=str,
                    help='path to store predictions')
parser.add_argument('metric_file', type=str,
                    help='path to store metrics')                    
parser.add_argument('--debug', type=bool, default=False,
                    help='set to True to show logging')



# Hint: You might find it helpful to define functions 
# that do the following:
# 1. Calculate Alphas
# 2. Calculate Betas
# 3. Implement the LogSumExpTrick
# 4. Calculate probabilities and predictions
def logSumExpTrick(v):
    m = []
    def logSumExpTrick1(v):
        m = max(v)
        return m + np.log(sum(np.exp(v-m)))
    for v_r in v:
        m.append(logSumExpTrick1(v_r))
#     m = v.max(1)
#     return m + np.log((np.exp(v-m.T)).sum(axis=1))
    return m

## With log
def get_alpha_l(sentence,tag_dict,init,emission,transition,word_dict):
    alpha_l = np.empty((len(sentence),len(tag_dict)), dtype='float')
    def cal_alpha_l(index):
        nonlocal alpha_l
        if index == 0:
            alpha_l[0] = np.log(init)+np.log(emission[:,word_dict[sentence[index]]])
            return alpha_l[0]
        else: 
            al = np.log(emission[:,word_dict[sentence[index]]])+logSumExpTrick(np.log(transition.T)+cal_alpha_l(index-1))
            alpha_l[index] = al.copy()
            return al
    cal_alpha_l(len(sentence)-1) ##one sentence only
    return alpha_l

## Beta with log
def get_beta_l(sentence, tag_dict,emission,transition,word_dict):
    beta_l = np.empty((len(sentence),len(tag_dict)), dtype='float')
    def cal_beta_l(index,length):
        nonlocal beta_l
        if index == length-1:
            beta_l[index] = np.zeros((1,len(tag_dict)))
            return beta_l[index].copy()
        else:
            beta_l[index]  = logSumExpTrick(np.log(transition)+np.log(emission[:,word_dict[sentence[index+1]]])+cal_beta_l(index+1,length))
            return beta_l[index]
    cal_beta_l(0,len(sentence)) ##one sentence only
    return beta_l

def predict(p_yt_l,tag_dict):
    p_yt = np.exp(p_yt_l)
    result = []
    for i in p_yt:
        max_index = np.argmax(i)
        result.append(list(tag_dict.keys())[list(tag_dict.values()).index(max_index)])
    return result

def logSumExpTrick_llh(v):
        m = v.max()
        return m + np.log(sum(np.exp(v-m)))
    
def avg_loglikelihood(alpha_l):
    return logSumExpTrick_llh(alpha_l[-1])
    
# TODO: Complete the main function
def main(args):

    # Get the dictionaries
    word_dict = make_dict(args.index_to_word)
    tag_dict = make_dict(args.index_to_tag)

    # Parse the validation file
    sentences, tags = parse_file(args.validation_input)

    ## Load your learned matrices
    ## Make sure you have them in the right orientation
    ## TODO:  Uncomment the following line when you're ready!
    
    init, emission, transition = get_matrices(args)
    predictions = []
    log_likelihoods = []
    for sentence in sentences:
        alpha_l = get_alpha_l(sentence,tag_dict,init,emission,transition,word_dict) 
        beta_l = get_beta_l(sentence,tag_dict,emission,transition,word_dict)
        p_yt_l = alpha_l+beta_l
        predictions.append(predict(p_yt_l,tag_dict))
        log_likelihoods.append(avg_loglikelihood(alpha_l))
    
    predicted_tags = predictions #TODO: store your predicted tags here (in the right order)
    avg_log_likelihood = sum(log_likelihoods)/len(sentences) # TODO: store your calculated average log-likelihood here
    
    accuracy = 0 # We'll calculate this for you

    ## Writing results to the corresponding files.  
    ## We're doing this for you :)
    ## TODO: Just Uncomment the following lines when you're ready!

    accuracy = write_predictions(args.prediction_file, sentences, predicted_tags, tags)
    write_metrics(args.metric_file, avg_log_likelihood, accuracy)

    return

if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)04d} %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.DEBUG)
    logging.debug('*** Debugging Mode ***')
    main(args)
