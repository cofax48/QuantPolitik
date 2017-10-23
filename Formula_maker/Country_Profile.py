# -*- coding: utf-8 -*-
#! Governmental Perspective Relations Formula Maker

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier
 
def CPFM(country_name_list, country_and_percentile_rank_list):
    people_power_percentile_rank_list = []
    financial_power_percentile_rank_list = []
    global_climate_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        People_Power = (country_and_percentile_rank_list['Power Status and Relationship'][country] +
                                country_and_percentile_rank_list['Population in Millions'][country] +
                                country_and_percentile_rank_list['Geographic Area including water'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in People_Power]))
        real_len = int(len(People_Power)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(People_Power[1::2])
        People_Power = biz_sum / dvisible_number       
        people_power_percentile_rank_list.append(People_Power)
        
        Financial_Climate = (country_and_percentile_rank_list['GDP in Billions at PPP'][country] +
                                country_and_percentile_rank_list['5 Year GDP Growth Rate in Percentage'][country] +
                                country_and_percentile_rank_list['GDP per Capita in PPP'][country] +
                                country_and_percentile_rank_list['Unemployment in Percent'][country] +
                                country_and_percentile_rank_list['Public Debt as Percentage of GDP'][country] +
                                country_and_percentile_rank_list['HDI'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Financial_Climate]))
        real_len = int(len(Financial_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Financial_Climate[1::2])
        Financial_Climate = num_sum / dvisible_number
        financial_power_percentile_rank_list.append(Financial_Climate)

        Global_Climate = (country_and_percentile_rank_list['Same language'][country] +
                                country_and_percentile_rank_list['Opinion of the US'][country] +
                                country_and_percentile_rank_list['Free Trade Agreements'][country] +
                                country_and_percentile_rank_list['Shared Currency'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Global_Climate]))
        real_len = int(len(Global_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Global_Climate[1::2])
        Global_Climate = num_sum / dvisible_number
        global_climate_percentile_rank_list.append(Global_Climate)

    #PERCENTILING COMPOSITES AND FACTORIZATION
    people_power_percentile_rank_list_factored = []
    financial_power_percentile_rank_list_factored = []
    global_climate_percentile_rank_list_factored = []

    for a in people_power_percentile_rank_list:
        people_power_percentile_rank_list_factored.append(stats.percentileofscore(people_power_percentile_rank_list, a, kind='rank'))            

    for b in financial_power_percentile_rank_list:
        financial_power_percentile_rank_list_factored.append(stats.percentileofscore(financial_power_percentile_rank_list, b, kind='rank'))

    for c in global_climate_percentile_rank_list:
        global_climate_percentile_rank_list_factored.append(stats.percentileofscore(global_climate_percentile_rank_list, c, kind='rank'))

    # Weighting of Size more heavily
    people_power_percentile_rank_list_factored = [i * 3 for i in people_power_percentile_rank_list_factored]
                                                                     
    total_profile_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        profile_rank_data_together = (people_power_percentile_rank_list_factored[country_num],
                                        financial_power_percentile_rank_list_factored[country_num],
                                        global_climate_percentile_rank_list_factored[country_num])
        total_profile_rank[str(country)] = profile_rank_data_together                                         
    
    country_profile_aggregate_factored = []
    for country in country_name_list:
        tbr = total_profile_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        tbr = tbr / 2
        country_profile_aggregate_factored.append(tbr)

    return {'country_profile_aggregate_factored':country_profile_aggregate_factored}
