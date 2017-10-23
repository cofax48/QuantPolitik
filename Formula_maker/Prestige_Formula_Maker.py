# -*- coding: utf-8 -*-
#! Prestige Formula Maker
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier
 
def PFM(country_name_list, country_and_percentile_rank_list):
    summer_olympics_percentile_rank_list = []
    winter_olympics_percentile_rank_list = []
    total_olympics_percentile_rank_list = []
    miscellany_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Summer_Olympics = (country_and_percentile_rank_list['Games Attended Total Summer Olympics'][country] +
                                country_and_percentile_rank_list['Medals Total Summer Olympics'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Summer_Olympics]))
        real_len = int(len(Summer_Olympics)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Summer_Olympics[1::2])
        Summer_Olympics = biz_sum / dvisible_number       
        summer_olympics_percentile_rank_list.append(Summer_Olympics)

                                  
        Winter_Olympics = (country_and_percentile_rank_list['Winter Olympics Attended Total'][country] +
                                country_and_percentile_rank_list['Winter Olympics Medals Total'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Winter_Olympics]))
        real_len = int(len(Winter_Olympics)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Winter_Olympics[1::2])
        Winter_Olympics = num_sum / dvisible_number
        winter_olympics_percentile_rank_list.append(Winter_Olympics)

        Total_Olympics = (country_and_percentile_rank_list['Combined Olympics Attended'][country] +
                                country_and_percentile_rank_list['Combined Medals Total Olympics'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Total_Olympics]))
        real_len = int(len(Total_Olympics)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Total_Olympics[1::2])
        Total_Olympics = num_sum / dvisible_number
        total_olympics_percentile_rank_list.append(Total_Olympics)
        
        Miscellany = (country_and_percentile_rank_list['Number Of Billionaires'][country] +
                                country_and_percentile_rank_list['Nobel Prizes'][country])

        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Miscellany]))
        real_len = int(len(Miscellany)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Miscellany[1::2])
        Miscellany = num_sum / dvisible_number
        miscellany_percentile_rank_list.append(Miscellany)


    #PERCENTILING COMPOSITES AND FACTORIZATION
    summer_olympics_percentile_rank_list_factored = []
    winter_olympics_percentile_rank_list_factored = []
    total_olympics_percentile_rank_list_factored = []
    miscellany_percentile_rank_list_factored = []

    for a in summer_olympics_percentile_rank_list:
        summer_olympics_percentile_rank_list_factored.append(stats.percentileofscore(summer_olympics_percentile_rank_list, a, kind='rank'))            

    for c in winter_olympics_percentile_rank_list:
        winter_olympics_percentile_rank_list_factored.append(stats.percentileofscore(winter_olympics_percentile_rank_list, c, kind='rank'))

    for d in total_olympics_percentile_rank_list:
        total_olympics_percentile_rank_list_factored.append(stats.percentileofscore(total_olympics_percentile_rank_list, d, kind='rank'))

    for e in miscellany_percentile_rank_list:
        miscellany_percentile_rank_list_factored.append(stats.percentileofscore(miscellany_percentile_rank_list, e, kind='rank'))
    
    # Weighting of Size more heavily

    '''
    miscellany_percentile_rank_list_factored = [i * 2 for i in miscellany_percentile_rank_list_factored]
    '''
    
    total_prestige_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        prestige_rank_data_together = (summer_olympics_percentile_rank_list_factored[country_num],
                                        winter_olympics_percentile_rank_list_factored[country_num],
                                        total_olympics_percentile_rank_list_factored[country_num],
                                        miscellany_percentile_rank_list_factored[country_num])
        total_prestige_rank[str(country)] = prestige_rank_data_together                                       
    
    prestige_rank_aggregate_factored = []
    for country in country_name_list:
        tbr = total_prestige_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        
        prestige_rank_aggregate_factored.append(tbr)

    return {'prestige_rank_aggregate_factored':prestige_rank_aggregate_factored}
