from pyserini.search import SimpleSearcher
from pyserini.search import get_topics
from pyserini.index import IndexReader

import pandas as pd

import json
from os import path


def do_search():
    searcher = SimpleSearcher('indexes/sample_collection_jsonl')
    searcher.set_bm25()
    # But first, let me parse the kweries
    # searcher.batch_search()
    hits = searcher.search('what is a lobster roll?')

    for i in range(0, 10):
        print(f'{i + 1:2} {hits[i].docid:7} {hits[i].score:.5f} {hits[i].contents}')
        # print(hits[i])

    # print(get_topics('msmarco-passage-dev-subset'))

    # index_reader = IndexReader.from_prebuilt_index('msmarco-passage')
    # index_reader.get_document_vector()


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
