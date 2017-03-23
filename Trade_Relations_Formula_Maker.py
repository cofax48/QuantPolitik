# -*- coding: utf-8 -*-
#! Trade Relations Formula Maker

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier

def zero_or_nan(country, country_and_percentile_rank_list):
    score = country_and_percentile_rank_list['Fortune Global 500'][country]
    score = list(score)
    if int(score[1]) == int(41):
        score.pop()
        score.append(np.nan)
        score = tuple(score)
        return {'score':score}
    else:
        score = tuple(score)
        return {'score':score}

def trade_data_multiplier(country, country_and_percentile_rank_list):
    new_import_score = country_and_percentile_rank_list['Imports to the United States in 2015'][country]
    new_import_score = list(new_import_score)
    new_import_score_to_insert = new_import_score[1] * 3
    new_import_score.pop()
    new_import_score.append(new_import_score_to_insert)
    new_import_score = tuple(new_import_score)
    
    new_export_score = country_and_percentile_rank_list['Exports from the United States in 2015'][country]
    new_export_score = list(new_export_score)
    new_export_score_to_insert = new_export_score[1] * 3
    new_export_score.pop()
    new_export_score.append(new_export_score_to_insert)
    new_export_score = tuple(new_export_score)
        
    return {'new_import_score':new_import_score, 'new_export_score':new_export_score}


def TRFM(country_name_list, country_and_percentile_rank_list):
    #Total Business Score
    total_trade_rank_percentile_list = []

    rankings_trade_percentile_rank_list = []
    data_trade_percentile_rank_list = []

    for country in country_name_list:
        country_name = country
        country = int(country_numberifier(country))
        Rankings_Trade = (country_and_percentile_rank_list['FDI Inflow in Millions'][country] +
                                country_and_percentile_rank_list['Trading Across Borders'][country] +
                                country_and_percentile_rank_list['GDP Growth Rate in pencentage'][country] +
                                zero_or_nan(country, country_and_percentile_rank_list)['score']  +
                                country_and_percentile_rank_list['Trade Freedom'][country] +
                                country_and_percentile_rank_list['Change in Trade Freedom from 2015'][country] +
                                country_and_percentile_rank_list['Stock Market Capitalization in billions'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Rankings_Trade]))
        real_len = int(len(Rankings_Trade)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Rankings_Trade[1::2])
        Rankings_Trade = biz_sum / dvisible_number
        rankings_trade_percentile_rank_list.append(Rankings_Trade)
        
        Data_Trade = (trade_data_multiplier(country, country_and_percentile_rank_list)['new_import_score'] +
                                trade_data_multiplier(country, country_and_percentile_rank_list)['new_export_score'] +
                                country_and_percentile_rank_list['Exports from the United States in 2014'][country] +
                                country_and_percentile_rank_list['Imports to the United States in 2014'][country] +
                                country_and_percentile_rank_list['Exports from the United States in 2013'][country] +
                                country_and_percentile_rank_list['Imports to the United States in 2013'][country] +
                                country_and_percentile_rank_list['Exports from the United States in 2012'][country] +
                                country_and_percentile_rank_list['Imports to the United States in 2012'][country] +
                                country_and_percentile_rank_list['Exports from the United States in 2011'][country] +
                                country_and_percentile_rank_list['Imports to the United States in 2011'][country] +
                                country_and_percentile_rank_list['Exports from the United States in 2010'][country] +
                                country_and_percentile_rank_list['Imports to the United States in 2010'][country] +
                                country_and_percentile_rank_list['Exports from the United States in 2009'][country] +
                                country_and_percentile_rank_list['Imports to the United States in 2009'][country])
        #Factoring for number of missing data Fields and averaging the raw score

        number_of_nan = int(sum([pd.isnull(i) for i in Data_Trade]))
        real_len = int(len(Data_Trade)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Data_Trade[1::2])
        Data_Trade = num_sum / dvisible_number           
        data_trade_percentile_rank_list.append(Data_Trade)



    #PERCENTILING COMPOSITES AND FACTORIZATION
    rankings_trade_percentile_rank_list_factored = []
    data_trade_percentile_rank_list_factored = []


    for a in rankings_trade_percentile_rank_list:
        rankings_trade_percentile_rank_list_factored.append(stats.percentileofscore(rankings_trade_percentile_rank_list, a, kind='rank'))            

    for b in data_trade_percentile_rank_list:
        data_trade_percentile_rank_list_factored.append(stats.percentileofscore(data_trade_percentile_rank_list, b, kind='rank'))

    #Weighting The Trade Rankings By a factor of 8 for Data_Trade
    rankings_trade_percentile_rank_list_factored = [i * .25 for i in rankings_trade_percentile_rank_list_factored]
    data_trade_percentile_rank_list_factored = [i * 1.75 for i in data_trade_percentile_rank_list_factored] 
                                                              
    total_trade_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        trade_rank_data_together = (rankings_trade_percentile_rank_list_factored[country_num],
                                        data_trade_percentile_rank_list_factored[country_num])
        total_trade_rank[str(country)] = trade_rank_data_together                                         

    trade_relations_aggregate_factored = []
    for country in country_name_list:
        tbr = total_trade_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        trade_relations_aggregate_factored.append(tbr)

    return {'trade_relations_aggregate_factored':trade_relations_aggregate_factored}
