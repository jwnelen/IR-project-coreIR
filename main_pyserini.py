from pyserini.search import SimpleSearcher
from pyserini.search import get_topics
from pyserini.index import IndexReader

import pandas as pd

import json
from os import path


def do_search():
    # searcher = SimpleSearcher('indexes/sample_collection_jsonl')
    # searcher.set_bm25()

    index_reader = IndexReader('indexes/sample_collection_jsonl')

    print(index_reader.stats())
    d = []

    # print(index_reader.doc("0"))

    # names = ['colA', 'colB'], header = None
    qrels = pd.read_csv("data/qrels.dev.tsv", sep='\t', header=None)
    queries = pd.read_csv("data/queries/queries.dev.tsv", sep='\t', names=['qid', 'query'], header=None)

    print(qrels.head())
    print(queries.head())

    for index, row in qrels.iterrows():
        qid = row[0]
        docid = row[2]
        query_frame = queries[queries["qid"] == qid]
        query = query_frame["query"]
        # index_reader.compute_query_document_score(docid="0", query="what was the immediate impact"))
        if not query is None:
            score = index_reader.compute_query_document_score(str(docid), str(query))
            if score > 0.01:
                # print(score)
                d.append([1, qid, docid, score])

    results = pd.DataFrame(d)
    print(results.head(100))


# Blatantly copied from https://www.geeksforgeeks.org/python-tsv-conversion-to-json/
def tsv2json(input_file, output_file):
    arr = []
    with open(input_file, 'r') as file:
        titles = ["id", "contents"]
        for line in file:
            d = {}
            for t, f in zip(titles, line.split('\t')):
                # Convert each row into dictionary with keys as titles
                d[t] = f.strip()

            # we will use strip to remove '\n'.
            arr.append(d)

            # we will append all the individual dictionaires into list
            # and dump into file.
        with open(output_file, 'w', encoding='utf-8') as output_file:
            output_file.write(json.dumps(arr, indent=4))


if __name__ == '__main__':
    # Do not do this, this is way too expensive
    # # Convert collection into JSON for Pyserini index builder
    # datafolder = 'data/collectionandqueries/'
    # collection_file = datafolder + 'collection.tsv'
    # collection_file_json = datafolder + 'collection.json'
    # if not path.exists(collection_file_json):
    #     # tsv2json(collection_file, collection_file_json)
    #     df = pd.read_csv(collection_file, sep='\t')
    #     df.to_json(collection_file_json)

    do_search()
