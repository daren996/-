
import json
import nltk
from nltk.corpus import wordnet as wn


# if __name__ == '__main__':
#     word = input()
#     count = 0
#     word_syn_set = wn.synsets(word)
#     for word_syn in word_syn_set:
#         count += 1
#         print("\nset" + str(count) + ":")
#         word_names = word_syn.lemma_names()
#         examples = word_syn.examples()
#         for word_name in word_names:
#             print("", word_name, end="")
#         print()
#         count_example = 0
#         for example in examples:
#             count_example += 1
#             print(" example" + str(count_example) + ":", example)

import os
from nltk.parse import stanford

# 添加stanford环境变量,此处需要手动修改，jar包地址为绝对地址。
os.environ['STANFORD_PARSER'] = 'E:/jars/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'E:/jars/stanford-parser-3.5.0-models.jar'

# 为JAVAHOME添加环境变量
java_path = "C:/Program Files (x86)/Java/jdk1.8.0_11/bin/java.exe"
os.environ['JAVAHOME'] = java_path

# 句法标注
parser = stanford.StanfordParser(
    model_path="E:/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sentences = parser.parse_sents("Hello, My name is Melroy.".split(), "What is your name?".split())
print(sentences)

# GUI
for sentence in sentences:
    sentence.draw()