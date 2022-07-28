from snownlp import sentiment
# 训练语料库
sentiment.train('neg.txt', 'text_corpus/pos.txt')
sentiment.save('text_corpus/weibo.marshal')