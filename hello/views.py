# coding=utf-8
import json
from datetime import datetime
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from sqlalchemy import create_engine
from hello.country_to_number import country_numberifier
from hello.country_to_number import codex
from hello.country_to_number import iso_numberifier

#Global Variables
engine = create_engine('ma engine') #Not fo you , sorry!
#57600 is 16 hours, which are subtracted so the server only requests date data
#which is generated at 8am eastern or 16 hours after midnight UTC (server time)
todays_date = datetime.fromtimestamp(int(time.time()) - 57600).strftime('%B-%d-%Y')


# My views go here.
def index(request):
    #My index page
    return render(request, 'index.html')

def aboutPage(request):
    return render(request, 'about.html')

def areaOfAnalysis(request):
    return render(request, 'areaOfAnalysis.html')

def dataDashBoard(request):
    return render(request, 'extraNewDashboard.html')

def originalHomePage(request):
    return render(request, 'homePage.html')

def theTech(request):
    return render(request, 'TheTech.html')

def theAlgorithm(request):
    return render(request, 'TheAlgorithm.html')

####Angular Testing

def drSchenkein(request):
    return render(request, 'drSchenkein.html')

def AngularTesting(request):
    return render(request, 'AngularTesting.html')

def SevenminWorkout(request):
    return render(request, '7minWorkout.html')

def DataByCountryAngularApp(request):
    return render(request, 'DataByCountryAngularApp.html')

#########

def JSResume(request):
    return render(request, 'JSResume.html')


#Areas of Analysis
def BureaucraticExchange(request):
    return render(request, 'BureaucraticExchange.html')

def BusinessRelations(request):
    return render(request, 'BusinessRelations.html')

def CountryProfile(request):
    return render(request, 'CountryProfile.html')

def CulturalDiffusion(request):
    return render(request, 'CulturalDiffusion.html')

def GovernmentalPerspective(request):
    return render(request, 'GovernmentalPerspective.html')

def Prestige(request):
    return render(request, 'Prestige.html')

def Security(request):
    return render(request, 'Security.html')

def TradeRelations(request):
    return render(request, 'TradeRelations.html')


#API's
def meeting_json_list(request):
    meeting_json_list_whole = []
    with open("meeting_json_list.json") as f:
        meeting_json_list = json.load(f)
        meeting_json_list_whole.append(meeting_json_list)
    return JsonResponse(meeting_json_list_whole, safe=False)

def country_name_list(request):
    country_name_list_whole = []
    with open("COUNTRY_JSON_AUTHORITATIVE.json") as f:
        country_name_list = json.load(f)
        country_name_list_whole.append(country_name_list)
    return JsonResponse(country_name_list_whole, safe=False)

def get_Table(request):
    #connect to database
    conn = engine.connect()
    #preform query and return json data

    #Eliminate WSGI Get notation
    ABRV_table_name = str(request)[24:]
    ABRV_table_name = ABRV_table_name[:-2]
    ABRV_table_name != 'favicon.ico'
    ABRV_table_name != '/favicon.ico'

    list_return = []

    if '/' in str(ABRV_table_name):
        get_Table_and_Column(request)
    elif 'Dynamic' in str(ABRV_table_name):
        get_Dynamic_Table(request)
    else:

        col_query = conn.execute('''SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}';'''.format(ABRV_table_name))
        col_names = []
        [col_names.append(q[3]) for q in col_query]
        query = conn.execute('SELECT * FROM "{}" ORDER BY "Country_Name";'.format(ABRV_table_name))
        query_list = query.cursor.fetchall()

        iso3_codes = conn.execute('''SELECT "Iso3" FROM "QP_Score" ORDER BY "Country_Name";''')
        iso3_codes_list = iso3_codes.cursor.fetchall()

        country_and_data_dict = []
        for i in range(len(query_list)):
            country = query_list[i][0]
            temp_list = {}
            for c in range(len(col_names)):
                temp_list[col_names[c]] = query_list[i][c]
            temp_list["Iso3"] = iso3_codes_list[i][0]
            country_and_data_dict.append(temp_list)


        list_return.append(country_and_data_dict)

    return JsonResponse(list_return, safe=False)

def get_Table_and_Column(request):
    #r'^api/\w{2,20}/\w{2,20}'
    #connect to database
    conn = engine.connect()
    #preform query and return json data

    #Eliminate WSGI Get notation
    ABRV_table_name = str(request)[24:]
    ABRV_table_name = str(ABRV_table_name)[:-2]

    table_name = ABRV_table_name.rsplit('/', 1)[-1] # table
    country_url = ABRV_table_name.rsplit('/', 2)[-2] # country
    country_name = country_url.replace('%20', ' ')


    query = conn.execute('''SELECT "{}" FROM "{}";'''.format(country_name, table_name))
    query_list = query.cursor.fetchall()

    date_query = conn.execute('''SELECT "Date" FROM "{}";'''.format(table_name))
    date_query_list = date_query.cursor.fetchall()

    country_data_dict = {}
    zipper = zip(query_list, date_query_list)
    for z in zipper:
        country_data_dict[z[1][0]] = z[0][0]

    json_list_to_send = []
    json_list_to_send.append(country_data_dict)


    return JsonResponse(json_list_to_send, safe=False)

def get_Dynamic_Table(request):
    #connect to database
    conn = engine.connect()
    #preform query and return json data

    #Eliminate WSGI Get notation
    print(request)
    ABRV_table_name = str(request)[31:]
    ABRV_table_name = ABRV_table_name[:-2]
    ABRV_table_name != 'favicon.ico'
    ABRV_table_name != '/favicon.ico'

    list_return = []

    print(ABRV_table_name)

    col_name = col_query = conn.execute('''SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'QP_SCORE2';''')
    col_query = col_name.cursor.fetchall()
    date_and_country_name = col_query[:2]
    remaining_columns = col_query[2:]
    country_list = []
    for i in remaining_columns:
        country_list.append(i[3])
    new_column_list = [date_and_country_name[0][3], date_and_country_name[1][3]] + country_list

    table_query = conn.execute('''SELECT * FROM "{}" WHERE "Date" = '{}';'''.format(ABRV_table_name, todays_date))
    query_list = table_query.cursor.fetchall()
    new_query_list = list(query_list[0])

    bosnia = new_column_list[-2] #23
    stkitts = new_column_list[-1] #148
    new_new_column_list = new_column_list[:23] + [bosnia] + new_column_list[23:147] + [stkitts] + new_column_list[147:-2]

    country_data_dictionary_in_json = {}
    for i in range(len(new_new_column_list)):
        country_data_dictionary_in_json[new_new_column_list[i]] = new_query_list[i]
    list_return.append(country_data_dictionary_in_json)

    return JsonResponse(list_return, safe=False)

def get_Country_headline_data(request):
    #r'^api/ByCountry/\w{2,40}'
    #connect to database
    conn = engine.connect()
    #preform query and return json data

    #Eliminate WSGI Get notation
    ABRV_Country_name = str(request)[24:]
    ABRV_Country_name = ABRV_Country_name[:-2]
    ABRV_Country_name = ABRV_Country_name[10:]
    ABRV_Country_name != 'favicon.ico'
    ABRV_Country_name != '/favicon.ico'

    ABRV_Country_name = ABRV_Country_name.replace('%20', ' ')

    QP_Score_query = conn.execute('''SELECT "{}" FROM "QP_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    QPSResult = QP_Score_query.cursor.fetchall()
    Population_query = conn.execute('''SELECT "Population in Millions" FROM "Country_Profile" WHERE "Country_Name" = '{}';'''.format(ABRV_Country_name))
    PQResult = Population_query.cursor.fetchall()
    GDP_query = conn.execute('''SELECT "GDP in Billions at PPP" FROM "Country_Profile" WHERE "Country_Name" = '{}';'''.format(ABRV_Country_name))
    GDPResult = GDP_query.cursor.fetchall()
    PerCapita_query = conn.execute('''SELECT "GDP per Capita in PPP" FROM "Country_Profile" WHERE "Country_Name" = '{}';'''.format(ABRV_Country_name))
    PerCapitaResult = PerCapita_query.cursor.fetchall()
    HDI_query = conn.execute('''SELECT "HDI" FROM "Country_Profile" WHERE "Country_Name" = '{}';'''.format(ABRV_Country_name))
    HDIResult = HDI_query.cursor.fetchall()
    size_query = conn.execute('''SELECT "Geographic Area including water" FROM "Country_Profile" WHERE "Country_Name" = '{}';'''.format(ABRV_Country_name))
    SizeResult = size_query.cursor.fetchall()
    Presidential_SCORE2 = conn.execute('''SELECT "{}" FROM "Presidential_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    Presidential_SCORE2Result = Presidential_SCORE2.cursor.fetchall()
    Prestige_SCORE2 = conn.execute('''SELECT "{}" FROM "Prestige_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    Prestige_SCORE2Result = Prestige_SCORE2.cursor.fetchall()
    GP_SCORE2 = conn.execute('''SELECT "{}" FROM "GP_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    GP_SCORE2Result = GP_SCORE2.cursor.fetchall()
    CD_SCORE2 = conn.execute('''SELECT "{}" FROM "CD_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    CD_SCORE2Result = CD_SCORE2.cursor.fetchall()
    Security_SCORE2 = conn.execute('''SELECT "{}" FROM "Security_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    Security_SCORE2Result = Security_SCORE2.cursor.fetchall()
    Sec_State_SCORE2 = conn.execute('''SELECT "{}" FROM "Sec_State_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    Sec_State_SCORE2Result = Sec_State_SCORE2.cursor.fetchall()
    CProfile_SCORE2 = conn.execute('''SELECT "{}" FROM "CProfile_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    CProfile_SCORE2Result = CProfile_SCORE2.cursor.fetchall()
    BR_SCORE2 = conn.execute('''SELECT "{}" FROM "BR_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    BR_SCORE2Result = BR_SCORE2.cursor.fetchall()
    Trade_SCORE2 = conn.execute('''SELECT "{}" FROM "Trade_SCORE2" WHERE "Date" = '{}';'''.format(ABRV_Country_name, todays_date))
    Trade_SCORE2Result = Trade_SCORE2.cursor.fetchall()


    Country_Name = ABRV_Country_name
    all_the_data = [{"Country Name":ABRV_Country_name}, {"QP_Score":QPSResult[0][0]}, {"Population in Millions":PQResult[0][0]}, {"GDP":GDPResult[0][0]}, {"GDP per Capita":PerCapitaResult[0][0]}, {"HDI":HDIResult[0][0]}, {"Size":SizeResult[0][0]}, \
    {"Presidential_SCORE2": Presidential_SCORE2Result[0][0]}, {"Prestige_SCORE2":Prestige_SCORE2Result[0][0]}, {"GP_SCORE2Result":GP_SCORE2Result[0][0]}, {"CD_SCORE2":CD_SCORE2Result[0][0]}, {"Security_SCORE2":Security_SCORE2Result[0][0]}, \
    {"Sec_State_SCORE2":Sec_State_SCORE2Result[0][0]}, {"CProfile_SCORE2":CProfile_SCORE2Result[0][0]}, {"BR_SCORE2":BR_SCORE2Result[0][0]}, {"Trade_SCORE2":Trade_SCORE2Result[0][0]}]
    return JsonResponse(all_the_data, safe=False)
