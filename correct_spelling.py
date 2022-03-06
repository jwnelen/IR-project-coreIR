from spellchecker import SpellChecker
import csv


def correct_corpus(input, output):
    spell = SpellChecker()

    with open(input) as inputf:
        with open(output, 'w') as outputf:
            inputreader = csv.reader(inputf, delimiter='\t')
            outputwriter = csv.writer(outputf, delimiter='\t')
            for row in inputreader:
                # print(row)
                outputwriter.writerow([row[0], correct_sentence(spell, row[1])])




def correct_sentence(spell, sentence):
    sentence_split = sentence.split()
    sentence_corrected = ' '.join([spell.correction(term) if len(term) > 5 else term for term in sentence_split])
    # print(sentence_corrected)
    return sentence_corrected


if __name__ == '__main__':
    folder = 'data/collectionandqueries/'
    corpus = 'queries.dev.small.tsv'
    corrected = 'queries.dev.small_spell_corrected.tsv'

    correct_corpus(folder+corpus, folder+corrected)
