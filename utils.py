import math


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
    return 0