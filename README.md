# EducationDataMining

Implementation of cloze questions generation. 

# 准备工作

## 使用 WordNet

我们的程序基于 [NLTK](http://www.nltk.org/) 

可以通过 [WordNet](https://wordnet.princeton.edu/) 获得同义词以及其例句：

	>>> from nltk.corpus import wordnet as wn
	>>> wn.synsets('motorcar')                                //找到同义词集
	[Synset('car.n.01')]
	>>> wn.synset('car.n.01').lemma_names()                   //访问同义词集
	['car', 'auto', 'automobile', 'machine', 'motorcar']
	>>> wn.synset('car.n.01').examples()            //获取该词在该词集下的例句
	['he needs a car to get to work']

## 使用 stanford parser

程序使用了 [Stanford Parser](https://nlp.stanford.edu/software/lex-parser.html)
下载链接：https://pan.baidu.com/s/11yERcUjgU2FxzGgyjFMqkw 密码：gj35

可以下载其最新版本，解压后获得其中的路径，设置环境变量如下。
必须装有 java。

	os.environ['STANFORD_PARSER'] = '../jars/stanford-parser.jar'
	os.environ['STANFORD_MODELS'] = '../jars/stanford-parser-3.5.0-models.jar'

在使用中：

	parser = stanford.StanfordParser(model_path="../stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
	sentences = parser.parse_sents("Hello, My name is Melroy.".split(), "What is your name?".split())
	print(sentences)

# 论文思路

论文原文：[提高完形填空问题质量的选择策略](https://github.com/daren996/EducationDataMining/blob/master/AccurateEducation/Cite/A%20Selection%20Strategy%20to%20Improve%20Cloze%20Question%20Quality.pdf)

## 选择句子

我们需要从每个单词的几个样本句子中进行选择。 
但是， WordNet 在任何给定的 synset 中每个单词都有一个或一个样本句子。 
因此，我们使用了剑桥高级学习词典（CALD） ， 它对每个单词的含义都有几个样本句子。
我们保留了与 baseline 相同的选择标准， 即句子的长度， 并增加了新的语言相关标准。
我们的方法采用以下选择标准： 
 
1. 复杂性 complexity
2. 明确定义的上下文 well-defined context
3. 语法 grammaticality
4. 长度 length

我们使用 [Stanford 解析器](https://nlp.stanford.edu/software/lex-parser.html) 解析它并计算得到的子句数来评估句子的复杂性。
例如，用其解析句子： 

>We didn’ t get much information from the first report, but subsequent reports were much more helpful.

	(S
	  (S
	    (NP (NP (NP (PRP We)) (ADJP (JJ didn)) (POS ')) (NN t))
	    (VP
	      (VBP get)
	      (NP (JJ much) (NN information))
	      (PP (IN from) (NP (DT the) (JJ first) (NN report)))))
	  (, ,)
	  (CC but)
	  (S
	    (NP (JJ subsequent) (NNS reports))
	    (VP (VBD were) (ADJP (RB much) (RBR more) (JJ helpful))))
	  (. .)
	)

如果句子的上下文要求句子中存在目标词并拒绝任何其他词的存在，则认为句子的上下文是明确定义的。
评估关于目标词在句子中如何明确定义上下文的方法是将目标词与句子中的其他词之间的搭配分数相加。 
系统通过计算两个相邻单词的窗口内的共同出现来计算内容单词的共现频率。 
然后，它通过计算每个可能对的似然比来识别显着的搭配。

我们还使用斯坦福解析器来评估句子的语法性。
为每个解析的句子分配对应于概率上下文无关语法分数的分数。
较长的句子通常具有较差的分数，因此我们将该分数与句子的长度的平方进行归一化。
虽然解析器适用于任何句子，即使是不合语法的句子，但后者的得分低于语法句子。
虽然没有明确的语义要求，但搭配是经常共同出现的词汇，有时甚至是更大的集合。 
对于我们分析的**形容词**，首先在[Tree](https://www.nltk.org/api/nltk.html#nltk.tree.Tree)中找出其所修饰的名词，然后计算搭配出现的频率。

最后，我们使用句子长度作为质量标准。

**在这里我们需要注意如何将这四个标准统一在一起，可以考虑使用将每个得分归一化，之后计算它们的乘积。这个判断得分的过程会随着语料库的增大而增大，后期可以考虑使用并行技术进行优化。**

## 选择错误选项 Distractor

遵循两个标准：

1. 选择了在语法和搭配上得分较高的干扰项
2. 选择了与目标词在语义上“足够远”的干扰项


# 调试环境

使用 Python3.6 作为编程语言

其中核心算法使用了 nltk 平台，编译之前需要下载其中的gutenberg, genesis, inaugural, nps_chat, webtext, treebank, wordnet 等语料库

需要自行下载 stanford parser 并修改相关参数

还需要使用剑桥高级学习词典(CALD)语料库作为例句的来源，此库不在 nltk 上，需要自行下载并处理


# 代码说明

核心算法都在 generator.py 文件中，该文件函数结构：

	generator.py
	|-- get_synonym(w)  # 得到 w 的同义词序列
	|-- get_sentences(w)  # 得到含有单词 w 的句子序列
	|-- get_complexity_score(sens)  # 计算句子序列中每一个句子的复杂性得分
	|-- get_context_score(sens)  # 计算句子序列中每一个句子的上下文得分
	|
	|-- get_grammar_score(sens, w)  # 计算句子序列中每一个句子的语法得分
	|-- get_length_score(sens)  # 计算句子序列中每一个句子的长度得分
	|
	|-- get_distracts(sen, w)  # 得到针对句子 sen 和单词 w 的干扰项序列
	|
	|-- main  # 一个运行函数，可以在终端运行并输出找到的句子序列、
			  # 每个句子的得分、干扰项排序、生成的题目等

一个简单的 GUI 代码在 gui.py 中

# 重要代码注释

1) 使用 stanford parser 得到的子句数评估句子的复杂性

	parser = stanford.StanfordParser(model_path="E:\stanfordParser\englishPCFG.ser.gz")  # 导入斯坦福解析器
	ss = []
	for sen in sens:
    	score_complexity = 1  # 句子初始得分为1
		parse = parser.raw_parse(sen)
		tree = list(parse)[0]  # 得到句子成分分析树
		for tr in tree.subtrees()
			......
		ss.append(score_complexity)

类似的，也可以评估语法得分

2) 得到干扰项

	words_fre = []
    temp = sen.split(" ")  # 拆分句子到单词序列
    word_tag = dict(nltk.pos_tag(temp))  # 得到每个单词词性
    temp.remove(w)  # 去除原始单词
    for n in temp:
        if word_tag[n] in conf.contexts:  # 只分析有意义的单词
            words_fre += get_frequent_words(n)  # 得到干扰项及其得分
    words_fre = sorted(words_fre, key=lambda item: item[1], reverse=True)  # 按照得分排序
    words_fre = [x for x in words_fre if x not in conf.stopwords]  # 移除停用词
    return [words_fre[x][0] for x in range(0, min(3, len(words_fre)))]  # 返回前三名
