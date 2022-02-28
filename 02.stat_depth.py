#!/usr/bin/python
# -*- coding:utf-8 -*-
#lvli
import os
import sys
from argparse import ArgumentParser
import pandas as pd


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--depth",action="store",dest="depth",help="")
    parser.add_argument("--outdir",action="store",dest="outdir",help="")
    args = parser.parse_args()
    return args

def trans_depth(depth_df_enzy, depth_path, cut_type):
    depth_df_enzy = depth_df_enzy.drop(['id', 'batch', '酶切'], axis = 1).set_index('#primer')
    depth_df_enzy_T = depth_df_enzy.T
    depth_df_enzy_T.to_csv(f'{depth_path}/depth_{cut_type}', sep = '\t', index_label = '#primer')
    return depth_df_enzy_T

def extract_depth(args):
    depth_path = os.path.abspath(os.path.dirname(args.depth))
    depth = pd.read_csv(args.depth, sep = '\t', dtype = object)
    depth_group = depth.groupby('id')
    depth_df = depth_group.get_group('depth')
    #将depth数据框分为双酶切和单酶切
    depth_df_double_enzy = depth_df[depth_df['酶切'] == '双酶切']
    depth_df_single_enzy = depth_df[depth_df['酶切'] == '单酶切']

    depth_df_double_enzy_T = trans_depth(depth_df_double_enzy, depth_path, 'double_enzy')
    depth_df_single_enzy_T = trans_depth(depth_df_single_enzy, depth_path, 'single_enzy')
    return depth_df_double_enzy_T, depth_df_single_enzy_T

def compute_quantile(depth_df_enzy, cut_type, args):
    depth_df_enzy = depth_df_enzy.astype(int)
    depth_percentile = depth_df_enzy.quantile([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9], axis = 1).T
    merged = depth_df_enzy.join(depth_percentile, how = 'inner')
    print(merged)
    merged.to_csv(f'{args.outdir}/depth_{cut_type}_stat.xls', sep = '\t', index_label = '#primer')
    return

def stat_depth(args):
    depth_df_double_enzy_T, depth_df_single_enzy_T = extract_depth(args)
    print(depth_df_double_enzy_T)
    print(depth_df_single_enzy_T)
    compute_quantile(depth_df_double_enzy_T, 'double_enzy', args)
    compute_quantile(depth_df_single_enzy_T, 'single_enzy', args)
    return

def main():
    args = parse_args()
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    stat_depth(args)

if __name__ == "__main__":
    main()
