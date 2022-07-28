# -*- coding: utf-8  -*-
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import metrics
import settings


def main():
    df = pd.read_csv(r'srcData//vecData.csv')
    y = df.iloc[:, 1]
    x = df.iloc[:, 2:]
    clf = svm.SVC(C=2, probability=True)
    clf.fit(x, y)
    print("Test Accuracy: {:.2f}%".format(clf.score(x, y)))
    pred_probas = clf.predict_proba(x)[:, 1]
    fpr, tpr, _ = metrics.roc_curve(y, pred_probas)
    roc_auc = metrics.auc(fpr, tpr)
    plt.plot(fpr, tpr, label='area = %.2f' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.legend(loc='lower right')
    plt.show()
    outputPath = f'{settings.dstData}area figure'
    plt.savefig(outputPath)


if __name__ == '__main__':
    main()
