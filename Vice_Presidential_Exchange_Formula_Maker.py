# -*- coding: utf-8 -*-
#! Prestige Formula Maker
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier
 
def VPFM(country_name_list, country_and_percentile_rank_list):
    VP_2011_percentile_rank_list = []
    VP_2012_percentile_rank_list = []
    VP_2013_percentile_rank_list = []
    VP_2014_percentile_rank_list = []
    VP_2015_percentile_rank_list = []
    VP_2016_percentile_rank_list = []
    Total_VP_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        VP_2011 = (country_and_percentile_rank_list['VP_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in VP_2011]))
        real_len = int(len(VP_2011)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(VP_2011[1::2])
        VP_2011 = biz_sum / dvisible_number 
        VP_2011_percentile_rank_list.append(VP_2011)

        #2012
        VP_2012 = (country_and_percentile_rank_list['VP_2012'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in VP_2012]))
        real_len = int(len(VP_2012)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(VP_2012[1::2])
        VP_2012 = biz_sum / dvisible_number 
        VP_2012_percentile_rank_list.append(VP_2012)

        #2013
        VP_2013 = (country_and_percentile_rank_list['VP_2013'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in VP_2013]))
        real_len = int(len(VP_2013)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(VP_2013[1::2])
        VP_2013 = biz_sum / dvisible_number 
        VP_2013_percentile_rank_list.append(VP_2013)

        #2014
        VP_2014 = (country_and_percentile_rank_list['VP_2014'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in VP_2014]))
        real_len = int(len(VP_2014)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(VP_2014[1::2])
        VP_2014 = biz_sum / dvisible_number 
        VP_2014_percentile_rank_list.append(VP_2014)

        #2015
        VP_2015 = (country_and_percentile_rank_list['VP_2015'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in VP_2015]))
        real_len = int(len(VP_2015)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(VP_2015[1::2])
        VP_2015 = biz_sum / dvisible_number 
        VP_2015_percentile_rank_list.append(VP_2015)

        #2016
        VP_2016 = (country_and_percentile_rank_list['VP_2016'][country])      
        number_of_nan = int(sum([pd.isnull(i) for i in VP_2016]))
        real_len = int(len(VP_2016)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(VP_2016[1::2])
        VP_2016 = biz_sum / dvisible_number 
        VP_2016_percentile_rank_list.append(VP_2016)

        #TOTAL
        Total_VP = (country_and_percentile_rank_list['VP_2016'][country] +
                              country_and_percentile_rank_list['VP_2015'][country] +
                              country_and_percentile_rank_list['VP_2014'][country] +
                              country_and_percentile_rank_list['VP_2013'][country] +
                              country_and_percentile_rank_list['VP_2012'][country] +
                              country_and_percentile_rank_list['VP_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in Total_VP]))
        real_len = int(len(Total_VP)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Total_VP[1::2])
        Total_VP = biz_sum / dvisible_number 
        Total_VP_percentile_rank_list.append(Total_VP)


    #PERCENTILING COMPOSITES AND FACTORIZATION
    VP_2011_percentile_rank_list_factored = []
    VP_2012_percentile_rank_list_factored = []
    VP_2013_percentile_rank_list_factored = []
    VP_2014_percentile_rank_list_factored = []
    VP_2015_percentile_rank_list_factored = []
    VP_2016_percentile_rank_list_factored = []
    Total_VP_percentile_rank_list_factored = []

    for a in VP_2011_percentile_rank_list:
        VP_2011_percentile_rank_list_factored.append(stats.percentileofscore(VP_2011_percentile_rank_list, a, kind='rank'))            

    for b in VP_2012_percentile_rank_list:
        VP_2012_percentile_rank_list_factored.append(stats.percentileofscore(VP_2012_percentile_rank_list, b, kind='rank'))            

    for c in VP_2013_percentile_rank_list:
        VP_2013_percentile_rank_list_factored.append(stats.percentileofscore(VP_2013_percentile_rank_list, c, kind='rank'))            

    for d in VP_2014_percentile_rank_list:
        VP_2014_percentile_rank_list_factored.append(stats.percentileofscore(VP_2014_percentile_rank_list, d, kind='rank'))            

    for e in VP_2015_percentile_rank_list:
        VP_2015_percentile_rank_list_factored.append(stats.percentileofscore(VP_2015_percentile_rank_list, e, kind='rank'))            

    for f in VP_2016_percentile_rank_list:
        VP_2016_percentile_rank_list_factored.append(stats.percentileofscore(VP_2016_percentile_rank_list, f, kind='rank'))            

    for g in Total_VP_percentile_rank_list:
        Total_VP_percentile_rank_list_factored.append(stats.percentileofscore(Total_VP_percentile_rank_list, g, kind='rank'))            

    # Weighting of Age more heavily
    VP_2012_percentile_rank_list_factored = [i * 1.1 for i in VP_2012_percentile_rank_list_factored]
    VP_2013_percentile_rank_list_factored = [i * 1.2 for i in VP_2013_percentile_rank_list_factored]
    VP_2014_percentile_rank_list_factored = [i * 1.3 for i in VP_2014_percentile_rank_list_factored]
    VP_2015_percentile_rank_list_factored = [i * 1.4 for i in VP_2015_percentile_rank_list_factored]
    VP_2016_percentile_rank_list_factored = [i * 1.5 for i in VP_2016_percentile_rank_list_factored]
    Total_VP_percentile_rank_list_factored = [i * 1.6 for i in Total_VP_percentile_rank_list_factored]
    
    total_VP_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        VP_rank_data_together = (VP_2011_percentile_rank_list_factored[country_num],
                                        VP_2012_percentile_rank_list_factored[country_num],
                                        VP_2013_percentile_rank_list_factored[country_num],
                                        VP_2014_percentile_rank_list_factored[country_num],
                                        VP_2015_percentile_rank_list_factored[country_num],
                                        VP_2016_percentile_rank_list_factored[country_num],
                                        Total_VP_percentile_rank_list_factored[country_num])
        total_VP_rank[str(country)] = VP_rank_data_together                                      
    
    VP_rank_aggregate_factored = []
    for country in country_name_list:
        tbr = total_VP_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        
        VP_rank_aggregate_factored.append(tbr)

    return {'VP_rank_aggregate_factored':VP_rank_aggregate_factored}
