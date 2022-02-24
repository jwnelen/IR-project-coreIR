import os
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT
from whoosh import index

def build_inverted_index(collection):
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    schema = Schema(content=TEXT(analyzer=StemmingAnalyzer()))
    ix = index.create_in("indexdir", schema)

    writer = ix.writer()
    # For now only adding just a few haha
    size = 100000
    for ind, row in collection.sample(n=size).iterrows():
        writer.add_document(content=row[1])

    # To finalize the indexing
    writer.commit()

    return ix


# def build_document_length_table():
