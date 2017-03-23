# -*- coding: utf-8 -*-
#! Prestige Formula Maker
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier
 
def JMFM(country_name_list, country_and_percentile_rank_list):
    JM_2011_percentile_rank_list = []
    JM_2012_percentile_rank_list = []
    JM_2013_percentile_rank_list = []
    JM_2014_percentile_rank_list = []
    JM_2015_percentile_rank_list = []
    JM_2016_percentile_rank_list = []
    Total_JM_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        JM_2011 = (country_and_percentile_rank_list['JM_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in JM_2011]))
        real_len = int(len(JM_2011)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(JM_2011[1::2])
        JM_2011 = biz_sum / dvisible_number 
        JM_2011_percentile_rank_list.append(JM_2011)

        #2012
        JM_2012 = (country_and_percentile_rank_list['JM_2012'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in JM_2012]))
        real_len = int(len(JM_2012)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(JM_2012[1::2])
        JM_2012 = biz_sum / dvisible_number 
        JM_2012_percentile_rank_list.append(JM_2012)

        #2013
        JM_2013 = (country_and_percentile_rank_list['JM_2013'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in JM_2013]))
        real_len = int(len(JM_2013)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(JM_2013[1::2])
        JM_2013 = biz_sum / dvisible_number 
        JM_2013_percentile_rank_list.append(JM_2013)

        #2014
        JM_2014 = (country_and_percentile_rank_list['JM_2014'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in JM_2014]))
        real_len = int(len(JM_2014)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(JM_2014[1::2])
        JM_2014 = biz_sum / dvisible_number 
        JM_2014_percentile_rank_list.append(JM_2014)

        #2015
        JM_2015 = (country_and_percentile_rank_list['JM_2015'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in JM_2015]))
        real_len = int(len(JM_2015)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(JM_2015[1::2])
        JM_2015 = biz_sum / dvisible_number 
        JM_2015_percentile_rank_list.append(JM_2015)

        #2016
        JM_2016 = (country_and_percentile_rank_list['JM_2016'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in JM_2016]))
        real_len = int(len(JM_2016)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(JM_2016[1::2])
        JM_2016 = biz_sum / dvisible_number 
        JM_2016_percentile_rank_list.append(JM_2016)

        #TOTAL
        Total_JM = (country_and_percentile_rank_list['JM_2016'][country] +
                              country_and_percentile_rank_list['JM_2015'][country] +
                              country_and_percentile_rank_list['JM_2014'][country] +
                              country_and_percentile_rank_list['JM_2013'][country] +
                              country_and_percentile_rank_list['JM_2012'][country] +
                              country_and_percentile_rank_list['JM_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in Total_JM]))
        real_len = int(len(Total_JM)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Total_JM[1::2])
        Total_JM = biz_sum / dvisible_number 
        Total_JM_percentile_rank_list.append(Total_JM)


    #PERCENTILING COMPOSITES AND FACTORIZATION
    JM_2011_percentile_rank_list_factored = []
    JM_2012_percentile_rank_list_factored = []
    JM_2013_percentile_rank_list_factored = []
    JM_2014_percentile_rank_list_factored = []
    JM_2015_percentile_rank_list_factored = []
    JM_2016_percentile_rank_list_factored = []
    Total_JM_percentile_rank_list_factored = []

    for a in JM_2011_percentile_rank_list:
        JM_2011_percentile_rank_list_factored.append(stats.percentileofscore(JM_2011_percentile_rank_list, a, kind='rank'))            

    for b in JM_2012_percentile_rank_list:
        JM_2012_percentile_rank_list_factored.append(stats.percentileofscore(JM_2012_percentile_rank_list, b, kind='rank'))            

    for c in JM_2013_percentile_rank_list:
        JM_2013_percentile_rank_list_factored.append(stats.percentileofscore(JM_2013_percentile_rank_list, c, kind='rank'))            

    for d in JM_2014_percentile_rank_list:
        JM_2014_percentile_rank_list_factored.append(stats.percentileofscore(JM_2014_percentile_rank_list, d, kind='rank'))            

    for e in JM_2015_percentile_rank_list:
        JM_2015_percentile_rank_list_factored.append(stats.percentileofscore(JM_2015_percentile_rank_list, e, kind='rank'))            

    for f in JM_2016_percentile_rank_list:
        JM_2016_percentile_rank_list_factored.append(stats.percentileofscore(JM_2016_percentile_rank_list, f, kind='rank'))            

    for g in Total_JM_percentile_rank_list:
        Total_JM_percentile_rank_list_factored.append(stats.percentileofscore(Total_JM_percentile_rank_list, g, kind='rank'))            

    # Weighting of Age more heavily
    JM_2012_percentile_rank_list_factored = [i * 1.1 for i in JM_2012_percentile_rank_list_factored]
    JM_2013_percentile_rank_list_factored = [i * 1.2 for i in JM_2013_percentile_rank_list_factored]
    JM_2014_percentile_rank_list_factored = [i * 1.3 for i in JM_2014_percentile_rank_list_factored]
    JM_2015_percentile_rank_list_factored = [i * 1.4 for i in JM_2015_percentile_rank_list_factored]
    JM_2016_percentile_rank_list_factored = [i * 1.5 for i in JM_2016_percentile_rank_list_factored]
    Total_JM_percentile_rank_list_factored = [i * 1.6 for i in Total_JM_percentile_rank_list_factored]
    
    total_JM_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        JM_rank_data_together = (JM_2011_percentile_rank_list_factored[country_num],
                                        JM_2012_percentile_rank_list_factored[country_num],
                                        JM_2013_percentile_rank_list_factored[country_num],
                                        JM_2014_percentile_rank_list_factored[country_num],
                                        JM_2015_percentile_rank_list_factored[country_num],
                                        JM_2016_percentile_rank_list_factored[country_num],
                                        Total_JM_percentile_rank_list_factored[country_num])
        total_JM_rank[str(country)] = JM_rank_data_together                                      
    
    JM_rank_aggregate_factored = []
    for country in country_name_list:
        tbr = total_JM_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        
        JM_rank_aggregate_factored.append(tbr)

    return {'JM_rank_aggregate_factored':JM_rank_aggregate_factored}
