# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from sqlalchemy import create_engine
from hello.country_to_number import country_numberifier
from hello.country_to_number import codex
from hello.country_to_number import iso_numberifier


engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def dataDashBoard(request):
    return render(request, 'dataDashBoard.html')

def originalHomePage(request):
    return render(request, 'homePage.html')

def aboutPage(request):
    return render(request, 'about.html')

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
    #connect to database
    conn = engine.connect()
    #preform query and return json data

    #Eliminate WSGI Get notation
    ABRV_table_name = str(request)[24:]
    ABRV_table_name = str(ABRV_table_name)[:-2]


    table_name, column_name = ABRV_table_name.split("/")
    column_name = column_name.replace('%20', ' ')

    query = conn.execute('SELECT "{}" FROM "{}" ORDER BY "Country_Name";'.format(column_name, table_name))
    query_list = query.cursor.fetchall()


    country_names = conn.execute('SELECT "Country_Name" FROM "{}"; ORDER BY "Country_Name"'.format(table_name))
    country_list = country_names.cursor.fetchall()

    iso3_codes = conn.execute('SELECT "Iso3" FROM "QP_Score" ORDER BY "Country_Name";')
    iso3_codes_list = iso3_codes.cursor.fetchall()

    country_and_data_list = []
    for i in range(len(query_list)):
        country_and_data_dict = {}
        country_and_data_dict['Country_Name']  = country_list[i][0]
        country_and_data_dict['Iso3'] = iso3_codes_list[i][0]
        country_and_data_dict[column_name] = query_list[i][0]
        country_and_data_list.append(country_and_data_dict)

    json_list_to_send = []
    json_list_to_send.append(country_and_data_list)


    return JsonResponse(country_and_data_list, safe=False)
