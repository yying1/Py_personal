############ Welcome to HW7 ############
# TODO: Andrew-id: 


# Imports
# Don't import any other library
import argparse
import numpy as np
from utils import make_dict, parse_file
import logging

# Setting up the argument parser
# don't change anything here

parser = argparse.ArgumentParser()
parser.add_argument('train_input', type=str,
                    help='path to training input .txt file')
parser.add_argument('index_to_word', type=str,
                    help='path to index_to_word.txt file')
parser.add_argument('index_to_tag', type=str,
                    help='path to index_to_tag.txt file')
parser.add_argument('init', type=str,
                    help='path to store the hmm_init.txt (pi) file')
parser.add_argument('emission', type=str,
                    help='path to store the hmm_emission.txt (A) file')
parser.add_argument('transition', type=str,
                    help='path to store the hmm_transition.txt (B) file')
parser.add_argument('--debug', type=bool, default=False,
                    help='set to True to show logging')


# Hint: You might find it useful to define functions that do the following:
# 1. Calculate the init matrix
def build_init(tags,tag_dict):
    first_word = np.array([x[0] for x in tags],dtype='object')
    uniqueValues, occurCount = np.unique(first_word, return_counts=True)
    init = np.empty((len(tag_dict),1), dtype='float')
    total_pseudo = len(tag_dict)+len(first_word)
    for i in range(len(tag_dict)):
        tag = list(tag_dict.keys())[i]
        if tag not in uniqueValues:
            init[tag_dict[tag],0] = 1.0 /total_pseudo
        else:
            tag_index = np.where(uniqueValues == tag)
            init[tag_dict[tag],0] = (1.0+occurCount[tag_index]) /total_pseudo
    return init
# 2. Calculate the emission matrix
def build_emi(tags,tag_dict,word_dict,sentences):
    emi = np.empty((len(tag_dict),len(word_dict)), dtype='float')
    for i in range(len(tag_dict)):
        tag = list(tag_dict.keys())[i]
        word_count = dict.fromkeys(word_dict.keys(),0)
        for t in range(len(tags)):
            match_tag_index = [i for i,x in enumerate(tags[t]) if x == tag]
            if len(match_tag_index) != 0:
                for m in match_tag_index:
                    word_count[sentences[t][m]]+=1
        for word in word_dict.keys():
            emi[i][word_dict[word]] = (word_count[word]+1.0)/(sum(word_count.values())+len(word_dict))
    return emi
# 3. Calculate the transition matrix
def build_tra(tags,tag_dict):
    tra = np.empty((len(tag_dict),len(tag_dict)), dtype='float')
    for i in range(len(tag_dict)):
        tag_s = list(tag_dict.keys())[i]
        tag_count_dict = dict.fromkeys(tag_dict.keys(),0)
        for tag in tags:
            match_tag_index = [i for i,x in enumerate(tag) if x == tag_s and i < len(tag)-1]
            for m in match_tag_index:
                tag_count_dict[tag[m+1]]+=1
        for tag in tag_count_dict.keys():
            tra[i][tag_dict[tag]] = (tag_count_dict[tag]+1.0)/(sum(tag_count_dict.values())+len(tag_dict))
    return tra
# 4. Normalize the matrices appropriately

# TODO: Complete the main function
def main(args):

    # Get the dictionaries
    word_dict = make_dict(args.index_to_word)
    tag_dict = make_dict(args.index_to_tag)

    # Parse the train file
    # Suggestion: Take a minute to look at the training file,
    # it always hels to know your data :)
    sentences, tags = parse_file(args.train_input)

    logging.debug(f"Num Sentences: {len(sentences)}")
    logging.debug(f"Num Tags: {len(tags)}")
    
    init = build_init(tags,tag_dict) # TODO: Construct your init matrix
    emission = build_emi(tags,tag_dict,word_dict,sentences) # TODO: Construct your emission matrix
    transition = build_tra(tags,tag_dict) # TODO: Construct your transition matrix

    # Making sure we have the right shapes
    logging.debug(f"init matrix shape: {init.shape}")
    logging.debug(f"emission matrix shape: {emission.shape}")
    logging.debug(f"transition matrix shape: {transition.shape}")


    ## Saving the files for inference
    ## We're doing this for you :)
    ## TODO: Just Uncomment the following lines when you're ready!
    
    np.savetxt(args.init, init)
    np.savetxt(args.emission, emission)
    np.savetxt(args.transition, transition)

    return 

# No need to change anything beyond this point
if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)04d} %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.DEBUG)
    logging.debug('*** Debugging Mode ***')
    main(args)