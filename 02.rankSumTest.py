from sklearn.metrics import roc_curve, roc_auc_score
import pandas as pd
from statsmodels.stats.multitest import fdrcorrection
from scipy import stats

#!/usr/bin/python
# -*- coding:utf-8 -*-
#lvli
import os
import sys
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--cancer",action="store",dest="cancer",help="", default="")
    parser.add_argument("--normal",action="store",dest="normal",help="", default="")
    parser.add_argument("--outfile",action="store",dest="outfile",help="",default='')
    args = parser.parse_args()
    return args

def rm_minus_one_value(df):
    rm_index = []
    for index, row in df.iterrows():
        if -1 in row.values:
            rm_index.append(index)
    df_after_rm = df[~(df.index.isin(rm_index))]
    #print(df_after_rm)
    return df_after_rm

def rank_sum_test(cancer_file, normal_file):
    df_cancer_first = pd.read_csv(cancer_file, sep = '\t', skiprows=1, header=None, index_col=0).dropna(axis=0)
    #print(df_cancer_first)
    df_cancer_origin = df_cancer_first
    #df_cancer_origin = rm_minus_one_value(df_cancer_first)
    cancer_list = df_cancer_origin.index.tolist()

    df_normal_first = pd.read_csv(normal_file, sep = '\t', skiprows=1, header=None, index_col=0).dropna(axis=0)
    #print(df_normal_first)
    #df_normal_origin = rm_minus_one_value(df_normal_first)
    df_normal_origin = df_normal_first
    normal_list = df_normal_origin.index.tolist()

    overlap = list(set(cancer_list).intersection(set(normal_list)))
    df_cancer = df_cancer_origin[df_cancer_origin.index.isin(overlap)]
    #print('cancer')
    #print(df_cancer)
    df_normal = df_normal_origin[df_normal_origin.index.isin(overlap)]
    #print('normal')
    #print(df_normal)

    df_cancer_median, df_normal_median = df_cancer.median(1), df_normal.median(1)
    df_cancer_mean, df_normal_mean = df_cancer.mean(1), df_normal.mean(1)
    df_normal_median.replace(0, 0.00001, inplace=True)
    df_normal_mean.replace(0, 0.00001, inplace=True)
    median_fold_change = df_cancer_median/df_normal_median
    mean_fold_change = df_cancer_mean/df_normal_mean
    median_diff = df_cancer_median - df_normal_median
    mean_diff = df_cancer_mean - df_normal_mean
    label = [1]*df_cancer.shape[1] + [0]*df_normal.shape[1]
    label_rev = [0]*df_cancer.shape[1] + [1]*df_normal.shape[1]
    p_value, above_max_ratio, below_min_ratio, auc, sen = [], [], [], [], []
    # print(df_cancer)
    # print(df_cancer.index)
    for index in df_cancer.index.tolist():
        cancer_value = df_cancer.loc[index,:]
        normal_value = df_normal.loc[index,:]
        normal_max_value, normal_min_value = normal_value.max(), normal_value.min()
        above_max_ratio_i = (cancer_value>normal_max_value).sum()/len(cancer_value)
        below_min_ratio_i = (cancer_value<normal_min_value).sum()/len(cancer_value)
        above_max_ratio.append(above_max_ratio_i)
        below_min_ratio.append(below_min_ratio_i)
        feature = df_cancer.loc[index, :].tolist() + df_normal.loc[index, :].tolist()
        # print(feature)
        auc_index = roc_auc_score(label, feature)
        fpr, tpr, thresholds = roc_curve(label, feature)
        if auc_index < 0.5:
            auc_index = roc_auc_score(label_rev, feature)
            fpr, tpr, thresholds = roc_curve(label_rev, feature)
        auc.append(auc_index)
        sensitivity, specificity = tpr, 1-fpr
        cc = pd.DataFrame([specificity, sensitivity], index=['spe', 'sen']).T
        cc = cc.loc[cc['spe']>=0.95,:]
        #print(cc)
        if not cc.empty:
            sen_i = cc.iloc[cc.shape[0]-1, 1]
        else:
            sen_i = 0
        sen.append(sen_i)
        if len(list(set(feature)))==1:
            p_value.append(1)
        else:
            p_value.append(stats.mannwhitneyu(df_cancer.loc[index,:], df_normal.loc[index,:])[1])
    fdr = fdrcorrection(p_value)[1]
    result = pd.DataFrame({'mean_foldchange':mean_fold_change,'mean_diff':mean_diff,'median_foldchange': median_fold_change, 'median_diff':median_diff, 'cancer_median':df_cancer_median,'normal_median': df_normal_median,'cancer_mean':df_cancer_median,'normal_mean':df_normal_mean,'pvalue': p_value, 'fdr':fdr, 'sen':sen, 'auc':auc})
    #result.index.names = ['id']
    result.index.name = 'id'
    #print(result)
    return result

def main():
    args = parse_args()
    global outdir
    cancer_file, normal_file, outfile= args.cancer, args.normal, args.outfile
    result_df = rank_sum_test(cancer_file, normal_file)
    result_df.to_csv(outfile, sep = '\t')

if __name__ == "__main__":
    main()
