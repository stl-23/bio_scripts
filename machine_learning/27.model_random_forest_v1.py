#!/bionfsdate/Software/Anaconda3/bin/python
# -*- coding: utf-8 -*-
# author：lukang time:2021/4/20
"""
20210520:
output train and test dataset true label and predict score to file
v0.7.1:
remove feature selection

v0.7: feature selection in train datasets
method: Use SelectFromModel packages to select methy features which importance above average level

v0.6.1:
1. change input : from 2 files (feature and label) to 1 file (feature + lable)
2. change RepeatedKFold to RepeatedStraitifiedKFold

v0.6: add save model function

Change Validation method to 10 fold cross validation

Random Forest Classifieer for DZ methylation data
"""

import numpy as np
from argparse import ArgumentParser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold
from sklearn.feature_selection import SelectFromModel
from collections import defaultdict
import pickle


def get_best_youden_index(y, y_predict, prefix):
    fpr, tpr, thresholds = roc_curve(y, y_predict)
    sensitivity = tpr
    specificity = 1 - fpr
    df = pd.DataFrame(list(zip(*[list(sensitivity), list(specificity), list(thresholds)])), columns=['sensitivity_validation', 'specificity_validation', 'thresholds'])
    df['youden_index'] = sensitivity + specificity - 1
    df.to_csv('{}_performance_detail.xls'.format(prefix), sep='\t', index=False)
    index = [df.loc[df['specificity_validation']>=0.93, :].index[-1]]
    index.append(df.loc[df['specificity_validation']>=0.95, :].index[-1])
    index.append(df.loc[df['specificity_validation']>=0.98, :].index[-1])
    df_filter = df.loc[index, :]
    return df_filter


def roc_plot(y, y_predict, output):
    fpr, tpr, thresholds = roc_curve(y, y_predict)
    auc_score = roc_auc_score(y, y_predict)
    plt.clf()
    plt.plot(fpr, tpr,  lw=2, alpha=0.7, label='AUC=%.3f' % auc_score)
    plt.plot((0, 1), (0, 1), c='#808080', lw=1, ls='--', alpha=0.7)
    plt.xlim((-0.02, 1.02))
    plt.ylim((-0.02, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('1 - Specificity', fontsize=13)
    plt.ylabel('Sensitivity', fontsize=13)
    plt.grid(b=True, ls=':')
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    title = output.split('/')[-1]
    plt.title(title, fontsize=17)
    plt.savefig(f'{output}.png')
    return auc_score

def predict_prob_10fold(train_df):
    X_train = train_df.iloc[:, :-1]
    y_train = train_df.iloc[:, -1]
    d_valid_prob = defaultdict(list)
    rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=234)
    for train_index, valid_index in rskf.split(X_train, y_train):
        X_train1, y_train1 = X_train.iloc[train_index, :], y_train.iloc[train_index]
        X_valid , y_valid  = X_train.iloc[valid_index, :], y_train.iloc[valid_index]
        clf = RandomForestClassifier()
        clf.fit(X_train1, y_train1)
        y_valid_predict = clf.predict_proba(X_valid)[:, 1]
        for i, j in zip(X_valid.index, y_valid_predict): d_valid_prob[i].append(j)
    valid_df = pd.DataFrame(d_valid_prob).T
    valid_df['label_predict'] = valid_df.mean(1)
    valid_df = pd.concat([valid_df, y_train], axis=1)
    return valid_df

def predict_prob(train_df, test_df, outdir):
    clf = RandomForestClassifier()
    clf.fit(train_df.iloc[:,:-1], train_df.iloc[:,-1])
    module_pkl = open('{}/random_forest.pkl'.format(outdir), 'wb')
    pickle.dump(clf, module_pkl)
    y_test_predict = clf.predict_proba(test_df.iloc[:,:-1])[:, 1]
    test_df['label_predict'] = y_test_predict
    return test_df.loc[:,['sample_label', 'label_predict']]

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--train_data",action="store",dest="train_data",help="")
    parser.add_argument('--test_data',action="store",dest="test_data",help='')
    parser.add_argument("--outdir",action="store",dest="outdir",help="")
    args = parser.parse_args()
    return args


def calculate_metric(real, pred, df_filter, prefix):
    sensitivitys, specificitys, accuracys = [], [], []
    for cutoff in df_filter['thresholds']:
        pred1 = pred.copy()
        pred1[pred1>cutoff]=1
        pred1[pred1<1]=0
        confusion = confusion_matrix(real, pred1)
        TP = confusion[1, 1]
        TN = confusion[0, 0]
        FP = confusion[0, 1]
        FN = confusion[1, 0]
        sensitivity = TP / float(TP+FN)
        specificity = TN / float(TN+FP)
        accuracy = (TP+TN)/float(TP+TN+FP+FN)
        sensitivitys.append(sensitivity)
        specificitys.append(specificity)
        accuracys.append(accuracy)
    df_filter['sensitivity_{}'.format(prefix)] = sensitivitys
    df_filter['specificity_{}'.format(prefix)] = specificitys
    df_filter['accuracy_{}'.format(prefix)] = accuracys
    return df_filter

def main():
    args = parse_args()
    outdir = args.outdir

    train_df = pd.read_csv(args.train_data, index_col=0, sep=',')
    test_df = pd.read_csv(args.test_data, index_col=0, sep=',')
    #train_df     = train_df.replace(np.inf, 1.5)
    #train_df     = train_df.fillna(value=1)
    #test_df      = test_df.replace(np.inf, 1.5)
    #test_df      = test_df.fillna(value=1)

    valid_df = predict_prob_10fold(train_df)

    valid_auc_score = roc_plot(valid_df["sample_label"], valid_df["label_predict"], '{}/validation_ROC'.format(outdir))
    df_filter = get_best_youden_index(valid_df["sample_label"], valid_df["label_predict"], '{}/validation'.format(outdir))

    test_df_label= predict_prob(train_df, test_df, outdir)
    test_auc_score = roc_plot(test_df_label["sample_label"], test_df_label['label_predict'], '{}/test_ROC'.format(outdir))
    df_filter = calculate_metric(test_df_label["sample_label"], test_df_label['label_predict'], df_filter, 'test')

    valid_df.to_csv('{}/validation_score.xls'.format(args.outdir), sep='\t')
    test_df_label.to_csv('{}/test_score.xls'.format(args.outdir), sep='\t')
    auc_score = pd.DataFrame()    
    auc_score.loc['validation', 'auc'] = valid_auc_score
    auc_score.loc['test', 'auc'] = test_auc_score
    auc_score.to_csv('{}/auc.xls'.format(args.outdir), sep='\t')
    df_filter.to_csv('{}/performace.xls'.format(args.outdir), sep='\t', index=False)

if __name__ == '__main__':
    main()
