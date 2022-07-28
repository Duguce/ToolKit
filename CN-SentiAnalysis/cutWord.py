# -*- coding: utf-8  -*-
import jieba
import jieba.analyse
import re
import settings


def clearTxt(text):
    """
    对文本内容进行清洗，删除英文、数字和符号
    :param text: 文本内容
    :return:text-清洗后的行数据
    """
    if text != '':
        text = text.strip()
        text = text.encode("utf-8").decode("utf-8")
        text = re.sub("[a-zA-Z0-9]", "", text)  # 去除文本中的英文和数字
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", text)  # 去除文本中的各类符号
    return text


def sent2word(text):
    """
    对文本内容进行分割
    :param text: 文本内容
    :return: segSentence.strip()-分割后的文本内容
    """
    segList = jieba.cut(text, cut_all=False)
    segSentence = ''.join(f"{word} " for word in segList if word != '\t')
    return segSentence.strip()


def stopwordsList(filepath):
    """
    创建停用词列表
    :param filepath: 停用词文件所在的路径
    :return: stopwords-停用词列表
    """
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def delstopword(text, stopwords):
    """
    删除停用词
    :param text: 原始文本
    :param stopwords: 停用词列表
    :return: 无
    """
    wordList = text.split(' ')
    sentence = ''
    for word in wordList:
        word = word.strip()
        if word not in stopwords and word != '\t':
            sentence += f"{word} "
    return sentence.strip()


def cutWord(sourcefile, targetfile, stopwords):
    """
    对输入数据进行文本分词
    :param sourcefile:输入文本文件
    :param targetfile:输出文本文件
    :param stopwords:停用词列表
    :return: 无
    """
    source = open(sourcefile, 'r')
    with open(targetfile, 'w', encoding='utf-8') as target:
        line = source.readline()
        while line:
            line = clearTxt(line)
            seg_line = sent2word(line)
            seg_line = delstopword(seg_line, stopwords)
            target.writelines(seg_line + "\n")
            line = source.readline()
        print(f"{sourcefile} 分词成功...")
        source.close()


if __name__ == '__main__':
    stopwordsPath = settings.staticDir + 'stopwords.txt'
    stopwords = stopwordsList(stopwordsPath)

    inputs = settings.corpusDir + 'neg.txt'
    outputs = settings.sourceData + 'neg_cut.txt'
    cutWord(inputs, outputs, stopwords)

    inputs = settings.corpusDir + 'pos.txt'
    outputs = settings.sourceData + 'pos_cut.txt'
    cutWord(inputs, outputs, stopwords)
