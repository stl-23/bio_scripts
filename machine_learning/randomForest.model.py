#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Author    : fangj
## FileName  : randomForest.model.py
## CreateTime: 2021-12-21  14:45:17

import numpy as np
import pandas as pd
from collections import Counter
import argparse
import sys
import os

import sklearn.ensemble 
import sklearn.model_selection
from sklearn.model_selection import GridSearchCV

## 模型评估
import sklearn.metrics as metrics
import sklearn.metrics as accuracy_score
from sklearn.metrics import confusion_matrix


usage = '''
Description:
    Designed for......!!!
Example: 
    python  %s  -h
    
''' % (__file__[__file__.rfind(os.sep) + 1:])

# 用于服务器中建模测试 
# 参考路径： /sxyf_keyan2020/01.yanfa/30.gene_structure_analysis/17.merge.result_v3_5MB/09.model/02.model_use5MB_allFeature/00.nocut_data
# 输入train file ,testfile 即可;
# n_estimators 决策树个数;

class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def get_df(args):
    # get train data
    traindf = pd.read_csv(args.trainfile,sep='\t',header=0,index_col=0,low_memory=False)
    # get test data
    testdf = pd.read_csv(args.testfile,sep='\t',header=0,index_col=0,low_memory=False)
    # split train data
    y = traindf["class"]
    X = traindf.iloc[:,1:]  # 第一列为label标签；
    X_train = X
    y_train = y
    # split test data
    y_exam = testdf["class"]
    X_exam = testdf.iloc[:,1:]  # 第一列为label标签；
    X_test = X_exam
    y_test = y_exam
    return X_train,y_train,X_test,y_test

def predict_model(args):
    X_train,y_train,X_test,y_test = get_df(args)
    param_grid = {
    #'n_estimators':[80,100,150,180,200],  # 决策树个数，即基评估器的数量-随机森林特有参数
    'n_estimators':[args.n_estimators],}
    #rfc =sklearn.ensemble.RandomForestClassifier()
    rfc_cv = GridSearchCV(estimator=sklearn.ensemble.RandomForestClassifier(random_state=1),
                            param_grid=param_grid,scoring='roc_auc', cv=5)
    rfc_cv.fit(X_train, y_train)
    
    y_pred = rfc_cv.predict(X_test)
    y_proba = rfc_cv.predict_proba(X_test)
    acc = metrics.accuracy_score(y_test, y_pred)
    p = metrics.precision_score(y_test, y_pred)
    r = metrics.recall_score(y_test, y_pred)
    f1 = metrics.f1_score(y_test, y_pred)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_proba[:, 1])
    auc = metrics.auc(fpr, tpr)

    print(acc,auc)

    cm = confusion_matrix(y_test, y_pred)  # y_test 真实label;y_pred 分类器的预测分类；

    TP = cm[1,1]
    TN = cm[0,0]
    FP = cm[0,1]
    FN = cm[1,0]

    # print(TN,FP,FN,TP)
    # tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    # print(tn, fp, fn, tp)

    accuracy = (TP + TN)/float(TP+TN+FP+FN)
    sensitivity = TP/float(TP+FN)    # 
    specificity = TN/float(TN+FP)    # 

    #print("#准确度\t灵敏度\t特异度\tAuc")
    print("#accuracy\tsensitivity\tspecificity\tAuc")
    print(accuracy,sensitivity,specificity,auc)

##### ARGS #####
def options():
    parser = argparse.ArgumentParser(formatter_class=HelpFormatter,description=usage)
    parser.add_argument('-trainfile', help='input train file', dest='trainfile', type=str, action='store', required=True)
    parser.add_argument('-testfile', help='input test file', dest='testfile', type=str, action='store', required=True)
    parser.add_argument('-n_estimators', help='input n_estimators numbers', dest='n_estimators', type=int, action='store', default=1000)
    #parser.add_argument('-out', help='output file', dest='out', type=str, action='store', default="tmp.out.csv")
    #parser.add_argument('-sample', help='input sample name', dest='sample', type=str, action='store', default="test")
    #parser.add_argument('-out', help='output csv file', dest='out', type=str, action='store', default="out.csv")
    args = parser.parse_args()
    return args

def main():
    args = options()
    predict_model(args)

if __name__ == '__main__':
    try:
        #s_time=StartTime()
        main()
        #EndTime(s_time)
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)