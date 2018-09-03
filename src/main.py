import os
import nltk
from nltk.parse import stanford
from nltk.corpus import (gutenberg, genesis, inaugural,
                         nps_chat, webtext, treebank, wordnet)


os.environ['STANFORD_PARSER'] = 'E:/stanfordParser/jars/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'E:/stanfordParser/jars/stanford-parser-3.9.1-models.jar'
parser = stanford.StanfordParser(model_path="E:\stanfordParser\englishPCFG.ser.gz")


def get_sentences(w):
    sens = []
    count = 0
    word_syn_set = wordnet.synsets(w)
    for word_syn in word_syn_set:
        count += 1
        word_names = word_syn.lemma_names()
        examples = word_syn.examples()
        count_example = 0
        for example in examples:
            count_example += 1
            sens.append(example)
    return sens


def get_complexity_score(sens):
    ss = []
    for sen in sens:
        score_complexity = 1
        parse = parser.raw_parse(sen)
        tree = list(parse)[0]
        for tr in tree.subtrees():
            if tr.label() == 'S':
                score_complexity += 1
        ss.append(score_complexity)
    return ss


# 还没写
def get_context_score(sens):
    ss = []
    for sen in sens:
        ss.append(1)
    return ss


def search_noun(pos, index):
    left = index - 1
    right = index + 1
    while left >= 0 or right < len(pos):
        if left >= 0 and (pos[left][1] == 'NN' or pos[left][1] == 'NNS'):
            return pos[left][0]
        if right < len(pos) and (pos[right][1] == 'NN' or pos[right][1] == 'NNS'):
            return pos[right][0]
        left += 1
        right += 1
    return None


def count_frequency(n, w):
    fre = 0
    for corpus_set in (gutenberg, webtext):  # , genesis, inaugural, nps_chat, treebank, wordnet):
        for fileid in corpus_set.fileids():
            try:
                corpus = gutenberg.sents(fileid)
            except OSError:
                corpus = []
            for sent in corpus:
                if w in sent and n in sent:
                    fre += 1
    return fre


def get_grammar_score(sens, w):
    ss = []
    for sen in sens:
        score_grammar = []
        parse = parser.raw_parse(sen)
        tree = list(parse)[0]
        pos = tree.pos()  # [('the', 'D'), ('dog', 'N'), ('chased', 'V'), ('the', 'D'), ('cat', 'N')]
        # print(pos)
        indexes = [i for i in range(len(pos)) if pos[i][0] == w]
        # print(w, indexes)
        for index in indexes:
            n = search_noun(pos, index)
            # print(n)
            if n is not None:
                fre = count_frequency(n, word)
                score_grammar.append(fre)
        if not score_grammar:
            ss.append(1)
        else:
            ss.append(max(max(score_grammar), 2))
    return ss


def get_length_score(sens):
    ss = []
    for sen in sens:
        length = len(sen.split())
        ss.append(length)
    return ss


if __name__ == '__main__':
    word = "happy"
    sentences = get_sentences(word)
    print("The number of sentences:", len(sentences))
    scores = [0 for i in sentences]
    complexity_scores = get_complexity_score(sentences)
    context_scores = get_context_score(sentences)
    grammar_scores = get_grammar_score(sentences, word)
    length_scores = get_length_score(sentences)
    print("complexity_scores:", complexity_scores)
    print("context_scores:", context_scores)
    print("grammar_scores:", grammar_scores)
    print("length_scores:", length_scores)
    for i in range(len(scores)):
        scores[i] += (complexity_scores[i] / max(complexity_scores)) * \
                     (context_scores[i] / max(context_scores)) * \
                     (grammar_scores[i] / max(grammar_scores)) * \
                     (length_scores[i] / max(length_scores))
    for i in range(len(scores)):
        print(round(scores[i], 10), end=": ")
        print(sentences[i])


