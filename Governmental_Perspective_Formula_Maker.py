# -*- coding: utf-8 -*-
#! Governmental Perspective Relations Formula Maker

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier

def UN_Grabber(engine):
    #For some reason Postgres kept mishandling the data and corrupting it everytime this
    #datafild was entered into the database on existing tabl
    country_name = pd.read_sql('SELECT "Country_Name" FROM "UN";', engine)
    data_column = pd.read_sql('SELECT "Voting correlation in Percentage at UN with the US" FROM "UN";', engine)

    country_name_list = []
    country_df = pd.DataFrame(country_name)
    for index, row in country_df.iterrows():
        country_name_list.append(row.to_string(index=False))
        
    country_and_percentile_rank_list = {}
    df = pd.DataFrame(data_column)
    #Makes Each data point a number
    whole_column_list = []
    for index, row in df.iterrows():
        if pd.isnull(np.asscalar(row)) == True:
            whole_column_list.append(np.nan)
        else:
            whole_column_list.append(np.asscalar(np.float64(row)))
    #prints the percentile rank for ach country
    column_percentile_list = []
    for a in whole_column_list:
        column_percentile_list.append(stats.percentileofscore(whole_column_list, a, kind='rank'))
    zipped_list = list(zip(country_name_list, column_percentile_list))

    return {'zipped_list':zipped_list}

 
def GRFM(country_name_list, country_and_percentile_rank_list):
    outlook_climate_percentile_rank_list = []
    political_climate_percentile_rank_list = []
    financial_climate_percentile_rank_list = []
    global_climate_percentile_rank_list = []
    UN_climate_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Outlook = (country_and_percentile_rank_list['World Giving Index'][country] +
                                country_and_percentile_rank_list['Science and Technology'][country] +
                                country_and_percentile_rank_list['Culture'][country] +
                                country_and_percentile_rank_list['Prosperity and Equality'][country] +
                                country_and_percentile_rank_list['Health and Wellbeing'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Outlook]))
        real_len = int(len(Outlook)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Outlook[1::2])
        Outlook = biz_sum / dvisible_number
        
        outlook_climate_percentile_rank_list.append(Outlook)
        
        Political_Climate = (country_and_percentile_rank_list['Political Freedom'][country] +
                                country_and_percentile_rank_list['Civil Liberties'][country] +
                                country_and_percentile_rank_list['Freedom Status'][country] +
                                country_and_percentile_rank_list['Freedom from Corruption'][country] +
                                country_and_percentile_rank_list['Political Terror Scale'][country] +
                                country_and_percentile_rank_list['Press Freedom Rank'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Political_Climate]))
        real_len = int(len(Political_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Political_Climate[1::2])
        Political_Climate = num_sum / dvisible_number           
        political_climate_percentile_rank_list.append(Political_Climate)
        
        Financial_Climate = (country_and_percentile_rank_list['Gini Coefficent'][country] +
                                country_and_percentile_rank_list['Labor Freedom'][country] +
                                country_and_percentile_rank_list['Tariff Rate in Percentage'][country] +
                                country_and_percentile_rank_list['Income Tax Rate in Percentage'][country] +
                                country_and_percentile_rank_list['Tax Burden as Percent of GDP'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Financial_Climate]))
        real_len = int(len(Financial_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Financial_Climate[1::2])
        Financial_Climate = num_sum / dvisible_number
        financial_climate_percentile_rank_list.append(Financial_Climate)

        Global_Climate = (country_and_percentile_rank_list['Good Country Overall Score'][country] +
                                country_and_percentile_rank_list['International Peace and Security'][country] +
                                country_and_percentile_rank_list['World Order'][country] +
                                country_and_percentile_rank_list['Planet and Climate'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Global_Climate]))
        real_len = int(len(Global_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Global_Climate[1::2])
        Global_Climate = num_sum / dvisible_number
        global_climate_percentile_rank_list.append(Global_Climate)
        
        UN_Rank = (country_and_percentile_rank_list['Voting correlation in Percentage at UN with the US'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in UN_Rank]))
        real_len = int(len(UN_Rank)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(UN_Rank[1::2])
        UN_Rank = num_sum / dvisible_number
        UN_climate_percentile_rank_list.append(UN_Rank)

    #PERCENTILING COMPOSITES AND FACTORIZATION
    outlook_climate_percentile_rank_list_factored = []
    political_climate_percentile_rank_list_factored = []
    financial_climate_percentile_rank_list_factored = []
    global_climate_percentile_rank_list_factored = []
    UN_climate_percentile_rank_list_factored = []


    for a in outlook_climate_percentile_rank_list:
        outlook_climate_percentile_rank_list_factored.append(stats.percentileofscore(outlook_climate_percentile_rank_list, a, kind='rank'))            

    for b in political_climate_percentile_rank_list:
        political_climate_percentile_rank_list_factored.append(stats.percentileofscore(political_climate_percentile_rank_list, b, kind='rank'))

    for c in financial_climate_percentile_rank_list:
        financial_climate_percentile_rank_list_factored.append(stats.percentileofscore(financial_climate_percentile_rank_list, c, kind='rank'))

    for d in global_climate_percentile_rank_list:
        global_climate_percentile_rank_list_factored.append(stats.percentileofscore(global_climate_percentile_rank_list, d, kind='rank'))

    for e in UN_climate_percentile_rank_list:
        UN_climate_percentile_rank_list_factored.append(stats.percentileofscore(UN_climate_percentile_rank_list, e, kind='rank'))

    

                                                                  
    total_governmental_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        governmental_rank_data_together = (outlook_climate_percentile_rank_list_factored[country_num],
                                        political_climate_percentile_rank_list_factored[country_num],
                                        financial_climate_percentile_rank_list_factored[country_num],
                                        global_climate_percentile_rank_list_factored[country_num],
                                        UN_climate_percentile_rank_list_factored[country_num])
        total_governmental_rank[str(country)] = governmental_rank_data_together                                         
    
    governmental_relations_aggregate_factored = []
    for country in country_name_list:
        tbr = total_governmental_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        governmental_relations_aggregate_factored.append(tbr)

    return {'governmental_relations_aggregate_factored':governmental_relations_aggregate_factored}
