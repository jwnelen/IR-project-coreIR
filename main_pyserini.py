import math
import pandas as pd
import json

from pyserini.index import IndexReader
from pyserini.analysis import Analyzer, get_lucene_analyzer


def learn_to_rank():
    index_reader = IndexReader('indexes/sample_collection_jsonl')
    qrels = pd.read_csv("data/qrels.dev.tsv", sep='\t', header=None)
    queries = pd.read_csv("data/queries/queries.dev.tsv", sep='\t', names=['qid', 'query'], header=None)

    training_data_list = list()
    # Default analyzer for English uses the Porter stemmer:
    analyzer = Analyzer(get_lucene_analyzer())

    print(index_reader.stats())

    # Number of documents
    N = index_reader.stats().get("documents")
    epsilon = 0.00001

    for idx, row in qrels.iterrows():
        qid = row[0]
        docid = row[2]
        query_frame = queries[queries["qid"] == qid]
        query = query_frame["query"].iloc[0]

        document_vector = index_reader.get_document_vector(str(docid))

        doc = index_reader.doc(str(docid))
        doc_length = len(json.loads(doc.raw()).get("contents").split())

        # Splitting it into tokens
        tokens = analyzer.analyze(query)

        tf_idfs = list()
        for term in tokens:
            # To prevent some null pointers
            t = analyzer.analyze(term)
            if len(t) > 0:
                # document frequency, collection frequency
                df, nk = index_reader.get_term_counts(term,
                                                      analyzer=analyzer.analyzer)
                idf = math.log(N / (nk + epsilon))

                frequency_term_in_document = document_vector.get(term, 0)
                tf = frequency_term_in_document / doc_length

                tf_idf = tf * idf
                tf_idfs.append(tf_idf)

        if not query is None:
            score = index_reader.compute_query_document_score(str(docid), str(query))
            query_length = len(query.split())
            training_data_list.append([1, qid, docid, score, sum(tf_idfs), doc_length, query_length])

    results = pd.DataFrame(training_data_list,
                           columns=["relevance", "qid", "docid", "BM25", "TFIDF", "doc length", "query length"])

    # set the max columns to none
    pd.set_option('display.max_columns', None)
    print(results.head())
    print(results.describe())

    results.to_csv('results.csv')


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


def toPrintString(qid, bm25, tdidf, doc_length, query_length):
    # 3 qid:1 1:1 2:1 3:0 4:0.2 5:0
    return f"1 qid:{qid} 1:{bm25} 2:{tdidf} 3:{doc_length} 4:{query_length}"


if __name__ == '__main__':
    # learn_to_rank()

    # For this, first the learn to rank should be called
    training_data = pd.read_csv("results.csv")
    print(training_data)

    with open('training.txt', 'w') as f:
        for index, row in training_data.iterrows():
            qid = row[2]
            bm25 = row[4]
            tfidf = row[5]
            doc_length = row[6]
            query_length = row[7]
            f.write(toPrintString(qid, bm25, tfidf, doc_length, query_length))
            f.write("\n")

    f.close()
