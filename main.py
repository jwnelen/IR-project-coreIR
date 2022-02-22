import whoosh
import pandas as pd


def load_data():
    queries_dev = pd.read_csv('data/queries/queries.dev.tsv', sep='\t')
    print(queries_dev.head())

    # Loading this takes very long haha
    # collection = pd.read_csv('data/collection.tsv', sep='\t')
    # print(collection.head())


if __name__ == '__main__':
    load_data()
