# CN-SentiAnalysis
中文文本情况分类实验

| 序号 |     项目名称     |                      备注                      |
| :--: | :--------------: | :--------------------------------------------: |
|  1   |      corpus      |          用于输入的原始语料存放文件夹          |
|  2   |     dstData      |              输出结果的存放文件夹              |
|  3   |     srcData      | 用于分类输入数据文件夹（分词后及向量化的语料） |
|  4   |      static      |             标准文件（eg.停用词）              |
|  5   |    cutWord.py    |    基于jieba对原始语料进行分词并去除停用词     |
|  6   |   word2vec.py    |      基于word2vec对分词后的语料进行向量化      |
|  7   |      svm.py      |      基于svm对向量化后的语料进行情感分类       |
|  8   | requirements.txt |         该项目所涉及到的第三方模块版本         |

注：编程实现基于Python3.7

**项目简述**

- **项目概况**
  - 本项目是利用机器学习方法训练已经标注好情感类别的训练数据集训练分类模型，再通过分类模型预测文本所属的情感分类。
- **运行步骤**
  - 运行cutWord.py（中文文本分词）==>运行word2vec.py（词向量化）==>运行svm.py（文本分类）
- **运行结果**
  - 运行代码，得到的Test Accuracy：0.90，即本次实验的预测准确率为90%
- **其他备注**
  - 本项目使用的训练好的词向量来自于https://github.com/Embedding/Chinese-Word-Vectors



**项目地址：** https://github.com/Duguce/my_gadgets/tree/main/CN-SentiAnalysis
