import os
import os.path
import pandas as pd
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import index

ix, collection = None, None


def load_data():
    global collection
    queries_dev = pd.read_csv('data/queries/queries.dev.tsv', sep='\t')

    # Loading this takes very long haha
    collection = pd.read_csv('data/collection.tsv', sep='\t')


def create_index():
    global ix, collection
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    schema = Schema(content=TEXT(analyzer=StemmingAnalyzer()))
    ix = index.create_in("indexdir", schema)

    writer = ix.writer()
    for ind, row in collection.iterrows():
        # For now only adding just a few haha
        if ind % 10000 == 0:
            writer.add_document(content=row[1])

    writer.commit()


if __name__ == '__main__':
    load_data()
    print('collection is loaded')
    # print(collection.head())

    create_index()

    print('created index, now searching')
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse("lizards do protect")
        results = searcher.search(query, terms=True)

        for r in results:
            print(r, r.score)
            # Was this results object created with terms=True?
            if results.has_matched_terms():
                # What terms matched in the results?
                print(results.matched_terms())

        # What terms matched in each hit?
        print("matched terms")
        for hit in results:
            print(hit.matched_terms())
