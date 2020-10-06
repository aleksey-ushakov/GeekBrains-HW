import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, r2_score, roc_auc_score
from matplotlib import pyplot as plt
from itertools import product

def short_model_score_report(y_true=[], y_pred=None, y_pred_proba=None, name='', display=True, header=True, model_type='classification'):
    
    # отчет для модели классификации
    if model_type == 'classification':
        
        if len(y_true) == 0:
            name = name
            f1 = ''
            pr = ''
            re = ''
            roc = ''
            gini = ''
            qty = 0
            y_true_rate = 0
        else:
            y_pred = np.round(y_pred_proba).astype('int')
            
            f1 = round(f1_score(y_true, y_pred),4)
            pr = round(precision_score(y_true, y_pred),4)
            re = round(recall_score(y_true, y_pred),4)
            roc = round(roc_auc_score(y_true, y_pred_proba),4) if (y_true.value_counts().shape[0] >1) else '-'
            gini = round(roc * 2 - 1, 4) if (roc !='-') else roc
            qty = len(y_true)
            y_true_rate = np.mean(y_true)
        
        if display:
            if header:
                print('\033[4m{:<40}{:>8}{:>8}{:>10}{:>10}{:>12}{:>10}{:>10}\033[0m'.format('Model', 'Qty', '1 %','f1 score', 'Recall', 'Precission', 'ROC AUC', 'Gini'))
            print('{:<40}{:>8}{:>8.2%}{:>10}{:>10}{:>12}{:>10}{:>10}'.format(name, qty, y_true_rate, f1, re, pr, roc, gini))
        else:
            return {'name':name,
                    'qty':qty,
                    'target_class_qty':np.sum(y_true),
                    'target_class_rate':y_true_rate,
                    'f1_score':f1,
                    'precision':pr,
                    'recall':re,
                    'ROC_AUC':roc,
                    'gini':gini} 
    
    
    # отчет для модели регрессии
    if model_type == 'regression':
        if len(y_true) == 0:
            name = name       
            mae = ''
            mse = ''
            rmse = ''
            r2 =  ''
            qty = 0
        else:
            mse_err = lambda y, y_pred : np.mean((y - y_pred) ** 2)
            rmse_err = lambda y, y_pred : mse_err(y, y_pred) ** 0.5
            mae_err = lambda y, y_pred : np.mean(np.abs(y - y_pred))
            r2_calc = lambda y, y_pred : 1 - mse_err(y, y_pred) / mse_err(y, np.mean(y))

            mae = round(mae_err(y_true, y_pred),4)
            mse = round(mse_err(y_true, y_pred),4)
            rmse = round(rmse_err(y_true, y_pred),4)
            r2 =  round(r2_calc(y_true, y_pred),4)
            qty= len(y_true)
        
        if display:
            if header:
                print('\033[4m{:<40}{:>10}{:>10}{:>10}{:>10}\033[0m'.format('Model', 'Qty', 'MAE', 'RMSE', 'R2'))
            print('{:<40}{:>10}{:>10}{:>10}{:>10}'.format(name, qty, mae, rmse, r2))
        else:
            return {'name':name,
                    'qty':qty,
                    'MAE':mae,
                    'MSE':mse,
                    'RMSE':rmse,
                    'r2_score':r2}
        

# Scoring report function
def scoring_report(y_true,
                   y_proba,
                   credit_amt=None,
                   split_qty=None,
                   min_scale=0,
                   max_scale=1000,
                   score_bucket=True,
                   value_report=False,
                   plot=False):
    
    # Корректировка входных данных на случай выбросов (FICO имеет большое кол-во скоров на границе диапазонов и случаются выбросы)
    y_proba[y_proba <= 0] = 0.1 / max_scale
    y_proba[y_proba >= 1] = 1 - 0.1 / max_scale
    
    if type(credit_amt) == type(None):
        credit_amt = pd.Series(np.ones(y_true.shape[0]))
    else:
        credit_amt = credit_amt
    
    report = pd.DataFrame({'score': max_scale - y_proba * (max_scale - min_scale),
                           'target': y_true,
                           'credit_amt': credit_amt,
                           'risk_amt': credit_amt * y_true})
    
    report.sort_values(by='score', ascending=True, inplace=True)
    
    report.index = np.arange(report.shape[0])

    
    # Определение кол-во бакетов по умолчанию для разных видов отчетов
    if not split_qty:
        split_qty = 10 + 10 * score_bucket
    
    # Деление на бакеты в зависимости от типа отчета
    if score_bucket:
        report['bucket_cut_row'] = report['score']
        buckets = np.linspace(min_scale, max_scale, split_qty+1).astype('int')
        buckets_labels = buckets

    else:
        
        if y_true.shape[0] >= split_qty:
            if value_report:
                report['bucket_cut_row'] = np.cumsum(report['credit_amt'])
                
                if np.sum(report['credit_amt']) > 0:
                    buckets = np.linspace(0, np.sum(report['credit_amt']), split_qty + 1)
                else:
                    buckets = np.linspace(0, split_qty, split_qty + 1)
                
            else:
                report['bucket_cut_row'] = report.index
                buckets = np.percentile(report['bucket_cut_row'], np.linspace(0, 100, split_qty + 1))
        else:
            report['bucket_cut_row'] = report.index            
            buckets = np.linspace(0, split_qty, split_qty + 1)
        
        buckets = list(buckets)[:-1] + [list(buckets)[-1]+1]
        buckets_labels = np.linspace(0, 100, split_qty + 1).astype('int')
    
    report['bucket'] = pd.cut(report['bucket_cut_row'], right=False, bins=buckets, labels=buckets_labels[1:])
    
    # Формирование отчета
    report = report.groupby(by='bucket').agg({'score':len,
                                              'target':sum,
                                              'credit_amt':sum,
                                              'risk_amt':sum}).reset_index()
    
    report.columns = ['bucket', 'buckets_qty', 'risk_qty', 'buckets_amt', 'risk_amt']
    
    report['buckets_qty'].fillna(0, inplace=True)
    report['buckets_amt'].fillna(0, inplace=True)
    
    report['buckets_amt'] = report['buckets_amt'] / 1000000
    report['risk_amt'] = report['risk_amt'] / 1000000
    
    report['buckets_qty'] = report['buckets_qty'].astype('int')
    
    report['buckets_qty_%'] = report['buckets_qty'] / np.sum(report['buckets_qty']) * 100
    report['buckets_amt_%'] = report['buckets_amt'] / np.sum(report['buckets_amt']) * 100
    
    report['buckets_qty_cum'] = np.cumsum(report['buckets_qty'])
    report['buckets_amt_cum'] = np.cumsum(report['buckets_amt'])
    
    report['buckets_qty_cum_%'] = report['buckets_qty_cum'] / np.sum(report['buckets_qty']) * 100
    report['buckets_amt_cum_%'] = report['buckets_amt_cum'] / np.sum(report['buckets_amt']) * 100    
    
    report['risk_qty_cum'] = np.cumsum(report['risk_qty'])
    report['risk_amt_cum'] = np.cumsum(report['risk_amt'])
    
    report['risk_qty_portion_%'] = report['risk_qty'] / report['buckets_qty'] * 100
    report['risk_amt_portion_%'] = report['risk_amt'] / report['buckets_amt'] * 100
    
    report['risk_qty_portion_cum_%'] = report['risk_qty_cum'] / report['buckets_qty_cum'] * 100
    report['risk_amt_portion_cum_%'] = report['risk_amt_cum'] / report['buckets_amt_cum'] * 100    
    
    report['portion_of_ttl_risk_qty_cum_%'] = report['risk_qty_cum'] / np.sum(report['risk_qty']) * 100
    report['portion_of_ttl_risk_amt_cum_%'] = report['risk_amt_cum'] / np.sum(report['risk_amt']) * 100

    # Округление полей отчета
    for col in report.columns:
        if col[-1]=='%':
            report[col] = np.round(report[col], 2)
        elif col[-3:] == 'qty' or col[-7:] == 'qty_cum':
            report[col] = np.round(report[col], 0)
        elif col[-3:] == 'amt' or col[-7:] == 'amt_cum':
            report[col] = np.round(report[col], 2)
        else:
            report[col] = np.round(report[col], 0)

    # Словарь для перевода нименования ситолбцов на русский язык
    report_columns_dict = {'bucket':'Бакет',
                           'buckets_qty':'Кол-во',
                           'buckets_qty_cum':'Кол-во (ком)',
                           'buckets_qty_%':'Кол-во %',
                           'buckets_qty_cum_%':'Кол-во % (ком)',
                           'risk_qty':'Риск кол-во',
                           'risk_qty_cum':'Риск кол-во (ком)',
                           'risk_qty_portion_%':'Риск кол-во %',
                           'risk_qty_portion_cum_%':'Риск кол-во % (ком)',
                           'portion_of_ttl_risk_qty_cum_%':'Доля риска от всего риска кол-во % (ком)',
                           'buckets_amt':'Сумма (млн)',
                           'buckets_amt_cum':'Сумма (ком)',
                           'buckets_amt_%':'Сумма %',
                           'buckets_amt_cum_%':'Сумма % (ком)',
                           'risk_amt':'Риск сумма',
                           'risk_amt_cum':'Риск сумма (ком)',
                           'risk_amt_portion_%':'Риск сумма %',
                           'risk_amt_portion_cum_%':'Риск сумма % (ком)',
                           'portion_of_ttl_risk_amt_cum_%':'Доля риска от всего риска сумма % (ком)'}
    
    if plot and score_bucket:
        
        fig, ax = plt.subplots(ncols=2, nrows=2)
        fig.set_size_inches (18 , 12)
        plt.subplots_adjust(wspace=0.3, hspace=0.3)
    
        ax = ax.flatten()
            
        bar_width = (max_scale - min_scale) / split_qty * 0.9
        
        # Графики по кол-ву
        ax_02 = ax[0].twinx()
        ax_02.bar(x=report['bucket'], height=report['buckets_qty_%'], width=bar_width, label='Выдача (кол-во %)',  align='center', alpha=0.5)
        ax_02.set_ylabel('Выдача (кол-во %)')        
        ax_02.legend(loc='upper right') 
        ax_02.set_ylim([0, np.max(report['buckets_qty_%'])*1.2])
        
        ax_12 = ax[1].twinx()
        ax_12.bar(x=buckets_labels[1:], height=report['buckets_qty_cum_%'], width=bar_width, label='Выдача накопительно\n(кол-во %)', alpha=0.5)
        ax_12.set_ylabel('Выдача (кол-во %)')        
        ax_12.legend(loc='upper right') 
        ax_12.set_ylim([0, np.max(report['buckets_qty_cum_%'])*1.2])
    
        ax[0].plot(buckets_labels[1:], report['risk_qty_portion_%'], 'ro-',label='Риск (кол-во %)')
        ax[0].set_title('Распределение по бакетам (кол-во)')
        ax[0].set_xlabel('Скор-Бал')
        ax[0].set_ylabel('Риск %')
        ax[0].set_xticks(buckets_labels[1:])
        ax[0].set_ylim([0, np.max(report['risk_qty_portion_%'])*1.2])
        ax[0].legend(loc='upper left')
        ax[0].set_xticklabels(labels = buckets_labels, rotation = 45) 

        ax[1].plot(buckets_labels[1:], report['risk_qty_portion_cum_%'],'ro-', label='Риск накопительно \n(кол-во %)')
        ax[1].set_title('Накопительное распределение (кол-во)')
        ax[1].set_xlabel('Скор-Бал')
        ax[1].set_ylabel('Риск %')
        ax[1].set_xticks(buckets_labels[1:])
        ax[1].set_ylim([0, np.max(report['risk_qty_portion_cum_%'])*1.2])
        ax[1].legend(loc='upper left')
        ax[1].set_xticklabels(labels = buckets_labels, rotation = 45) 
        
        # Графики по сумме        
        ax_22 = ax[2].twinx()
        ax_22.bar(x=report['bucket'], height=report['buckets_amt_%'], width=bar_width, label='Выдача (сумма %)',  align='center', alpha=0.5)
        ax_22.set_ylabel('Выдача (сумма %)')        
        ax_22.legend(loc='upper right') 
        ax_22.set_ylim([0, np.max(report['buckets_amt_%'])*1.2])
        
        ax_32 = ax[3].twinx()
        ax_32.bar(x=buckets_labels[1:], height=report['buckets_amt_cum_%'], width=bar_width, label='Выдача накопительно\n(сумма %)', alpha=0.5)
        ax_32.set_ylabel('Выдача (сумма %)')        
        ax_32.legend(loc='upper right') 
        ax_32.set_ylim([0, np.max(report['buckets_amt_cum_%'])*1.2])
    
        ax[2].plot(buckets_labels[1:], report['risk_amt_portion_%'], 'ro-',label='Риск (сумма %)')
        ax[2].set_title('Распределение по бакетам (сумма)')
        ax[2].set_xlabel('Скор-Бал')
        ax[2].set_ylabel('Риск %')
        ax[2].set_xticks(buckets_labels[1:])
        ax[2].set_ylim([0, np.max(report['risk_amt_portion_%'])*1.2])
        ax[2].legend(loc='upper left')
        ax[2].set_xticklabels(labels = buckets_labels, rotation = 45) 

        ax[3].plot(buckets_labels[1:], report['risk_amt_portion_cum_%'],'ro-', label='Риск накопительно \n(сумма %)')
        ax[3].set_title('Накопительное распределение (сумма)')
        ax[3].set_xlabel('Скор-Бал')
        ax[3].set_ylabel('Риск %')
        ax[3].set_xticks(buckets_labels[1:])
        ax[3].set_ylim([0, np.max(report['risk_amt_portion_cum_%'])*1.2])
        ax[3].legend(loc='upper left')
        ax[3].set_xticklabels(labels = buckets_labels, rotation = 45) 
        
        
    if plot and not score_bucket:
        
        fig, ax = plt.subplots(ncols=1, nrows=1)
        fig.set_size_inches (11 , 5)
        plt.subplots_adjust(wspace=0.2, hspace=0.3)
        
        if value_report:
            bar_series = 'portion_of_ttl_risk_amt_cum_%'
            line_1_series = 'risk_amt_portion_%'
            line_1_label = 'Риск (сумма %)'
            line_2_series = 'risk_amt_portion_cum_%'
            line_2_label = 'Риск накопительно (сумма %)'
        else:
            bar_series = 'portion_of_ttl_risk_qty_cum_%'
            line_1_series = 'risk_qty_portion_%'
            line_1_label = 'Риск (кол-во %)'
            line_2_series = 'risk_qty_portion_cum_%'
            line_2_label = 'Риск накопительно (кол-во %)'
        
        bar_width = 100 / split_qty * 0.9
        
        ax_2 = ax.twinx()
        ax_2.bar(x=buckets_labels[1:], height=report[bar_series], width=bar_width, label='Доля риска от всего риска % (ком)', alpha=0.5, color='grey')
        #ax_2.plot(buckets_labels[1:], report['portion_of_ttl_risk_cum_%'],'bo-', label='Доля риска от всего риска % (ком)')
        ax_2.set_ylabel('Доля риска от всего риска %')        
        ax_2.legend(loc='upper right') 
        ax_2.set_ylim([0, np.max(report[bar_series])*1.2])
   
        ax.plot(buckets_labels[1:], report[line_1_series], 'ro-',label=line_1_label)
        ax.plot(buckets_labels[1:], report[line_2_series],'go-', label=line_2_label)
        ax.set_title('Распределение по персентилям')
        ax.set_xlabel('Персентиль выдач')
        ax.set_ylabel('Риск %')
        ax.set_xticks(buckets_labels[1:])
        ax.set_ylim([0, np.max(report[[line_1_series, line_2_series]].stack())*1.2])
        ax.legend(loc='upper left')
        ax.set_xticklabels(labels = buckets_labels, rotation = 45) 
    
    # Упорядочивание колонок
    report = report[report_columns_dict.keys()]              

    # Переименоване столбцов отчета на русский язык перед выводом
    report.columns = [report_columns_dict[col] for col in report.columns]

    report.set_index('Бакет', inplace=True)
    
    return report


def slice_report(df,                           # DataFrame with features columns from features_list
                 y_true,                       # y_true Series
                 y_proba=None,                 # Dictionary with predicted y probability {model_name:y_proba}
                 credit_amt=None,              # Credit amount
                 slice_dict=None,              # Dictionaty with slices from dict to check metrics: {slice_name:slice_indexes}
                 feature_list=None,            # list of features to check metyrics 
                 score_splits=20,              # bucket_qty in score report
                 percentile_splits=20,         # bucket_qty in percentile report
                 model_type='classification'): # Model type to get metrics from short_model_score_report
    df = df[feature_list]
    scoring_report_list = []
    slice_bunch_metrics_list = []
    
    if type(credit_amt) == type(None):
        credit_amt = y_true.map(lambda p:1)
    
    if not slice_dict:
        slice_dict={'ALL_VALUES':df.index}
    
    dimentions_list = list(list(df[feature].value_counts().index) + ['ALL_VALUES'] for feature in feature_list)
    dimentions_list = list(product(*dimentions_list))
    
    slice_qty = len(y_proba.keys()) * len(slice_dict.keys()) * len(dimentions_list)
    slice_counter = 0
    
    for model in y_proba.keys():
        for slice_key in slice_dict.keys():
            
            df_slice = df.loc[slice_dict[slice_key]]
            y_true_slice = y_true.loc[slice_dict[slice_key]]
            credit_amt_slice = credit_amt.loc[slice_dict[slice_key]]
            y_proba_slice = y_proba[model].loc[slice_dict[slice_key]]
            
            if len(feature_list) > 0 and (dimentions_list[0][0] != 'ALL_VALUES'):
                cur_dimention_0 = dimentions_list[0][0]
                cur_df_slice_bunch = df_slice.loc[df_slice[feature_list[0]]==dimentions_list[0][0]]
                
            for dimention in dimentions_list:
                print('\r' * 100 + f'{slice_counter} of {slice_qty} slice done', end='')
                
                if cur_dimention_0 != dimention[0]:
                    cur_dimention_0 = dimention[0]
                    if dimention[0] != 'ALL_VALUES':
                        cur_df_slice_bunch = df_slice.loc[df_slice[feature_list[0]]==dimention[0]]
                    else:
                        cur_df_slice_bunch = df_slice
                        
                df_slice_bunch = cur_df_slice_bunch.loc[:]
                slice_bunch_name = str(slice_key) + ' ' + feature_list[0] + '=' + str(dimention[0])

                for i in range(1, len(feature_list)):
                    slice_bunch_name += ' ' + feature_list[i] + '=' + str(dimention[i])

                    if dimention[i] != 'ALL_VALUES':
                        df_slice_bunch = df_slice_bunch.loc[df_slice_bunch[feature_list[i]]==dimention[i]]
                slice_bunch_index = df_slice_bunch.index

                # Формирование отчета по метрикам на слайсе по заданному срезу признаков
                slice_bunch_metrics = short_model_score_report(y_true=y_true_slice.loc[slice_bunch_index],
                                                               y_pred_proba=y_proba_slice.loc[slice_bunch_index],
                                                               name=slice_bunch_name,
                                                               header=True,
                                                               model_type=model_type,
                                                               display=False)
                slice_bunch_metrics['model'] = model
                slice_bunch_metrics['slice'] = slice_key
                for f, i in zip(feature_list, range(len(feature_list))):
                    slice_bunch_metrics[f] = list(dimention)[i]
                slice_bunch_metrics_list.append(slice_bunch_metrics)
                                
                #формирование отчетов по скорам и персентилям                
                slice_bunch_report_score = scoring_report(y_true=y_true_slice.loc[slice_bunch_index],
                                                          credit_amt=credit_amt_slice.loc[slice_bunch_index],
                                                          y_proba=y_proba_slice.loc[slice_bunch_index],
                                                          split_qty=score_splits,
                                                          min_scale=0,
                                                          max_scale=1000,
                                                          score_bucket=True,
                                                          value_report=False,
                                                          plot=False)
                
                slice_bunch_report_per_q = scoring_report(y_true=y_true_slice.loc[slice_bunch_index],
                                                          credit_amt=credit_amt_slice.loc[slice_bunch_index],
                                                          y_proba=y_proba_slice.loc[slice_bunch_index],
                                                          split_qty=score_splits,
                                                          min_scale=0,
                                                          max_scale=1000,
                                                          score_bucket=False,
                                                          value_report=False,                                                          
                                                          plot=False)
                
                slice_bunch_report_per_a = scoring_report(y_true=y_true_slice.loc[slice_bunch_index],
                                                          credit_amt=credit_amt_slice.loc[slice_bunch_index],
                                                          y_proba=y_proba_slice.loc[slice_bunch_index],
                                                          split_qty=score_splits,
                                                          min_scale=0,
                                                          max_scale=1000,
                                                          score_bucket=False,
                                                          value_report=True,                                                          
                                                          plot=False)
                
                # Добавление к скоринговому отчету названия слайсов, модели значение признаков
                slice_bunch_report_score['report_type'] = 'score bucket'
                slice_bunch_report_per_q['report_type'] = 'percentile qty'
                slice_bunch_report_per_a['report_type'] = 'percentile amt'
                
                slice_bunch_report = pd.concat((slice_bunch_report_score.reset_index(),
                                                slice_bunch_report_per_q.reset_index(),
                                                slice_bunch_report_per_a.reset_index()),
                                                axis=0)
                
                slice_bunch_report['model'] = model
                slice_bunch_report['slice'] = slice_key
                slice_bunch_report['name'] = slice_bunch_name
                
                for j in range(len(feature_list)):
                    slice_bunch_report[feature_list[j]] = dimention[j]
                    
                scoring_report_list.append(slice_bunch_report)
                
                slice_counter += 1
                print('\r' * 100 + f'{slice_counter} of {slice_qty} slice done', end='')
    print()
    
    report_metrics = list(short_model_score_report (model_type=model_type, display=False).keys())
    metrics_report = pd.DataFrame(slice_bunch_metrics_list)
    metrics_report = metrics_report[['model', 'slice'] + feature_list + report_metrics]
    scoring_report_full =  pd.concat((scoring_report_list), axis=0)

    return metrics_report, scoring_report_full



# Оценка Качество предсказаний модели в разрезе продуктов и повторных/новых заемщиков
def report_by_product(df, y_true, y_proba, model_type='classification'):
    
    # Dictionaries
    product_dict = {1:'Кредит на автомобиль',
                    4:'Лизинг',
                    6:'Ипотека',
                    7:'Кредитная карта',
                    9:'Потребительский кредит',
                    10:'На развитие бизнеса',
                    11:'На пополнение оборотных средств',
                    12:'На покупку оборудования',
                    13:'На строитель|ство',
                    14:'На покупку ценных бумаг',
                    15:'Межбанковский кредит',
                    16:'Микрокредит',
                    17:'Дебетовая карта с овердрафтом',
                    18: 'Овердрафт',
                    'ALL_VALUES':'ВСЕ ПРОДУКТЫ'}
    
    if 'NEW_REPEAD' in df.columns:
        df['REPEAT_CNT'] = df['NEW_REPEAD']
    
    if 'PRODUCT' in df.columns:
        df['ACCT_TYPE'] = df['PRODUCT']
    
    
    segments = [('ВСЕ ЗАЕМЩИКИ', df),
                ('ПОВТОРНЫЕ', df.loc[(df['REPEAT_CNT'] > 0)]),
                ('НОВЫЕ', df.loc[(df['REPEAT_CNT'] == 0)])]

    for segment_name, segment_df in segments:
        print('\n'+segment_name)
        for prod in df['ACCT_TYPE'].unique():
            prod_index =  segment_df.loc[segment_df['ACCT_TYPE'] == prod].index
            if prod_index.shape[0]>0:
                short_model_score_report(y_true=y_true.loc[prod_index],
                                         y_pred_proba=y_proba.loc[prod_index],
                                         name=product_dict.get(prod) +' (' + str(int(prod)) +')',
                                         header=(prod == df['ACCT_TYPE'].unique()[0]),
                                         model_type=model_type)
        prod_index =  segment_df.index
        short_model_score_report(y_true=y_true.loc[prod_index],
                                 y_pred_proba=y_proba.loc[prod_index],
                                 name='Все продукты',
                                 header=False,
                                 model_type=model_type)