#!/sxyf_keyan/01.yanfa/18.methy_panCancer/00.script/02.software/miniconca3/bin/python
# -*- coding: UTF-8 -*-

## Author    : fangjian
## FileName  : randomForest.classifier.model.v1.py
## CreateTime: 2022-02-17  11:35:38

import argparse
import sys
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
from sklearn.model_selection import RepeatedStratifiedKFold
from collections import defaultdict
import pickle
import matplotlib.pyplot as plt

usage = '''
Description:
    Designed for random forest classifier modeling!!!
Example: 
    python  %s  -h
    
''' % (__file__[__file__.rfind(os.sep) + 1:])

'''
输入文件格式：
#sample  class   feature1    feature2    feature3
sample1  1       numbers1    numbers2    numbers3
sample2  0       numbers4    numbers5    numbers6
'''
'''
v1 版
随机森林建模;十折交叉验证; Auc,Sen,Spe; ROC曲线;导出model
python 路径:  /sxyf_keyan/01.yanfa/18.methy_panCancer/00.script/02.software/miniconca3/bin/python
---------------------
v2 版
ing......
'''
class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def split_df(train_data,test_data):
    '''
    划分数据集，将feature与label 分开；其中X表示feature,y表示label,train表示训练集，test表示测试集
    '''
    # get train data
    train_df = pd.read_csv(train_data,sep='\t',header=0,index_col=0,low_memory=False)
    # get test data
    test_df = pd.read_csv(test_data,sep='\t',header=0,index_col=0,low_memory=False)
    # split train data
    X_train = train_df.iloc[:,1:]   # 第一列为label标签；
    y_train = train_df["class"]
    # split test data
    y_test = test_df["class"]
    X_test = test_df.iloc[:,1:]     # 第一列为label标签；
    return X_train,y_train,X_test,y_test

def train_10fold_cross_validation(X_train,y_train,prefix,n_estimators_num,outdir):
    '''
    训练集十折交叉验证
    '''
    X = X_train
    y = y_train
    test_proba_list = defaultdict(list)
    rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=234)
    rf = RandomForestClassifier(n_estimators= n_estimators_num, random_state= 1)    # 可以适当修改n_estimators
    for train_index, test_index in rskf.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        rf.fit(X_train,y_train)
        y_proba = rf.predict_proba(X_test)[:,1]
        for i, j in zip(X_test.index, y_proba): test_proba_list[i].append(j)
    train_score_df = pd.DataFrame(test_proba_list).T
    train_score_df["predict_score_mean"] = train_score_df.mean(1)
    train_score_class_df = pd.concat([train_score_df,y],axis = 1)
    train_score_class_df.to_csv("{0}/{1}.train.predict.score.csv".format(outdir,prefix),sep="\t",index=True)
    auc_score = roc_auc_score(train_score_class_df["class"],train_score_class_df["predict_score_mean"])   ## 注意标签对应
    print("10fole Auc:%f"%(auc_score))
    return train_score_class_df,auc_score

def get_best_youden_index(y, y_predict):
    '''
    通过yueden指数，找最佳阈值；
    '''
    fpr, tpr, thresholds = roc_curve(y, y_predict)
    #auc = metrics.auc(fpr, tpr)
    y = tpr - fpr
    youden_index_number = np.argmax(y)
    optimal_threshold = thresholds[youden_index_number]
    #point = [fpr[youden_index_number],tpr[youden_index_number]]
    youden_index = y[youden_index_number]
    return optimal_threshold,youden_index

def predict_prob(X_train, y_train,X_test,y_test,n_estimators_num,prefix,outdir):
    '''
    随机森林建模，预测
    '''
    clf = RandomForestClassifier(n_estimators= n_estimators_num, random_state= 1)
    clf.fit(X_train, y_train)
    module_pkl = open('{0}/{1}.random.forest.pkl'.format(outdir,prefix), 'wb')
    pickle.dump(clf, module_pkl)
    y_proba = clf.predict_proba(X_test)
    y_proba_df = pd.DataFrame(y_proba,index = y_test.index,columns = ["score1","score2"])   # right
    y_proba_class_df = pd.concat([y_test,y_proba_df],axis = 1)
    # fpr, tpr, thresholds = roc_curve(y_test, y_proba[:, 1])
    # auc = sklearn.metrics.auc(fpr, tpr)
    # acc = accuracy_score(y_test, y_proba[:, 1])
    auc_score = roc_auc_score(y_test, y_proba[:, 1])
    print("predict auc :%s"%(auc_score))
    y_proba_class_df.to_csv('{0}/{1}.test.predict.score.xls'.format(outdir,prefix), sep='\t')
    return y_proba_class_df,auc_score

def calculate_metric(y_test, y_predict, optimal_threshold,youden_index,auc_score):
    '''
    根据最佳阈值，计算灵敏度，特异度，准确度等
    '''
    index_count_df = pd.DataFrame()
    cutoff = optimal_threshold
    pred_copy = y_predict.copy()
    pred_copy[pred_copy>=cutoff] = 1   # 是否等于？
    pred_copy[pred_copy<cutoff] = 0
    confusion = confusion_matrix(y_test, pred_copy)
    TP = confusion[1, 1]
    TN = confusion[0, 0]
    FP = confusion[0, 1]
    FN = confusion[1, 0]
    sensitivity = TP / float(TP+FN)
    specificity = TN / float(TN+FP)
    accuracy = (TP+TN)/float(TP+TN+FP+FN)
    index_count_df["sensitivity"] = [sensitivity]
    index_count_df["specificity"] = [specificity]
    index_count_df["accuracy"] = [accuracy]
    index_count_df["optimal_threshold"] = [optimal_threshold]   
    index_count_df["youden_index"] = [youden_index]
    index_count_df["test_auc"] = [auc_score]
    #index_count_df.to_csv('{0}/{1}.index.count.xls'.format(outdir,prefix), sep='\t',index=False)
    return index_count_df

def roc_plot(y, y_predict,prefix,outdir,type):
    '''
    ROC曲线
    '''
    fpr, tpr, thresholds = roc_curve(y, y_predict)
    auc_score = roc_auc_score(y, y_predict)
    plt.clf()
    plt.plot(fpr, tpr,  lw=2, alpha=0.7, label='AUC=%.4f' %(auc_score))
    plt.plot((0, 1), (0, 1), c='#808080', lw=1, ls='--', alpha=0.7)
    plt.xlim((-0.02, 1.02))
    plt.ylim((-0.02, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('1 - Specificity', fontsize=13)
    plt.ylabel('Sensitivity', fontsize=13)
    #plt.grid(b=True, ls=':')  ## MatplotlibDeprecationWarning,版本低
    visible = True
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    title = "{0}.{1}.ROC_Auc".format(prefix,type)
    plt.title(title, fontsize=17)
    plt.savefig("{0}/{1}.{2}.ROC.png".format(outdir,prefix,type))
    print("plot auc: %s"%(auc_score))

def make_dir(dirname):
    dirname = os.path.abspath(dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

##### ARGS #####
def options():
    parser = argparse.ArgumentParser(formatter_class=HelpFormatter,description=usage)
    parser.add_argument('-trainfile', help='input train file', dest='trainfile', type=str, action='store', required=True)
    parser.add_argument('-testfile', help='input test file', dest='testfile', type=str, action='store', required=True)
    parser.add_argument('-n_estimators', help='input random rorest n_estimators numbers', dest='n_estimators', type=int, action='store', default=100)
    parser.add_argument('-outdir', help='output directory', dest='outdir', type=str, action='store', default="./out.rf.model.result")
    parser.add_argument('-prefix', help='the prefix of output file name', dest='prefix', type=str, action='store', default="tmp")
    parser.add_argument('-fold10', help='whether to 10 fold cross validate[T,F]', dest='fold10', type=str, action='store', default="F")
    args = parser.parse_args()
    return args

def main():
    args = options()
    train_data = args.trainfile  
    test_data = args.testfile      
    outdir = make_dir(args.outdir)        # 结果输出目录
    prefix = args.prefix                  # 文件前缀
    n_estimators_num = args.n_estimators

    X_train,y_train,X_test,y_test = split_df(train_data,test_data)
    y_proba_class_df,auc_score = predict_prob(X_train, y_train,X_test,y_test,n_estimators_num,prefix,outdir)
    optimal_threshold,youden_index = get_best_youden_index(y_proba_class_df["class"],y_proba_class_df["score2"])
    index_count_df = calculate_metric(y_test,y_proba_class_df["score2"], optimal_threshold,youden_index,auc_score)  # youden_index,auc_score 仅用于输出
    roc_plot(y_test,y_proba_class_df["score2"],prefix,outdir,"test")

    index_count_df["n_estimators"] = n_estimators_num


    ## 是否进行 10fold_cross_validation
    if args.fold10 == "T":
        train_score_class_df,train_auc_score = train_10fold_cross_validation(X_train,y_train,prefix,n_estimators_num,outdir)
        roc_plot(train_score_class_df["class"],train_score_class_df["predict_score_mean"],prefix,outdir,"train")

    try:    ## 判断是否进行了交叉验证
        train_auc_score
    except NameError:
        index_count_df.to_csv('{0}/{1}.index.count.xls'.format(outdir,prefix), sep='\t',index=False)
    else:
        index_count_df["train_auc"] = train_auc_score
        index_count_df.to_csv('{0}/{1}.index.count.xls'.format(outdir,prefix), sep='\t',index=False)
    print(index_count_df)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
