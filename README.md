# EducationDataMining

Implementation of cloze questions generation. 

# 如何使用 WordNet

可以通过 WordNet 获得同义词以及其例句：

	>>> from nltk.corpus import wordnet as wn
	>>> wn.synsets('motorcar')                                //找到同义词集
	[Synset('car.n.01')]
	>>> wn.synset('car.n.01').lemma_names()                   //访问同义词集
	['car', 'auto', 'automobile', 'machine', 'motorcar']
	>>> wn.synset('car.n.01').examples()            //获取该词在该词集下的例句
	['he needs a car to get to work']

# 论文思路

论文原文：[提高完形填空问题质量的选择策略](https://github.com/daren996/EducationDataMining/blob/master/AccurateEducation/Cite/A%20Selection%20Strategy%20to%20Improve%20Cloze%20Question%20Quality.pdf)

## 选择句子

我们需要从每个单词的几个样本句子中进行选择。 
但是， WordNet 在任何给定的 synset 中每个单词都有一个或一个样本句子。 
因此，我们使用了剑桥高级学习词典（CALD） ， 它对每个单词的含义都有几个样本句子。
我们保留了与基线相同的选择标准， 即句子的长度， 并增加了新的语言相关标准。
我们的方法采用以下选择标准： 复杂性， 明确定义的上下文， 语法和长度。
