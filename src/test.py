
import nltk
import os
from nltk.parse import stanford
from nltk.corpus import wordnet

os.environ['STANFORD_PARSER'] = 'E:/stanfordParser/jars/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'E:/stanfordParser/jars/stanford-parser-3.9.1-models.jar'
parser = stanford.StanfordParser(model_path="E:\stanfordParser\englishPCFG.ser.gz")

synonym_set = []
word_syn_set = wordnet.synsets("happily")
for word_syn in word_syn_set:
    word_names = word_syn.lemma_names()
    synonym_set += word_names
print(set(synonym_set))


tags = nltk.pos_tag(("they watched carefully not").split())
print(tags)

