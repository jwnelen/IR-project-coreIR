import json
import math

import pandas as pd
from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.index import IndexReader


def learn_to_rank():
    index_reader = IndexReader('indexes/sample_collection_jsonl')

    # TODO: Watch out, training takes around 15 min
    qrels = pd.read_csv("data/2019qrels-pass.txt", sep='\s+', header=None)
    queries = pd.read_csv("data/msmarco-test2019-queries.tsv", sep='\t', names=['qid', 'query'], header=None)

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
        tfs = list()
        idfs = list()
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

                tfs.append(tf)
                idfs.append(idf)
                tf_idfs.append(tf_idf)

        if not query is None:
            score = index_reader.compute_query_document_score(str(docid), str(query))
            query_length = len(query.split())
            rel = row[3]
            training_data_list.append(
                [rel, qid, docid, score, sum(tf_idfs), sum(tfs), sum(idfs), doc_length, query_length])

    # This is the _improved_ version, which includes more features
    results = pd.DataFrame(training_data_list,
                           columns=["relevance", "qid", "docid", "BM25", "TFIDF",
                                    "TF", "IDF", "doc length", "query length"])

    results.to_csv('results-2019.train-2.csv')


def to_feature_string(rel, qid, bm25, tdidf, tf, idf, doc_length, query_length):
    # 1 qid:1 1:1 2:1 3:0 4:0.2 5:0
    return f"{rel} qid:{qid} 1:{bm25} 2:{tdidf} 3:{tf} 4:{idf} 5:{doc_length} 6:{query_length}"


def write_features_to_txt():
    # To be able to use this, first learn_to_rank() should be called
    training_data = pd.read_csv("results-2019.train-2.csv")

    # Where it should be saved
    with open('training-2019-data-2.txt', 'w') as f:
        for index, row in training_data.iterrows():
            # rel, qid, docid, score, sum(tf_idfs), sum(tfs), sum(idfs), doc_length, query_length]
            rel = row[1]
            qid = row[2]
            # docid is index 3 but we don't need that anymore
            bm25 = row[4]
            tfidf = row[5]
            tf = row[6]
            idf = row[7]
            doc_length = row[8]
            query_length = row[9]
            f.write(to_feature_string(rel, qid, bm25, tfidf, tf, idf, doc_length, query_length))
            f.write("\n")

    f.close()


if __name__ == '__main__':
    # TODO: Use this method to create the features and store them in a csv
    learn_to_rank()

    # TODO: Use this method to convert the features from csv to the correct txt format
    write_features_to_txt()
