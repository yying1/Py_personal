# This file was created starting the cookie2.py from Think Bayes
# That code implements a simple Naive Bayes model where there is only one feature, namely
# the flavor of the cookie that was selected from a bowl.
# Refer to that file for the original version of this code.
# Here I will document how I have modified it for our assignment
# Note that you will make changes to three functions
# You will modify the condprob function that is used to compute conditional probabilities
# You will also modify the liklihood function
# You will also handle the case where a feature value has not occurred in the training dataset
# Specific instructions about how to do the modifications are given in the code and comments
# for those functions.
# You will turn in your modified version of this file as well as a text file with the output 
# that was printed when you ran this.

from thinkbayes import Pmf
import csv
from collections import defaultdict

# here are two global variables you can play with once you get the code working
# classval is the name of the feature that you will predict
# smoothing is a flag that indicates whether you are using smoothing or not
classval = 'play'
smoothing = 0

# These global variables keep track of the counts for each feature value in connection with 
# each classvalue (in countdict) as well as the full list of feature values for each feature
# in the order in which they were encountered in the data file (in featuredict)
# featlist is the full list of features in the order in which the corresponding columns 
# appear in the data file
# classpos is the position in the feature list where the class value is found

featuredict = defaultdict(list)
countdict = defaultdict(int)
classpos = 0
featlist = list()

# this function simply concatenates the three tags
def conc (tag1, tag2, tag3):
    return '+'.join([tag1,tag2,tag3])

# this function reads weather.csv and creates featuredict, countdics, and featlist
def read_data ():
    global classpos
    global countdict
    global featuredict
    global featlist
    
    pos = 0
    with open('weather.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            pos += 1
            if pos == 1:
                featlist = row
                for x in range(len(row)):
                    if row[x] == classval:
                        classpos = x
                        featuredict[row[x]] = list()
            else:
                localclassval = row[classpos]
                countdict[localclassval] += 1
                    
                for x in range(len(featlist)):
                    if row[x] in featuredict[featlist[x]]:
                        countdict[conc(featlist[x],row[x],localclassval)] += 1
                    else:
                        featuredict[featlist[x]].append(row[x])
                        countdict[conc(featlist[x],row[x],localclassval)] = 1
                                 

# this function computes the conditional probability of the feature called feat having 
# the value featval given that the class value is classval
def condprob (classval, feat, featval):
## Modify this function to use the value of smoothing
    total = 0  # This will be the total number of instances of class value = classval
    val = 0 # this will be the number of times that feat was of value featval when class was classval
    
    
    for fval in featuredict[feat]:
        count = countdict[conc(feat,fval,classval)] 
        total += count
        if fval == featval:
            val = count
            
    # if featval never occred in the dataset, you need to handle this condition here
    if not(featval in featuredict[feat]):
        total += 0
        val = 0
        
    val = float(val)/total # here is where you finally compute the conditional probability

    return val

def condprob_check(data):
    # This function validates calculations to help identify common problems.
    # If a common problem is identified, this will print an error. 
    # However, if no error is printed, that doesn't guarantee correct code.

    correct_condprobs = {0: # no smoothing
    {'no+outlook+overcast': 0.0,
    'no+temperature+hot': 0.4,
    'no+humidity+normal': 0.2,
    'no+windy+TRUE': 0.6,
    'yes+outlook+overcast': 0.4444444444444444,
    'yes+temperature+hot': 0.2222222222222222,
    'yes+humidity+normal': 0.6666666666666666,
    'yes+windy+TRUE': 0.3333333333333333,
    },
                1:
    {'no+outlook+overcast': 0.125,
    'no+temperature+hot': 0.375,
    'no+humidity+normal': 0.25,
    'no+windy+TRUE': 0.5714285714285714,
    'yes+outlook+overcast': 0.4166666666666667,
    'yes+temperature+hot': 0.25,
    'yes+humidity+normal': 0.5833333333333334,
    'yes+windy+TRUE': 0.36363636363636365,
    }}

    for feature, value in zip(featlist, data[:-1]):
        for classval in ['yes', 'no']:
            if correct_condprobs[smoothing][conc(classval,feature,value)] != condprob(classval,feature,value):
                    print("Conditional probability validation failed")
                    return

# this is a modification on the Cookie class that is set up for the play tennis data
class Weather(Pmf):
    """A map from whether you play tennis or not to a probablity."""

    def __init__(self, hypos):
        """Initialize self.

        hypos: whether you play tennis or not 
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, countdict[hypo])
        self.Normalize()

    def Update(self, data):
        total = 0
        """Updates the PMF with new data.

        data: feature values for outlook, temperature, humidity, and windy
        """
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            total += like
            self.Mult(hypo, like)
        if total > 0: self.Normalize()

    # Currently this function computes the likelihood from just one conditional probability
    # You need to modify it to properly take the full set of features into account.
    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: feature values for outlook, temperature, humidity, and windy
        hypo: whether you play tennis or not
        """
        like = 1
        # in the Cookie problem, there was only one feature.  So the likelihood before
        # it multiplied by the prior probability was just the conditional probability
        # of the feature value given the class value, which you saw in the mix variable
        # That would be like just considering one of the 4 features we have, which I have
        # done below.  Change the code so that you take all f4 features into account
        # according to what we discussed in class and you saw in the Witten book for
        # computing the likelihood for the play tennis dataset

        if data == ['overcast','hot','normal','TRUE','?']:
            condprob_check(data)

        like = condprob(hypo, featlist[0], data[0]) # this is the conditional probability of
                                                    # the value (in data) of the feature (in
                                                    # featlist) given the class value (in hypo)
                                                    # note that featlist lists all of the features
                                                    # and data lists all the values for this instance
        return like

# This function computes the probability for each class value for the data point given
def test_instance (hypos, data):
    pmf = Weather(hypos)
    pmf.Update(data)
    
    print("--------------------------")
    print(data)
    if smoothing: 
        print("Smoothing")
    else: 
        print("No Smoothing")
        
    for hypo, prob in sorted(pmf.Items(), reverse=True):
        print(hypo, prob)

# This function implements the instructions for the assignment.
# It reads the play tennis data, computes all the counts, and then
# evaluates the probability for each possible class value with and
# without smoothing for each of the 4 test instances given in the 
# assignment
def main():
    global smoothing
    
    read_data() 
    hypos = featuredict[classval]    
    
    smoothing = 0
    test_instance(hypos, ['overcast','hot','normal','TRUE','?'])
    test_instance(hypos, ['rainy','hot','high','FALSE','?'])
    test_instance(hypos, ['overcast','cool','normal','TRUE','?'])
    test_instance(hypos, ['rainy','mild','low','FALSE','?'])
    smoothing = 1
    test_instance(hypos, ['overcast','hot','normal','TRUE','?'])
    test_instance(hypos, ['rainy','hot','high','FALSE','?'])
    test_instance(hypos, ['overcast','cool','normal','TRUE','?'])
    test_instance(hypos, ['rainy','mild','low','FALSE','?'])
    
    
if __name__ == '__main__':
    main()
