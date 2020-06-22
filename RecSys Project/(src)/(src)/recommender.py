import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares
from implicit.nearest_neighbours import ItemItemRecommender
from implicit.nearest_neighbours import bm25_weight, tfidf_weight

import os, sys
import catboost as catb

class RecSys:
 
    def __init__(self,
                 df, 
                 df_items, 
                 df_users,
                 weighting=True,
                 history_weeks_first_model=26,
                 history_weeks_second_model=6,
                 first_model_rec_limit=200,
                 prefilter_params = {'n_popular_limit':5000,
                                     'upper_popularity_limit':0.2,
                                     'lower_popularity_limit':0.02,
                                     'lower_price_limit':1,
                                     'upper_price_limit':50,
                                     'min_dep_assortment':100},
                 als_params = {'n_factors':20,
                               'regularization':0.001,
                               'iterations':15}):
        
        self.df = df.copy()
        self.df_users = df_users.copy()
        self.df_items = df_items.copy()

        self.history_weeks_first_model = history_weeks_first_model
        self.history_weeks_second_model = history_weeks_second_model   
        
        self.weighting = weighting
        self.prefilter_params = prefilter_params
        self.als_params = als_params
        self.first_model_rec_limit = first_model_rec_limit
        
        self.df_pr = None
        self.top_purchases = None
        self.top_popular = None
        self.user_item_matrix = None
        self.id_to_itemid = None
        self.id_to_userid = None
        self.itemid_to_id = None
        self.userid_to_id = None
        
        self._add_item_features()
        self._add_user_features()
        self._prepare_df()
        self._prepare_user_item_matrix()
        
        self._add_top_popular()
        self._add_top_purchases()
        self._add_top_purchases_by_user()
        self._add_own_recs()
        self._add_als_recs(n_factors=als_params['n_factors'], regularization=als_params['regularization'], iterations=als_params['iterations'])
        self._add_basic_recs()

        self.df_sm= self._prepare_df_sm(df=self.df_users,
                                        column_recommended='basic_recommender', 
                                        column_purchases_train='purchases_train', 
                                        df_users=self.df_users)
        
        self._fit_sm()
        
    
    # Training second model
    def _fit_sm(self):

        catbm = catb.CatBoostClassifier(eval_metric='AUC',
                                silent=True,
                                iterations=1000,
                                random_state=21)
        
        df_train = self.df_sm.copy()
        cat_feat_idx = df_train.dtypes[df_train.dtypes == 'object'].index.to_list()
        df_train[cat_feat_idx] = df_train[cat_feat_idx].fillna('')
        
        catbm.fit(df_train.drop(columns=['user_id', 'item_id', 'flag']), df_train['flag'], cat_features=cat_feat_idx)
        self.catb_model = catbm
        self.catb_model_columns = df_train.drop(columns=['user_id', 'item_id', 'flag']).columns.to_list()
        
        df_train['proba'] = catbm.predict_proba(df_train[self.catb_model_columns])[:,1]
        df_train.drop_duplicates(subset=['user_id', 'item_id'], keep='first', inplace=True)
        df_train.sort_values(by=['user_id', 'proba'], ascending=[True, False], inplace=True)
        df_train['item_id'] = df_train['item_id'].astype(int)
        
        catb_pred_dict = df_train.groupby(by=['user_id']).agg({'item_id': list})['item_id'].to_dict()
        
        self.df_users['catb_recommender'] = self.df_users['user_id'].map(catb_pred_dict)
        
        
    # Prepares df for second model based on source df with one column and 
    def _prepare_df_sm(self, df=None, column_recommended=None, column_purchases_train=None, df_users=None, df_items=None):
        
        def normalize_df_column(df, normalize_column):
            user_id_item_list_dict = df.set_index('user_id')[normalize_column].to_dict()
            df_sm = pd.DataFrame()
            for user_id in user_id_item_list_dict.keys():
                df_sm = pd.concat((df_sm, pd.DataFrame({'user_id':user_id, 'item_id':user_id_item_list_dict[user_id]})), axis=0)
            return df_sm
        
        df_sm = normalize_df_column(df=df, normalize_column=column_recommended)
        
        # Adding user features
        user_skip_cols = ['top_popular', 'top_purchases', 'top_purchases_by_user', 'own_recommender', 'als_recommender', 'basic_recommender' , 'purchases_train', 'id']
        df_sm = pd.merge(left=df_sm,
                         right = self.df_users.drop(columns=user_skip_cols),
                         on='user_id',
                         how='left')
        
        # Adding item features
        item_skip_cols = ['popularity', 'id', 'CURR_SIZE_OF_PRODUCT']
        df_sm = pd.merge(left=df_sm,
                         right = self.df_items.drop(columns=item_skip_cols),
                         on='item_id',
                         how='left')

        if type(column_purchases_train) != type(None):
            df_tmp = normalize_df_column(df=df, normalize_column=column_purchases_train)
            df_tmp['flag'] = 1

            df_sm = pd.merge(left=df_sm,
                             right=df_tmp,
                             on=['user_id', 'item_id'],
                             how='left')
            
            df_sm['flag'].fillna(0, inplace=True)
            df_sm['flag'].astype(int)
        
        return df_sm

    
    def predict(self, df_test=None, user_id=None):
        if 'catb_recommender' in self.df_users.columns:
            rec_cols = ['top_popular', 'top_purchases' , 'top_purchases_by_user', 'own_recommender', 'als_recommender', 'basic_recommender', 'catb_recommender']
        else:
            rec_cols = ['top_popular', 'top_purchases' , 'top_purchases_by_user', 'own_recommender', 'als_recommender', 'basic_recommender']            
        
        if type(user_id) == type(None):
            df_test_pred = pd.merge(left=df_test,
                                    right=self.df_users[['user_id'] + rec_cols],
                                    how='left',
                                    on='user_id')     
            df_test_pred['hit'] = (~df_test_pred['top_popular'].isnull())*1
            
            df_test_pred['top_popular'] = df_test_pred['user_id'].map(lambda i: self.top_popular[:self.first_model_rec_limit])     
            df_test_pred['top_purchases'] = df_test_pred['user_id'].map(lambda i: self.top_purchases[:self.first_model_rec_limit])
            
            for col in rec_cols:
                df_test_pred.loc[df_test_pred[col].isnull(), col] = df_test_pred['user_id'].loc[df_test_pred[col].isnull()].map(lambda i: self.top_purchases[:self.first_model_rec_limit])                

            return df_test_pred
        else:
            
            dict_pred = {'user_id': user_id}
            if np.sum(self.df_users['user_id'] == user_id) == 0:
                dict_pred['hit'] = False
                for col in rec_cols:
                    dict_pred[col] = self.df_users.loc[self.df_users['user_id'] == user_id, 'top_popular'].values[0]
            else:
                dict_pred['hit'] = True
                for col in rec_cols:
                    dict_pred[col] = self.df_users.loc[self.df_users['user_id'] == user_id, col].values[0]
                    
            return dict_pred
    
    
    def _add_item_features(self):
        
        self.df_items['dep_assortment'] = self.df_items['DEPARTMENT'].map(self.df_items.groupby(by='DEPARTMENT')['item_id'].count().to_dict())
        self.df_items['brand_assortment'] = self.df_items['BRAND'].map(self.df_items.groupby(by='BRAND')['item_id'].count().to_dict())
        self.df_items['commodity_assortment'] = self.df_items['COMMODITY_DESC'].map(self.df_items.groupby(by='COMMODITY_DESC')['item_id'].count().to_dict())
        self.df_items['subcommodity_assortment'] = self.df_items['SUB_COMMODITY_DESC'].map(self.df_items.groupby(by='SUB_COMMODITY_DESC')['item_id'].count().to_dict())
        self.df_items['manufacturar_assortment'] = self.df_items['SUB_COMMODITY_DESC'].map(self.df_items.groupby(by='SUB_COMMODITY_DESC')['item_id'].count().to_dict())         
        self.df_items['popularity'] = self.df_items['item_id'].map((self.df.groupby('item_id')['user_id'].nunique()/ self.df['user_id'].nunique()).to_dict())
        self.df_items['price_avg'] = self.df_items['item_id'].map((self.df.groupby('item_id')['sales_value'].sum() / self.df.groupby('item_id')['quantity'].sum()).to_dict())
        self.top_popular = self.df_items[(self.df_items['popularity'] <  self.prefilter_params['upper_popularity_limit']) &
                                         (self.df_items['popularity'] > self.prefilter_params['lower_popularity_limit'])]
        self.top_popular = self.top_popular.sort_values(by=['popularity'], ascending=False)['item_id'].to_list()
        
        
    def _add_user_features(self):
        # Users dataset preparation (including all users)
        self.df_users = pd.merge(left=pd.DataFrame({'user_id' : sorted(pd.concat((self.df['user_id'], self.df_users['user_id']), axis=0).unique())}),
                                 right= self.df_users,
                                 on='user_id',
                                 how='left')
        
        # Adding purchases for second level model training
        df_tmp = self.df.loc[self.df['week_no'] > (np.max(self.df['week_no']) - self.history_weeks_second_model)]
        purchases_train_dict = df_tmp.groupby(by=['user_id']).agg({'item_id': lambda lst: list(lst)})['item_id'].to_dict()
        self.df_users['purchases_train'] = self.df_users['user_id'].map(purchases_train_dict)
        self.df_users['purchases_train'] = self.df_users['purchases_train'].map(lambda val: val if type(val)==type([]) else [])        

    def _prepare_df(self):

        self.df_pr = pd.merge(left=self.df,
                              right=self.df_items[['item_id', 'popularity', 'price_avg', 'dep_assortment']],
                              how='left',
                              on='item_id')
        
        # History depth prefiltering
        th_1 = (np.max(self.df_pr['week_no']) - self.history_weeks_first_model-self.history_weeks_second_model)
        th_2 = (np.max(self.df_pr['week_no']) - self.history_weeks_second_model)
        self.df_pr = self.df_pr.loc[(self.df_pr['week_no'] > th_1) & (self.df_pr['week_no'] <= th_2)]
        
        
        
        # Popularity prefiltering
        if 'lower_popularity_limit' in self.prefilter_params.keys():
            self.df_pr.loc[self.df_pr['popularity'] < self.prefilter_params['lower_popularity_limit'], 'item_id'] = 999999
        if 'upper_popularity_limit' in self.prefilter_params.keys():
            self.df_pr.loc[self.df_pr['popularity'] > self.prefilter_params['upper_popularity_limit'], 'item_id'] = 999999
        
        # Average item price prefiltering
        if 'lower_price_limit' in self.prefilter_params.keys():
            self.df_pr.loc[self.df_pr['price_avg'] < self.prefilter_params['lower_price_limit'], 'item_id'] = 999999
        if 'upper_price_limit' in self.prefilter_params.keys():
            self.df_pr.loc[self.df_pr['price_avg'] > self.prefilter_params['upper_price_limit'], 'item_id'] = 999999
        
        # Prefiltering items based on minimum department assortment
        if 'min_dep_assortment' in self.prefilter_params.keys():
            self.df_pr.loc[self.df_pr['dep_assortment'] < self.prefilter_params['min_dep_assortment'], 'item_id'] = 999999
            
        # Calculation top purchases overall
        top_purchases = self.df_pr.groupby('item_id')['quantity'].count().reset_index()
        top_purchases.sort_values('quantity', ascending=False, inplace=True)
        self.top_purchases = top_purchases[top_purchases['item_id'] != 999999]['item_id'].to_list()


        # Replace all least popular item_id to 999999
        if 'n_popular_limit' in self.prefilter_params.keys():            
            
            self.df_pr.loc[~self.df_pr['item_id'].isin(self.top_popular[:self.prefilter_params['n_popular_limit']]), 'item_id'] = 999999
            
        
        self.df_pr.drop(columns=['popularity', 'price_avg', 'dep_assortment'], inplace=True)    
        
    
    def _prepare_user_item_matrix(self):
        """Подготовка user-item матрицу и вспомогательных словарей """
        
        user_item_matrix = pd.pivot_table(self.df_pr,
                                          index='user_id',
                                          columns='item_id',
                                          values='quantity',  # Можно пробовать другие варианты
                                          aggfunc='count',
                                          fill_value=0)

        self.user_item_matrix = user_item_matrix.astype(float)  # необходимый тип матрицы для implicit
        
        self.user_item_matrix = csr_matrix(self.user_item_matrix).tocsr()
        
        if self.weighting:
            self.user_item_matrix = tfidf_weight(self.user_item_matrix.T).T
        
        # Preparing dicts
        userids = user_item_matrix.index.values
        itemids = user_item_matrix.columns.values

        matrix_userids = np.arange(len(userids))
        matrix_itemids = np.arange(len(itemids))

        self.id_to_itemid = dict(zip(matrix_itemids, itemids))
        self.id_to_userid = dict(zip(matrix_userids, userids))

        self.itemid_to_id = dict(zip(itemids, matrix_itemids))
        self.userid_to_id = dict(zip(userids, matrix_userids))
        
        self.df_users['id'] = self.df_users['user_id'].map(self.userid_to_id)
        self.df_items['id'] = self.df_items['item_id'].map(self.itemid_to_id)        

    
    def _add_top_popular(self):
        self.df_users['top_popular'] = self.df_users['user_id'].map(lambda id: self.top_popular[:self.first_model_rec_limit])        
        self.df_users['top_popular'] = self.df_users['top_popular'].map(lambda val: val if type(val)==type([]) else [])

    
    def _add_top_purchases(self):
        self.df_users['top_purchases'] = self.df_users['user_id'].map(lambda i: self.top_purchases[:self.first_model_rec_limit])
        self.df_users['top_purchases'] = self.df_users['top_purchases'].map(lambda val: val if type(val)==type([]) else [])    
    
    def _add_top_purchases_by_user(self):
        # Top purchases by user
        top_purchases_by_user = self.df_pr.groupby(['user_id', 'item_id'])['quantity'].count().reset_index()
        top_purchases_by_user.sort_values(['user_id', 'quantity'], ascending=[True, False], inplace=True)
        top_purchases_by_user = top_purchases_by_user[top_purchases_by_user['item_id'] != 999999]
        top_purchases_by_user = top_purchases_by_user.groupby(by=['user_id']).agg({'item_id': lambda lst: list(lst)[:self.first_model_rec_limit]})['item_id'].to_dict()
        self.df_users['top_purchases_by_user'] = self.df_users['user_id'].map(top_purchases_by_user)
        self.df_users['top_purchases_by_user'] = self.df_users['top_purchases_by_user'].map(lambda val: val if type(val)==type([]) else [])        

        
    def _add_own_recs(self):
        """Добавление к бейслайнам рекомендаций основанных на собственных покупках юзера"""
        user_item_matrix = (self.user_item_matrix > 0).astype(float)
        own_recommender = ItemItemRecommender(K=1, num_threads=4)
        own_recommender.fit(csr_matrix(user_item_matrix).T.tocsr())
        recs = lambda i: [self.id_to_itemid[rec[0]] for rec in own_recommender.recommend(userid=int(i), 
                                                                                         user_items=csr_matrix(user_item_matrix).tocsr(),
                                                                                         N=self.first_model_rec_limit,
                                                                                         filter_already_liked_items=False,
                                                                                         filter_items = [self.itemid_to_id[999999]])]
        self.df_users['own_recommender'] = None
        self.df_users.loc[~self.df_users['id'].isnull(), 'own_recommender'] = self.df_users.loc[~self.df_users['id'].isnull(), 'id'].map(recs)        
        self.df_users['own_recommender'] = self.df_users['own_recommender'].map(lambda val: val if type(val)==type([]) else [])    
    
    def _add_als_recs(self, n_factors=20, regularization=0.001, iterations=20, num_threads=0):

        als_model = AlternatingLeastSquares(factors=n_factors,
                                            regularization=regularization,
                                            iterations=iterations,
                                            num_threads=num_threads)
        
        als_model.fit(csr_matrix(self.user_item_matrix).T.tocsr())
        self.als_model = als_model
        
        als_recs = lambda i: [self.id_to_itemid[rec[0]] for rec in als_model.recommend(userid=int(i), 
                                                                                       user_items=csr_matrix(self.user_item_matrix).tocsr(), 
                                                                                       N=self.first_model_rec_limit,
                                                                                       filter_items = [self.itemid_to_id[999999]],
                                                                                       recalculate_user=True,
                                                                                       filter_already_liked_items=False)]
        self.df_users['als_recommender'] = None
        self.df_users.loc[~self.df_users['id'].isnull(), 'als_recommender'] = self.df_users.loc[~self.df_users['id'].isnull(), 'id'].map(als_recs)
        self.df_users['als_recommender'] = self.df_users['als_recommender'].map(lambda val: val if type(val)==type([]) else [])
        
        # adding embedings to df_users and df_items as features
        als_user_factors = pd.DataFrame(self.als_model.user_factors, columns=[f'als_user_factor_{i}' for i in range(self.als_model.user_factors.shape[1])])
        als_user_factors['id'] = als_user_factors.index
        self.df_users = pd.merge(left=self.df_users,
                                 right=als_user_factors,
                                 on='id',
                                 how='left')

        als_item_factors = pd.DataFrame(self.als_model.item_factors, columns=[f'als_item_factor_{i}' for i in range(self.als_model.item_factors.shape[1])])
        als_item_factors['id'] = als_item_factors.index
        self.df_items = pd.merge(left=self.df_items,
                                 right=als_item_factors,
                                 on='id',
                                 how='left')
    
    # Generating reccomendations for 2nd level model
    def _add_basic_recs(self):
        
        self.df_users['basic_recommender'] = list(zip(self.df_users['top_popular'],
                                                      self.df_users['top_purchases'],
                                                      self.df_users['top_purchases_by_user'],
                                                      self.df_users['als_recommender'],
                                                      self.df_users['own_recommender']))
        self.df_users['basic_recommender'] = self.df_users['basic_recommender'].map(lambda zp: np.array(list(zip(zp[0], zp[1], zp[2], zp[3], zp[4]))).flatten())
    
    
    # preprocess test data (adding 'purchases' column based on sales)
    def df_test_preprocess(self, df_test):
        df_test_pr = df_test.groupby(by=['user_id']).agg({'item_id': list}).reset_index()
        df_test_pr.rename(columns={'item_id':'purchases'}, inplace=True)

        return df_test_pr