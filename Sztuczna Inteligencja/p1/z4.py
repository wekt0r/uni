#min of hamming distances between all 01 sentences with d-ones

def hamming_distance(w,v):
    return sum(c != d for c,d in zip(w,v))

def all_1_sentences(n, d):
    for i in range(0,n-d):
        yield [0]*i + [1]*d + [0]*(n-i-d)


def opt_dist(l, d):
    return min([hamming_distance(l, sen) for sen in all_1_sentences(len(l),d)])
