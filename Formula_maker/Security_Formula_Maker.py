# -*- coding: utf-8 -*-
#! Security Profile

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier

def SPFM(country_name_list, country_and_percentile_rank_list):
    military_power_percentile_rank_list = []
    foreign_power_percentile_rank_list = []
    nuclear_power_percentile_rank_list = []
    alliance_climate_percentile_rank_list = []
    rank_percentile_rank_list = []

    for country in country_name_list:
        country = int(country_numberifier(country))
        Military_Power = (country_and_percentile_rank_list['TOTAL US MILITARY Personnel Abroad'][country] +
                                country_and_percentile_rank_list['US Military Bases Abroad'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Military_Power]))
        real_len = int(len(Military_Power)/2)
        dvisible_number = int(real_len - number_of_nan)
        biz_sum = np.nansum(Military_Power[1::2])
        Military_Power = biz_sum / dvisible_number
        military_power_percentile_rank_list.append(Military_Power)


        Foreign_Power = (country_and_percentile_rank_list['Foreign Military Finance'][country] +
                                country_and_percentile_rank_list['Personel in Standing Army'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Foreign_Power]))
        real_len = int(len(Foreign_Power)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Foreign_Power[1::2])
        Foreign_Power_num = num_sum / dvisible_number
        foreign_power_percentile_rank_list.append(Foreign_Power_num)

        Nuclear_Technology = (country_and_percentile_rank_list['Nuclear Technology'][country])
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Nuclear_Technology]))
        real_len = int(len(Nuclear_Technology)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Nuclear_Technology[1::2])
        Nuclear_Technology = num_sum / dvisible_number
        nuclear_power_percentile_rank_list.append(Nuclear_Technology)

        Alliance_Climate = (country_and_percentile_rank_list['Alliances'][country] +
                                country_and_percentile_rank_list['Shared Multilateral Organizations'][country])

        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Alliance_Climate]))
        real_len = int(len(Alliance_Climate)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Alliance_Climate[1::2])
        Alliance_Climate = num_sum / dvisible_number
        alliance_climate_percentile_rank_list.append(Alliance_Climate)

        Rankings = (country_and_percentile_rank_list['Composite Index of National Capability'][country] +
                                country_and_percentile_rank_list['Global Peace Index Raw Score'][country])

        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in Rankings]))
        real_len = int(len(Rankings)/2)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(Rankings[1::2])
        Rankings = num_sum / dvisible_number
        rank_percentile_rank_list.append(Rankings)

    #PERCENTILING COMPOSITES AND FACTORIZATION
    military_power_percentile_rank_list_factored = []
    alliance_climate_percentile_rank_list_factored = []
    rank_percentile_rank_list_factored = []
    foreign_power_percentile_rank_list_factored = []

    for a in military_power_percentile_rank_list:
        military_power_percentile_rank_list_factored.append(stats.percentileofscore(military_power_percentile_rank_list, a, kind='rank'))

    for c in alliance_climate_percentile_rank_list:
        alliance_climate_percentile_rank_list_factored.append(stats.percentileofscore(alliance_climate_percentile_rank_list, c, kind='rank'))

    for d in rank_percentile_rank_list:
        rank_percentile_rank_list_factored.append(stats.percentileofscore(rank_percentile_rank_list, d, kind='rank'))

    for j in foreign_power_percentile_rank_list:
        foreign_power_percentile_rank_list_factored.append(stats.percentileofscore(foreign_power_percentile_rank_list, j, kind='rank'))

    # Weighting of Size more heavily
    """
    people_power_percentile_rank_list_factored = [i * 3 for i in people_power_percentile_rank_list_factored]
    """
    nuclear_power_percentile_rank_list = [i * 4 for i in nuclear_power_percentile_rank_list]

    total_security_rank = {}
    for country in country_name_list:
        country_num = int(country_numberifier(country))
        security_rank_data_together = (military_power_percentile_rank_list_factored[country_num],
                                        nuclear_power_percentile_rank_list[country_num],
                                        alliance_climate_percentile_rank_list_factored[country_num],
                                        rank_percentile_rank_list_factored[country_num],
                                        foreign_power_percentile_rank_list_factored[country_num])
        total_security_rank[str(country)] = security_rank_data_together

    security_rank_aggregate_factored = []
    for country in country_name_list:
        tbr = total_security_rank[country]
        #Factoring for number of missing data Fields and averaging the raw score
        number_of_nan = int(sum([pd.isnull(i) for i in tbr]))
        real_len = len(tbr)
        dvisible_number = int(real_len - number_of_nan)
        num_sum = np.nansum(tbr)
        tbr = num_sum / dvisible_number
        new_tbr = float(tbr) / 1.51
        security_rank_aggregate_factored.append(new_tbr)

    return {'security_rank_aggregate_factored':security_rank_aggregate_factored}
