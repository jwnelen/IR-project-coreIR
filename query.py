from whoosh.qparser import QueryParser

# def run_queries():

def initial_search(ix):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse("music")
        results = searcher.search(query, terms=True)

        for r in results:
            print(r, r.score)
            # Was this results object created with terms=True?
            if results.has_matched_terms():
                # What terms matched in the results?
                print(results.matched_terms())
                print(r)

        # What terms matched in each hit?
        print("matched terms")
        for hit in results:
            print(hit.matched_terms())
            print(hit)
