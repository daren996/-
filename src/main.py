import os
import nltk
from nltk.parse import stanford
from nltk.corpus import wordnet as wn


def get_sentences(w):
    sens = []
    count = 0
    word_syn_set = wn.synsets(w)
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
    scores = []
    for sen in sens:
        score_complexity = 0
        os.environ['STANFORD_PARSER'] = 'E:/stanfordParser/jars/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = 'E:/stanfordParser/jars/stanford-parser-3.9.1-models.jar'
        parser = stanford.StanfordParser(
            model_path="E:\stanfordParser\englishPCFG.ser.gz")
        parse = parser.raw_parse(sen)
        tree = list(parse)[0]
        for tr in tree.subtrees():
            if tr.label() == 'S':
                score_complexity += 1
        scores.append(score_complexity)
    return scores


if __name__ == '__main__':
    word = "car"
    sentences = get_sentences(word)
    print("The number of sentences:", len(sentences))
    score = [0 for i in sentences]
    complexity_score = get_complexity_score(sentences)
    for i in range(len(score)):
        score[i] += complexity_score[i]
    print(score)


