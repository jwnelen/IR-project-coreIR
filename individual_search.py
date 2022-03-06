from pyserini.search import SimpleSearcher
from pyserini.analysis import Analyzer, get_lucene_analyzer
from spellchecker import SpellChecker

spell = SpellChecker()


def _search_and_print(term, searcher, analyzer):
    tokens = analyzer.analyze(term)
    print(tokens)
    hits = searcher.search(tokens[0])
    if not hits:
        print("Nothing found")
    for i in range(len(hits)):
        print(f'{i + 1:2} {hits[i].docid:4} {hits[i].score:.5f}')


def correct_term(term='volunterilay'):
    searcher = SimpleSearcher('indexes/collection_json')
    analyzer = Analyzer(get_lucene_analyzer())

    _search_and_print(term, searcher, analyzer)

    corrected_term = spell.correction(term)
    _search_and_print(corrected_term, searcher, analyzer)
    

def correct_sentence():
    sentence = 'why did the us volunterilay enter ww1'
    sentence_split = sentence.split()
    print(spell.unknown(sentence_split))
    corrected_sentence = ' '.join([spell.correction(term) if len(term) > 5 else term for term in sentence_split])
    print(corrected_sentence)


if __name__ == '__main__':
    correct_term()
    correct_sentence()
