import math
import pandas as pd
import json

from pyserini.index import IndexReader
from pyserini.analysis import Analyzer, get_lucene_analyzer

from progressbar import ProgressBar, Percentage, Bar


def do_search():
    index_reader = IndexReader('indexes/sample_collection_jsonl')
    d = []

    qrels = pd.read_csv("data/qrels.dev.tsv", sep='\t', header=None)
    queries = pd.read_csv("data/queries/queries.dev.tsv", sep='\t', names=['qid', 'query'], header=None)

    # Default analyzer for English uses the Porter stemmer:
    analyzer = Analyzer(get_lucene_analyzer())

    print(index_reader.stats())
    print(qrels.head())
    print(queries.head())
    ep = 0.00001

    N = index_reader.stats().get("documents")

    for index, row in qrels.iterrows():
        qid = row[0]
        docid = row[2]
        query_frame = queries[queries["qid"] == qid]
        query = query_frame["query"].iloc[0]

        document_vector = index_reader.get_document_vector(str(docid))

        doc = index_reader.doc(str(docid))
        # print('contents', json.loads(doc.raw()).get("contents"))
        # print('vector', document_vector)
        doc_length = len(json.loads(doc.raw()).get("contents").split())

        tokens = analyzer.analyze(query)
        # print('tokens', tokens)

        tf_idfs = list()
        for term in tokens:
            # To prevent some null pointers
            t = analyzer.analyze(term)
            if len(t) > 0:
                # document frequency, collection frequency
                df, nk = index_reader.get_term_counts(term,
                                                      analyzer=analyzer.analyzer)
                idf = math.log(N / (nk + ep))

                frequency_term_in_document = document_vector.get(term, 0)
                tf = frequency_term_in_document / doc_length

                tf_idf = tf * idf
                tf_idfs.append(tf_idf)

        if not query is None:
            score = index_reader.compute_query_document_score(str(docid), str(query))
            query_length = len(query.split())
            d.append([1, qid, docid, score, sum(tf_idfs), doc_length, query_length])

    results = pd.DataFrame(d, columns=["relevance", "qid", "docid", "BM25", "TFIDF", "doc length", "query length"])
    # set the max columns to none
    pd.set_option('display.max_columns', None)

    print(results.head())
    print(results.describe())

    results.to_csv('results')


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
