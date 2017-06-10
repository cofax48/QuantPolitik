# -*- coding: utf-8 -*-
#! Business Relations Formula Maker

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier

def BRFM(country_name_list, country_and_percentile_rank_list):
    #Total Business Score
    total_business_rank_percentile_list = []

    business_climate_percentile_rank_list = []
    corporate_climate_percentile_rank_list = []
    financial_climate_percentile_rank_list = []
    composite_climate_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Business_Climate = (country_and_percentile_rank_list['Starting a Business'][country] +
                                country_and_percentile_rank_list['Dealing with Construction Permits'][country] +
                                country_and_percentile_rank_list['Getting Electricity'][country] +
                                country_and_percentile_rank_list['Registering Property'][country] +
                                country_and_percentile_rank_list['Property Rights'][country] +
                                country_and_percentile_rank_list['Getting Credit'][country] +
                                country_and_percentile_rank_list['Resolving Insolvency'][country])
        print(country, Business_Climate)
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Business_Climate]))
        real_len = int(len(Business_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Business_Climate[1::2])
        Business_Climate = biz_sum / dvisible_number
        business_climate_percentile_rank_list.append(Business_Climate)

        Corporate_Climate = (country_and_percentile_rank_list['Paying Taxes'][country] +
                                country_and_percentile_rank_list['Trading Across Borders'][country] +
                                country_and_percentile_rank_list['Enforcing Contracts'][country] +
                                country_and_percentile_rank_list['Business Freedom'][country] +
                                country_and_percentile_rank_list['Corporate Tax Rate Percentage'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Corporate_Climate]))
        real_len = int(len(Corporate_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Corporate_Climate[1::2])
        Corporate_Climate = num_sum / dvisible_number
        corporate_climate_percentile_rank_list.append(Corporate_Climate)

        Financial_Climate = (country_and_percentile_rank_list['Protecting Minority Investors'][country] +
                                country_and_percentile_rank_list['Monetary Freedom'][country] +
                                country_and_percentile_rank_list['Fiscal Freedom'][country] +
                                country_and_percentile_rank_list['Investment Freedom'][country] +
                                country_and_percentile_rank_list['Financial Freedom'][country] +
                                country_and_percentile_rank_list['Remittances'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Financial_Climate]))
        real_len = int(len(Financial_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Financial_Climate[1::2])
        Financial_Climate = num_sum / dvisible_number
        financial_climate_percentile_rank_list.append(Financial_Climate)

        Composite_Indices = (country_and_percentile_rank_list['Ease of Doing Business Rank'][country] +
                                country_and_percentile_rank_list['Economic Freedom World Rank'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Composite_Indices]))
        real_len = int(len(Composite_Indices)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Composite_Indices[1::2])
        Composite_Indices = num_sum / dvisible_number
        composite_climate_percentile_rank_list.append(Composite_Indices)



    #PERCENTILING COMPOSITES AND FACTORIZATION
    business_climate_percentile_rank_list_factored = []
    corporate_climate_percentile_rank_list_factored = []
    financial_climate_percentile_rank_list_factored = []
    composite_climate_percentile_rank_list_factored = []


    for a in business_climate_percentile_rank_list:
        business_climate_percentile_rank_list_factored.append(stats.percentileofscore(business_climate_percentile_rank_list, a, kind='rank'))

    for b in corporate_climate_percentile_rank_list:
        corporate_climate_percentile_rank_list_factored.append(stats.percentileofscore(corporate_climate_percentile_rank_list, b, kind='rank'))

    for c in financial_climate_percentile_rank_list:
        financial_climate_percentile_rank_list_factored.append(stats.percentileofscore(financial_climate_percentile_rank_list, c, kind='rank'))

    for d in composite_climate_percentile_rank_list:
        composite_climate_percentile_rank_list_factored.append(stats.percentileofscore(composite_climate_percentile_rank_list, d, kind='rank'))

    total_business_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        business_rank_data_together = (business_climate_percentile_rank_list_factored[country_num],
                                        corporate_climate_percentile_rank_list_factored[country_num],
                                        financial_climate_percentile_rank_list_factored[country_num],
                                        composite_climate_percentile_rank_list_factored[country_num])
        total_business_rank[str(country)] = business_rank_data_together

    business_relations_aggregate_factored = []
    for country in country_name_list:
        tbr = total_business_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        business_relations_aggregate_factored.append(tbr)

    return {'business_relations_aggregate_factored':business_relations_aggregate_factored}
