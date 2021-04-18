import math
import scipy.stats

class Entropy:
    def __init__(self, entropy, dmm_size, dmm_complexity, dmm_interfacing, commits_msges):
        super().__init__()
        self.entropy = entropy
        self.dmm_size = dmm_size
        self.dmm_complexity = dmm_complexity
        self.dmm_interfacing = dmm_interfacing
        self.commits_msges = commits_msges
    
def get_entropy(files):
    total = sum(files.values())
    entropy = 0
    for count in files.values():
        p = count/total
        entropy += p * math.log(p)
    return -entropy 

def get_KL(files1, files2):
    sum1 = sum(files1.values())
    sum2 = sum(files2.values())

    for key in files2.keys():
        if key not in files1:
            files1[key] = 0
    
    for key in files1.keys():
        if key not in files2:
            files2[key] = 0
    
    prob1, prob2 = [], []
    for key in files1.keys():
        prob1.append(files1[key]/sum1)
        prob2.append(files2[key]/sum2)
    return scipy.stats.entropy(prob1, prob2) 