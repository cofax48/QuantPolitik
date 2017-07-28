# -*- coding: utf-8 -*-
#! Prestige Formula Maker
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier

def PEFM(country_name_list, country_and_percentile_rank_list):
    Pres_2011_percentile_rank_list = []
    Pres_2012_percentile_rank_list = []
    Pres_2013_percentile_rank_list = []
    Pres_2014_percentile_rank_list = []
    Pres_2015_percentile_rank_list = []
    Pres_2016_percentile_rank_list = []
    Pres_2017_percentile_rank_list = []
    Total_Pres_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Pres_2011 = (country_and_percentile_rank_list['Pres_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2011]))
        real_len = int(len(Pres_2011)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2011[1::2])
        Pres_2011 = biz_sum / dvisible_number
        Pres_2011_percentile_rank_list.append(Pres_2011)

        #2012
        Pres_2012 = (country_and_percentile_rank_list['Pres_2012'][country])
        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2012]))
        real_len = int(len(Pres_2012)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2012[1::2])
        Pres_2012 = biz_sum / dvisible_number
        Pres_2012_percentile_rank_list.append(Pres_2012)

        #2013
        Pres_2013 = (country_and_percentile_rank_list['Pres_2013'][country])
        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2013]))
        real_len = int(len(Pres_2013)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2013[1::2])
        Pres_2013 = biz_sum / dvisible_number
        Pres_2013_percentile_rank_list.append(Pres_2013)

        #2014
        Pres_2014 = (country_and_percentile_rank_list['Pres_2014'][country])
        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2014]))
        real_len = int(len(Pres_2014)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2014[1::2])
        Pres_2014 = biz_sum / dvisible_number
        Pres_2014_percentile_rank_list.append(Pres_2014)

        #2015
        Pres_2015 = (country_and_percentile_rank_list['Pres_2015'][country])
        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2015]))
        real_len = int(len(Pres_2015)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2015[1::2])
        Pres_2015 = biz_sum / dvisible_number
        Pres_2015_percentile_rank_list.append(Pres_2015)

        #2016
        Pres_2016 = (country_and_percentile_rank_list['Pres_2016'][country])
        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2016]))
        real_len = int(len(Pres_2016)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2016[1::2])
        Pres_2016 = biz_sum / dvisible_number
        Pres_2016_percentile_rank_list.append(Pres_2016)

        #2017
        Pres_2017 = (country_and_percentile_rank_list['Pres_2017'][country])
        number_of_nan = int(sum([pd.isnull(i) for i in Pres_2017]))
        real_len = int(len(Pres_2017)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Pres_2017[1::2])
        Pres_2017 = biz_sum / dvisible_number
        Pres_2017_percentile_rank_list.append(Pres_2017)

        #TOTAL
        Total_Pres = (country_and_percentile_rank_list['Pres_2017'][country] +
                              country_and_percentile_rank_list['Pres_2016'][country] +
                              country_and_percentile_rank_list['Pres_2015'][country] +
                              country_and_percentile_rank_list['Pres_2014'][country] +
                              country_and_percentile_rank_list['Pres_2013'][country] +
                              country_and_percentile_rank_list['Pres_2012'][country] +
                              country_and_percentile_rank_list['Pres_2011'][country])

        number_of_nan = int(sum([pd.isnull(i) for i in Total_Pres]))
        real_len = int(len(Total_Pres)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Total_Pres[1::2])
        Total_Pres = biz_sum / dvisible_number
        Total_Pres_percentile_rank_list.append(Total_Pres)


    #PERCENTILING COMPOSITES AND FACTORIZATION
    Pres_2011_percentile_rank_list_factored = []
    Pres_2012_percentile_rank_list_factored = []
    Pres_2013_percentile_rank_list_factored = []
    Pres_2014_percentile_rank_list_factored = []
    Pres_2015_percentile_rank_list_factored = []
    Pres_2016_percentile_rank_list_factored = []
    Pres_2017_percentile_rank_list_factored = []
    Total_Pres_percentile_rank_list_factored = []

    for a in Pres_2011_percentile_rank_list:
        Pres_2011_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2011_percentile_rank_list, a, kind='rank'))

    for b in Pres_2012_percentile_rank_list:
        Pres_2012_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2012_percentile_rank_list, b, kind='rank'))

    for c in Pres_2013_percentile_rank_list:
        Pres_2013_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2013_percentile_rank_list, c, kind='rank'))

    for d in Pres_2014_percentile_rank_list:
        Pres_2014_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2014_percentile_rank_list, d, kind='rank'))

    for e in Pres_2015_percentile_rank_list:
        Pres_2015_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2015_percentile_rank_list, e, kind='rank'))

    for f in Pres_2016_percentile_rank_list:
        Pres_2016_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2016_percentile_rank_list, f, kind='rank'))

    for h in Pres_2017_percentile_rank_list:
        Pres_2017_percentile_rank_list_factored.append(stats.percentileofscore(Pres_2017_percentile_rank_list, h, kind='rank'))

    for g in Total_Pres_percentile_rank_list:
        Total_Pres_percentile_rank_list_factored.append(stats.percentileofscore(Total_Pres_percentile_rank_list, g, kind='rank'))

    # Weighting of Age more heavily
    Pres_2012_percentile_rank_list_factored = [i * 1.1 for i in Pres_2012_percentile_rank_list_factored]
    Pres_2013_percentile_rank_list_factored = [i * 1.2 for i in Pres_2013_percentile_rank_list_factored]
    Pres_2014_percentile_rank_list_factored = [i * 1.3 for i in Pres_2014_percentile_rank_list_factored]
    Pres_2015_percentile_rank_list_factored = [i * 1.4 for i in Pres_2015_percentile_rank_list_factored]
    Pres_2016_percentile_rank_list_factored = [i * 1.5 for i in Pres_2016_percentile_rank_list_factored]
    Pres_2017_percentile_rank_list_factored = [i * 1.6 for i in Pres_2017_percentile_rank_list_factored]
    Total_Pres_percentile_rank_list_factored = [i * 1.7 for i in Total_Pres_percentile_rank_list_factored]

    total_Pres_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        Pres_rank_data_together = (Pres_2011_percentile_rank_list_factored[country_num],
                                        Pres_2012_percentile_rank_list_factored[country_num],
                                        Pres_2013_percentile_rank_list_factored[country_num],
                                        Pres_2014_percentile_rank_list_factored[country_num],
                                        Pres_2015_percentile_rank_list_factored[country_num],
                                        Pres_2016_percentile_rank_list_factored[country_num],
                                        Pres_2017_percentile_rank_list_factored[country_num],
                                        Total_Pres_percentile_rank_list_factored[country_num])
        total_Pres_rank[str(country)] = Pres_rank_data_together

    Pres_rank_aggregate_factored = []
    for country in country_name_list:
        tbr = total_Pres_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number

        Pres_rank_aggregate_factored.append(tbr)

    return {'Pres_rank_aggregate_factored':Pres_rank_aggregate_factored}
