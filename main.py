import os
import os.path
import pandas as pd
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import index

import indices, parse, query, score


def load_data():
    # Loading this takes very long haha
    return pd.read_csv('data/collection.tsv', sep='\t')


def create_index(collection):
    return indices.build_inverted_index(collection)


def initial_search(ix):
    query.initial_search(ix)


if __name__ == '__main__':
    collection = load_data()
    print('collection is loaded')

    ix = create_index(collection)
    print('created index, now searching')

    initial_search(ix)