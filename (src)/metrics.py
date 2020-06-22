import pandas as pd
import numpy as np


def precision(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    flags = np.isin(bought_list, recommended_list)
    return flags.sum() / len(recommended_list)


def precision_at_k(recommended_list=[], bought_list=[], k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    
    flags = np.isin(recommended_list, bought_list)
    
    return flags.sum() / len(recommended_list)


def precision_at_k_series(df, rec_col, bought_col, k=5):
    df = df[[rec_col, bought_col]].copy()
    df['zip'] = list(zip(df[rec_col], df[bought_col]))
    df['p@k'] = df['zip'].map(lambda zp: precision_at_k(recommended_list=list(zp[0]), bought_list=list(zp[1]), k=k))
    
    return df['p@k']


def recall(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)

    flags = np.isin(bought_list, recommended_list)

    recall = flags.sum() / len(bought_list)

    return recall


def recall_at_k(recommended_list, bought_list, k=5):

    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]

    flags = np.isin(bought_list, recommended_list)
    recall = flags.sum() / len(bought_list)

    return recall


def recall_at_k_series(df, rec_col, bought_col, k=5):
    df = df[[rec_col, bought_col]].copy()
    df['zip'] = list(zip(df[rec_col], df[bought_col]))
    df['p@k'] = df['zip'].map(lambda zp: recall_at_k(recommended_list=list(zp[0]), bought_list=list(zp[1]), k=k))
    
    return df['p@k']


def evaluate_recommenders(df_test, bought_col, recommender_col_list, k_precision, k_recall):

    print(f'{" ":35} PRECISION     RECALL\n')    
    for col in recommender_col_list:
        p_at_k = np.mean(precision_at_k_series(df_test, rec_col=col, bought_col='purchases', k=k_precision))
        r_at_k = np.mean(recall_at_k_series(df_test, rec_col=col, bought_col='purchases', k=k_recall))
        print(f'{col:35} {p_at_k:f}      {r_at_k:f}')