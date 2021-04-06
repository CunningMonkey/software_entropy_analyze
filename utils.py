import math

def get_entropy(files):
    total = sum(files.values())
    entropy = 0
    for count in files.values():
        p = count/total
        entropy += p * math.log(p)
    return -entropy 