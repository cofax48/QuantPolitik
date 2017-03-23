#! Data Grabber
import time, datetime
time1 = time.time()
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
import scipy.stats as stats
from country_to_number import country_numberifier

#Engine Creator
engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')

QP_value = {}

def getting_all_the_column_names_from_the_table(table_name):
    column_name_list =  []   
    #Table Grabber
    country_name = pd.read_sql('SELECT "Country_Name" FROM "{}";'.format(table_name), engine)
    data_column = pd.read_sql('SELECT * FROM "{}";'.format(table_name), engine)
    for column in data_column:
        column_name_list.append(column)
        
    country_name_list = []
    country_df = pd.DataFrame(country_name)
    for index, row in country_df.iterrows():
        country_name_list.append(row.to_string(index=False))
        
    return {'column_name_list':column_name_list, 'country_name_list':country_name_list}
                                      
def percentile_ranking(column_name_list, country_name_list, table_name):
        
    #Neg Rankings
    Business_Relations_neg_ranking = [
    'Ease of Doing Business Rank',
    'Starting a Business',
    'Dealing with Construction Permits',
    'Getting Electricity',
    'Registering Property',
    'Getting Credit',
    'Protecting Minority Investors',
    'Paying Taxes',
    'Trading Across Borders',
    'Enforcing Contracts',
    'Resolving Insolvency',
    'Economic Freedom World Rank',
    'Region Rank',
    'Corporate Tax Rate Percentage',
    'Trading Across Borders',
    'Political Freedom',
    'Civil Liberties',
    'Freedom Status',
    'Press Freedom Rank',
    'Good Country Overall Score',
    'World Giving Index',
    'Science and Technology',
    'Culture',
    'International Peace and Security',
    'World Order',
    'Planet and Climate',
    'Prosperity and Equality',
    'Health and Wellbeing',
    'Political Terror Scale',
    'World Giving Index',
    'Gini Coefficent',
    'Unemployment in Percent',
    'Public Debt as Percentage of GDP',
    'Tariff Rate in Percentage',
    'Income Tax Rate in Percentage',
    'Tax Burden as Percent of GDP',
    'Global Peace Index Raw Score'
    ]

    country_and_percentile_rank_list = {}
    
    for reg_column in column_name_list:
        data_column = pd.read_sql('SELECT "{}" FROM "{}";'.format(str(reg_column), table_name), engine)
        df = pd.DataFrame(data_column)
        if str(reg_column) in Business_Relations_neg_ranking:
            #Makes Each data point a number
            whole_column_list = []
            for index, row in df.iterrows():
                if str(reg_column) == 'Country_Name':
                    pass
                else:
                    if pd.isnull(np.asscalar(row)) == True:
                        whole_column_list.append(np.nan)
                    else:
                        whole_column_list.append(np.asscalar(np.float64(row)))
            
            #makes the ranking of 1 to 198 negative so a low score is a higher percentile
            whole_column_list = [x * -1 for x in whole_column_list]
            
            #prints the percentile rank for ach country
            column_percentile_list = []
            for a in whole_column_list:
                column_percentile_list.append(stats.percentileofscore(whole_column_list, a, kind='rank'))
            zipped = list(zip(country_name_list, column_percentile_list))
            if str(reg_column) == str(reg_column):
                country_and_percentile_rank_list[str(reg_column)] = zipped

        elif str(reg_column) not in Business_Relations_neg_ranking:
            #Makes Each data point a number
            whole_column_list = []
            for index, row in df.iterrows():
                if str(reg_column) == 'Country_Name':
                    pass
                else:
                    if pd.isnull(np.asscalar(row)) == True:
                        whole_column_list.append(np.nan)
                    else:
                        whole_column_list.append(np.asscalar(np.float64(row)))
            #Combines the percentile rank for each country
            column_percentile_list = []
            for a in whole_column_list:
                column_percentile_list.append(stats.percentileofscore(whole_column_list, a, kind='rank'))
            zipped = list(zip(country_name_list, column_percentile_list))
            if str(reg_column) == str("Voting correlation in Percentage at UN with the US"):
                from Governmental_Perspective_Formula_Maker import UN_Grabber 
                UN_Result = UN_Grabber(engine)['zipped_list']
                country_and_percentile_rank_list[str(reg_column)] = UN_Result
            else:
                country_and_percentile_rank_list[str(reg_column)] = zipped
                     
    return {'country_and_percentile_rank_list':country_and_percentile_rank_list}

def formula(country_name_list, country_and_percentile_rank_list, table_name):
    if table_name == 'Business_Relations':
        from Business_Relations_Formula_Maker import BRFM
        business_relations_aggregate_factored = BRFM(country_name_list, country_and_percentile_rank_list)['business_relations_aggregate_factored']
        QP_value['Business_Relations'] = business_relations_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Trade_Relations':
        from Trade_Relations_Formula_Maker import TRFM
        trade_relations_aggregate_factored = TRFM(country_name_list, country_and_percentile_rank_list)['trade_relations_aggregate_factored']
        QP_value['Trade_Relations'] = trade_relations_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Governmental_Perspective':
        from Governmental_Perspective_Formula_Maker import GRFM, UN_Grabber 
        governmental_relations_aggregate_factored = GRFM(country_name_list, country_and_percentile_rank_list)['governmental_relations_aggregate_factored']
        QP_value['Governmental_Perspective'] = governmental_relations_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Country_Profile':
        from Country_Profile import CPFM
        country_profile_aggregate_factored = CPFM(country_name_list, country_and_percentile_rank_list)['country_profile_aggregate_factored']
        QP_value['Country_Profile'] = country_profile_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Security':
        from Security_Formula_Maker import SPFM
        security_rank_aggregate_factored = SPFM(country_name_list, country_and_percentile_rank_list)['security_rank_aggregate_factored']
        QP_value['Security'] = security_rank_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Cultural_Diffusion':
        from Cultural_Diffusion_Formula_Maker import CDFM
        cultural_diffusion_aggregate_factored = CDFM(country_name_list, country_and_percentile_rank_list)['cultural_diffusion_aggregate_factored']
        QP_value['Cultural_Diffusion'] = cultural_diffusion_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Prestige':
        from Prestige_Formula_Maker import PFM
        prestige_rank_aggregate_factored = PFM(country_name_list, country_and_percentile_rank_list)['prestige_rank_aggregate_factored']
        QP_value['Prestige'] = prestige_rank_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Sec_State_Bureaucratic_Exchange':
        from Sec_State_Formula_Maker import SSFM
        sec_state_rank_aggregate_factored = SSFM(country_name_list, country_and_percentile_rank_list)['sec_state_rank_aggregate_factored']
        QP_value['Sec_State_Bureaucratic_Exchange'] = sec_state_rank_aggregate_factored
        print(table_name, 'imported')
    if table_name == 'Presidential_Exchange':
        from Presidential_Exchange_Formula_Maker import PEFM
        pres_rank_aggregate_factored = PEFM(country_name_list, country_and_percentile_rank_list)['Pres_rank_aggregate_factored']
        from Vice_Presidential_Exchange_Formula_Maker import VPFM
        vp_rank_aggregate_factored = VPFM(country_name_list, country_and_percentile_rank_list)['VP_rank_aggregate_factored']
        from Joint_Meetings_List import JMFM
        jm_rank_aggregate_factored = JMFM(country_name_list, country_and_percentile_rank_list)['JM_rank_aggregate_factored']        
        
        Pres_VP_Joint_BEX = []
        for country in country_name_list:
            count_num = country_numberifier(country)
            Pres_VP_Joint_BEX.append(float(float(pres_rank_aggregate_factored[count_num] * 3) + float(vp_rank_aggregate_factored[count_num] * 2) + jm_rank_aggregate_factored[count_num]))

        Pres_VP_Joint_BEX_factored = []
        for a in Pres_VP_Joint_BEX:
            Pres_VP_Joint_BEX_factored.append(stats.percentileofscore(Pres_VP_Joint_BEX, a, kind='rank'))            

        QP_value['Presidential_Exchange'] = Pres_VP_Joint_BEX_factored
        print(table_name, 'imported')

        
def main():
    table_list = ['Business_Relations', 'Trade_Relations', 'Governmental_Perspective', 'Country_Profile', 'Security', 'Cultural_Diffusion', 'Prestige', 'Sec_State_Bureaucratic_Exchange', 'Presidential_Exchange']
    for tab in table_list:
        table_name = tab
        country_name_list = getting_all_the_column_names_from_the_table(table_name)['country_name_list']
        column_name_list = getting_all_the_column_names_from_the_table(table_name)['column_name_list']
        country_and_percentile_rank_list = percentile_ranking(column_name_list, country_name_list, table_name)['country_and_percentile_rank_list']
        formula(country_name_list, country_and_percentile_rank_list, table_name)

    QP_Final_Value_not_ranked = []
    for country in country_name_list:
        temp_value_list = []
        for tab in table_list:
            count_num = country_numberifier(country)
            table_name = tab
            if table_name == 'Sec_State_Bureaucratic_Exchange':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.8)
            if table_name == 'Presidential_Exchange':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.7)       
            if table_name == 'Business_Relations':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.6)
            if table_name == 'Trade_Relations':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.5)
            if table_name == 'Governmental_Perspective':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.4)
            if table_name == 'Prestige':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.3)
            if table_name == 'Security':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.2)
            if table_name == 'Cultural_Diffusion':
                temp_value_list.append(float(QP_value[table_name][count_num]) * 1.1)
            if table_name == 'Country_Profile':
                temp_value_list.append(QP_value[table_name][count_num])
            if len(temp_value_list) == 9:
                number_of_nan = int(sum([pd.isnull(i) for i in temp_value_list]))
                real_len = int(len(temp_value_list)/2)
                dvisible_number = int(real_len - number_of_nan)
                num_sum = np.nansum(temp_value_list)
                temp_value_list = num_sum / dvisible_number
                QP_Final_Value_not_ranked.append(temp_value_list)
                
    new_rank_percentile_rank_list_factored = []
    for v in QP_Final_Value_not_ranked:
        new_rank_percentile_rank_list_factored.append(stats.percentileofscore(QP_Final_Value_not_ranked, v, kind='rank'))

    QP_Final_Value = {}
    for country in country_name_list:
        count_num = country_numberifier(country)
        QP_Final_Value[country] = (new_rank_percentile_rank_list_factored[count_num] * 4) - 200

    #To add prior to adding any of the data
    #'''ALTER TABLE "QP_Score" ADD "{}";'''.format(datetime.datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y'))
    conn = engine.connect()

    todays_date = datetime.datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y')
        
    conn.execute('''ALTER TABLE "QP_Score" ADD COLUMN "{}" VARCHAR;'''.format(todays_date))
    conn.execute('''UPDATE "QP_Score" SET "{}" = 0;'''.format(todays_date))
    
    for w in sorted(QP_Final_Value, key=QP_Final_Value.get, reverse=True):
        conn.execute('''UPDATE "QP_Score" SET "{}" = "{}"::bigint + {} WHERE "Country_Name" = '{}';'''.format(todays_date, todays_date, float(QP_Final_Value[w]), w))

        print(w, QP_Final_Value[w])
    
    time2 = time.time()
    print("Total time to run ", int(time2 - time1), "seconds")





