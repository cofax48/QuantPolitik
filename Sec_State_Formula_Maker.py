# -*- coding: utf-8 -*-
#! Prestige Formula Maker
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier
 
def SSFM(country_name_list, country_and_percentile_rank_list):
    Sec_of_State_2011_percentile_rank_list = []
    Sec_of_State_2012_percentile_rank_list = []
    Sec_of_State_2013_percentile_rank_list = []
    Sec_of_State_2014_percentile_rank_list = []
    Sec_of_State_2015_percentile_rank_list = []
    Sec_of_State_2016_percentile_rank_list = []
    Sec_of_State_2017_percentile_rank_list = []    
    Total_Sec_of_State_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Sec_of_State_2011 = (country_and_percentile_rank_list['Sec_of_State_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2011]))
        real_len = int(len(Sec_of_State_2011)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2011[1::2])
        Sec_of_State_2011 = biz_sum / dvisible_number 
        Sec_of_State_2011_percentile_rank_list.append(Sec_of_State_2011)

        #2012
        Sec_of_State_2012 = (country_and_percentile_rank_list['Sec_of_State_2012'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2012]))
        real_len = int(len(Sec_of_State_2012)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2012[1::2])
        Sec_of_State_2012 = biz_sum / dvisible_number 
        Sec_of_State_2012_percentile_rank_list.append(Sec_of_State_2012)

        #2013
        Sec_of_State_2013 = (country_and_percentile_rank_list['Sec_of_State_2013'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2013]))
        real_len = int(len(Sec_of_State_2013)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2013[1::2])
        Sec_of_State_2013 = biz_sum / dvisible_number 
        Sec_of_State_2013_percentile_rank_list.append(Sec_of_State_2013)

        #2014
        Sec_of_State_2014 = (country_and_percentile_rank_list['Sec_of_State_2014'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2014]))
        real_len = int(len(Sec_of_State_2014)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2014[1::2])
        Sec_of_State_2014 = biz_sum / dvisible_number 
        Sec_of_State_2014_percentile_rank_list.append(Sec_of_State_2014)

        #2015
        Sec_of_State_2015 = (country_and_percentile_rank_list['Sec_of_State_2015'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2015]))
        real_len = int(len(Sec_of_State_2015)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2015[1::2])
        Sec_of_State_2015 = biz_sum / dvisible_number 
        Sec_of_State_2015_percentile_rank_list.append(Sec_of_State_2015)

        #2016
        Sec_of_State_2016 = (country_and_percentile_rank_list['Sec_of_State_2016'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2016]))
        real_len = int(len(Sec_of_State_2016)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2016[1::2])
        Sec_of_State_2016 = biz_sum / dvisible_number 
        Sec_of_State_2016_percentile_rank_list.append(Sec_of_State_2016)

        #2017
        Sec_of_State_2017 = (country_and_percentile_rank_list['Sec_of_State_2017'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in Sec_of_State_2017]))
        real_len = int(len(Sec_of_State_2017)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Sec_of_State_2017[1::2])
        Sec_of_State_2017 = biz_sum / dvisible_number 
        Sec_of_State_2017_percentile_rank_list.append(Sec_of_State_2017)
        
        #TOTAL
        Total_Sec_of_State = (country_and_percentile_rank_list['Sec_of_State_2017'][country] +
                              country_and_percentile_rank_list['Sec_of_State_2016'][country] +
                              country_and_percentile_rank_list['Sec_of_State_2015'][country] +
                              country_and_percentile_rank_list['Sec_of_State_2014'][country] +
                              country_and_percentile_rank_list['Sec_of_State_2013'][country] +
                              country_and_percentile_rank_list['Sec_of_State_2012'][country] +
                              country_and_percentile_rank_list['Sec_of_State_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in Total_Sec_of_State]))
        real_len = int(len(Total_Sec_of_State)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Total_Sec_of_State[1::2])
        Total_Sec_of_State = biz_sum / dvisible_number 
        Total_Sec_of_State_percentile_rank_list.append(Total_Sec_of_State)


    #PERCENTILING COMPOSITES AND FACTORIZATION
    Sec_of_State_2011_percentile_rank_list_factored = []
    Sec_of_State_2012_percentile_rank_list_factored = []
    Sec_of_State_2013_percentile_rank_list_factored = []
    Sec_of_State_2014_percentile_rank_list_factored = []
    Sec_of_State_2015_percentile_rank_list_factored = []
    Sec_of_State_2016_percentile_rank_list_factored = []
    Sec_of_State_2017_percentile_rank_list_factored = []
    Total_Sec_of_State_percentile_rank_list_factored = []

    for a in Sec_of_State_2011_percentile_rank_list:
        Sec_of_State_2011_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2011_percentile_rank_list, a, kind='rank'))            

    for b in Sec_of_State_2012_percentile_rank_list:
        Sec_of_State_2012_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2012_percentile_rank_list, b, kind='rank'))            

    for c in Sec_of_State_2013_percentile_rank_list:
        Sec_of_State_2013_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2013_percentile_rank_list, c, kind='rank'))            

    for d in Sec_of_State_2014_percentile_rank_list:
        Sec_of_State_2014_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2014_percentile_rank_list, d, kind='rank'))            

    for e in Sec_of_State_2015_percentile_rank_list:
        Sec_of_State_2015_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2015_percentile_rank_list, e, kind='rank'))            

    for f in Sec_of_State_2016_percentile_rank_list:
        Sec_of_State_2016_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2016_percentile_rank_list, f, kind='rank'))            

    for j in Sec_of_State_2017_percentile_rank_list:
        Sec_of_State_2017_percentile_rank_list_factored.append(stats.percentileofscore(Sec_of_State_2017_percentile_rank_list, j, kind='rank'))            


    for g in Total_Sec_of_State_percentile_rank_list:
        Total_Sec_of_State_percentile_rank_list_factored.append(stats.percentileofscore(Total_Sec_of_State_percentile_rank_list, g, kind='rank'))            

    # Weighting of Age more heavily
    Sec_of_State_2012_percentile_rank_list_factored = [i * 1.1 for i in Sec_of_State_2012_percentile_rank_list_factored]
    Sec_of_State_2013_percentile_rank_list_factored = [i * 1.2 for i in Sec_of_State_2013_percentile_rank_list_factored]
    Sec_of_State_2014_percentile_rank_list_factored = [i * 1.3 for i in Sec_of_State_2014_percentile_rank_list_factored]
    Sec_of_State_2015_percentile_rank_list_factored = [i * 1.4 for i in Sec_of_State_2015_percentile_rank_list_factored]
    Sec_of_State_2016_percentile_rank_list_factored = [i * 1.5 for i in Sec_of_State_2016_percentile_rank_list_factored]
    Sec_of_State_2017_percentile_rank_list_factored = [i * 1.6 for i in Sec_of_State_2017_percentile_rank_list_factored]
    Total_Sec_of_State_percentile_rank_list_factored = [i * 1.7 for i in Total_Sec_of_State_percentile_rank_list_factored]
    
    total_sec_state_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        sec_state_rank_data_together = (Sec_of_State_2011_percentile_rank_list_factored[country_num],
                                        Sec_of_State_2012_percentile_rank_list_factored[country_num],
                                        Sec_of_State_2013_percentile_rank_list_factored[country_num],
                                        Sec_of_State_2014_percentile_rank_list_factored[country_num],
                                        Sec_of_State_2015_percentile_rank_list_factored[country_num],
                                        Sec_of_State_2016_percentile_rank_list_factored[country_num],
                                        Sec_of_State_2017_percentile_rank_list_factored[country_num],
                                        Total_Sec_of_State_percentile_rank_list_factored[country_num])
        total_sec_state_rank[str(country)] = sec_state_rank_data_together                                      
    
    sec_state_rank_aggregate_factored = []
    for country in country_name_list:
        tbr = total_sec_state_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        
        sec_state_rank_aggregate_factored.append(tbr)

    return {'sec_state_rank_aggregate_factored':sec_state_rank_aggregate_factored}
