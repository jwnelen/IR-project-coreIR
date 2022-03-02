from math import log

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0


# This returns the score for a single word, combination of multiple words is left to the caller
# ri: Number of relevant documents containing term i
# ni: Number of documents containing the term i
# N: Number of documents in the corpus
# fi: Frequency of term i in the document
# qfi: Frequency of term i in the query
# dl: document length
# avdl: average document length in the corpus

def score_BM25(ri, ni, N, fi, qfi, dl, avdl):
    K = k1 * ((1 - b) + b * dl / avdl)

    part1 = log((ri + 0.5) / (R - ri + 0.5) / ((ni - ri + 0.5) / (N - ni - R + ri + 0.5)))
    constants = ((k1 + 1) * fi) / (K + fi)
    part3 = ((k2 + 1) * qfi) / (k2 + qfi)

    return part1 * constants * part3
