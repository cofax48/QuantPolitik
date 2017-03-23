# -*- coding: utf-8 -*-
#! Cultural Diffusion Maker

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier
 
def CDFM(country_name_list, country_and_percentile_rank_list):
    ease_of_travel_percentile_rank_list = []
    americana_abroad_percentile_rank_list = []
    immigration_percentile_rank_list = []
    ulterior_interaction_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Ease_Of_Travel = (country_and_percentile_rank_list['Visa_Requirements_for_US_Citizens'][country] +
                                country_and_percentile_rank_list['Total_Non_Immigrant_Arrivals_Visitation_to_the_US_FY_2014'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Ease_Of_Travel]))
        real_len = int(len(Ease_Of_Travel)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Ease_Of_Travel[1::2])
        Ease_Of_Travel = biz_sum / dvisible_number
        ease_of_travel_percentile_rank_list.append(Ease_Of_Travel)
        
        Americana_Abroad = (country_and_percentile_rank_list['McDonald_Locations_in_country'][country] +
                                country_and_percentile_rank_list['Starbucks'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Americana_Abroad]))
        real_len = int(len(Americana_Abroad)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Americana_Abroad[1::2])
        Americana_Abroad = num_sum / dvisible_number           
        americana_abroad_percentile_rank_list.append(Americana_Abroad)
        
        Immigration = (country_and_percentile_rank_list['Immigration_to_the_US_2010'][country] +
                                country_and_percentile_rank_list['Immigration_to_the_US_2011'][country] +
                                country_and_percentile_rank_list['Immigration_to_the_US_2012'][country] +
                                country_and_percentile_rank_list['Immigration_to_the_US_2013'][country] +
                                country_and_percentile_rank_list['Immigration_to_the_US_2014'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Immigration]))
        real_len = int(len(Immigration)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Immigration[1::2])
        Immigration = num_sum / dvisible_number
        immigration_percentile_rank_list.append(Immigration)

        Ulterior_Interaction = (country_and_percentile_rank_list['Total_Tourists_and_Business_Arrival_Visitation_to_the_US_FY_201'][country] +
                                country_and_percentile_rank_list['Students_and_exchange_visitors_Visitation_to_the_US_FY_2014'][country] +
                                country_and_percentile_rank_list['Temporary_workers_and_families_Visitation_to_the_US_FY_2014'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Ulterior_Interaction]))
        real_len = int(len(Ulterior_Interaction)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Ulterior_Interaction[1::2])
        Ulterior_Interaction = num_sum / dvisible_number
        ulterior_interaction_percentile_rank_list.append(Ulterior_Interaction)

    #PERCENTILING COMPOSITES AND FACTORIZATION
    ease_of_travel_percentile_rank_list_factored = []
    americana_abroad_percentile_rank_list_factored = []
    immigration_percentile_rank_list_factored = []
    ulterior_interaction_percentile_rank_list_factored = []


    for a in ease_of_travel_percentile_rank_list:
        ease_of_travel_percentile_rank_list_factored.append(stats.percentileofscore(ease_of_travel_percentile_rank_list, a, kind='rank'))            

    for b in americana_abroad_percentile_rank_list:
        americana_abroad_percentile_rank_list_factored.append(stats.percentileofscore(americana_abroad_percentile_rank_list, b, kind='rank'))

    for c in immigration_percentile_rank_list:
        immigration_percentile_rank_list_factored.append(stats.percentileofscore(immigration_percentile_rank_list, c, kind='rank'))

    for d in ulterior_interaction_percentile_rank_list:
        ulterior_interaction_percentile_rank_list_factored.append(stats.percentileofscore(ulterior_interaction_percentile_rank_list, d, kind='rank'))
    

                                                                  
    cultural_diffusion_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        cultural_diffusion_rank_data_together = (ease_of_travel_percentile_rank_list_factored[country_num],
                                        americana_abroad_percentile_rank_list_factored[country_num],
                                        immigration_percentile_rank_list_factored[country_num],
                                        ulterior_interaction_percentile_rank_list_factored[country_num])
        cultural_diffusion_rank[str(country)] = cultural_diffusion_rank_data_together                                        
    
    cultural_diffusion_aggregate_factored = []
    for country in country_name_list:
        tbr = cultural_diffusion_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        cultural_diffusion_aggregate_factored.append(tbr)

    return {'cultural_diffusion_aggregate_factored':cultural_diffusion_aggregate_factored}
