from sklearn.metrics import roc_curve, roc_auc_score
import pandas as pd
from statsmodels.stats.multitest import fdrcorrection
from scipy import stats
#from itertools import combinations
#from decimal import Decimal,ROUND_HALF_UP
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
    parser.add_argument("--loop",type=int,default=10,help="")
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
def select(df_cancer_all, df_normal_all, num):
    #df_cancer_orgin = pd.read_csv(cancer_file, sep = '\t', skiprows=1, header=None, index_col=0).dropna(axis=0)
    #df_normal_orgin = pd.read_csv(normal_file, sep = '\t', skiprows=1, header=None, index_col=0).dropna(axis=0)
    #cancer_samples = list(df_cancer_all.columns.values)
    #normal_samples = list(df_normal_all.columns.values)
    #cancer_num = int(df_cancer_all.shape[1])*0.8
    #cancer_num_new = Decimal(str(cancer_num)).quantize(Decimal('0.'), rounding=ROUND_HALF_UP)
    #normal_num = int(df_normal_all.shape[1])*0.8
    #normal_num_new = Decimal(str(normal_num)).quantize(Decimal('0.'), rounding=ROUND_HALF_UP)
    #cancer_com = list(combinations(cancer_samples,int(cancer_num_new)))
    #normal_com = list(combinations(normal_samples,int(normal_num_new)))
    #df_cancer_select = df_cancer_all.iloc[:,list(cancer_com[num])]
    #df_normal_select = df_normal_all.iloc[:,list(normal_com[num])]
    #print(str(df_cancer_all.shape[1]))
    df_cancer_select = df_cancer_all.sample(frac=0.8,axis=1,random_state=num)
    df_normal_select = df_normal_all.sample(frac=0.8,axis=1,random_state=num)
    return df_cancer_select,df_normal_select

def rank_sum_test(cancer_file, normal_file,loop_num):
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
    df_cancer_all = df_cancer_origin[df_cancer_origin.index.isin(overlap)]
    #print('cancer')
    #print(df_cancer)
    df_normal_all = df_normal_origin[df_normal_origin.index.isin(overlap)]
    #print('normal')
    #print(df_normal)
    i = 0
    result = {}
    while i < loop_num:
        df_cancer,df_normal = select(df_cancer_all, df_normal_all, i)
        df_cancer_median, df_normal_median = df_cancer.median(1), df_normal.median(1)
        df_cancer_mean, df_normal_mean = df_cancer.mean(axis=1), df_normal.mean(axis=1)
        df_normal_median.replace(0, 0.00001, inplace=True)
        df_normal_mean.replace(0, 0.00001, inplace=True)
        median_fold_change = df_cancer_median/df_normal_median
        mean_fold_change = df_cancer_mean/df_normal_mean
        median_diff = df_cancer_median - df_normal_median
        mean_diff = df_cancer_mean - df_normal_mean
        p_value = []
        #label = [1]*df_cancer.shape[1] + [0]*df_normal.shape[1]
        #label_rev = [0]*df_cancer.shape[1] + [1]*df_normal.shape[1]
        #p_value, above_max_ratio, below_min_ratio, auc, sen = [], [], [], [], []
    # print(df_cancer)
    # print(df_cancer.index)
        for index in df_cancer.index.tolist():
            feature = df_cancer.loc[index, :].tolist() + df_normal.loc[index, :].tolist()
            if len(list(set(feature)))==1:
                p_value.append(1)
            else:
                p_value.append(stats.mannwhitneyu(df_cancer.loc[index,:], df_normal.loc[index,:])[1])
        #result.update({'foldchange_'+str(i): fold_change,'median_diff_'+str(i):median_diff,'mean_diff_'+str(i):mean_diff,'pvalue_'+str(i):p_value})
        result.update({'mean_foldchange'+str(i):mean_fold_change,'mean_diff'+str(i):mean_diff,'median_foldchange'+str(i): median_fold_change, 'median_diff'+str(i):median_diff, 'cancer_median'+str(i):df_cancer_median,'normal_median'+str(i): df_normal_median,'cancer_mean'+str(i):df_cancer_mean,'normal_mean'+str(i):df_normal_mean,'pvalue'+str(i): p_value})
        i+=1
    out_data = pd.DataFrame(result)
    out_data.index.name = 'id'
    #print(result)
    return out_data

def main():
    args = parse_args()
    global outdir
    cancer_file, normal_file, loop, outfile= args.cancer, args.normal, int(args.loop), args.outfile
    result_df = rank_sum_test(cancer_file, normal_file,loop)
    result_df.to_csv(outfile, sep = '\t')

if __name__ == "__main__":
    main()
