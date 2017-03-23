# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import Numeric, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from country_to_number import country_numberifier
import json
import time

'''
NOTES!!!!
To link with primary key:
Column('Country_Name, ForeignKey('QP_Initialization.Country_Name'))
'''

#Engine Connection
engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')
connection = engine.connect()
metadata = MetaData()

conn = engine.connect()
#preform query and return json data
query = conn.execute('SELECT "Remittances" FROM "Business_Relations";')
query_list = query.cursor.fetchall()

filename = '/Users/cofax48/coding/QP_2016/countries_additional.json'
with open(filename) as f:
    pop_data = json.load(f)
country_name_list = []
for pop_dict in pop_data:
    country_name = pop_dict["name"]
    country_name_list.append(country_name)

multilater_country_list = ['G-20', 'G20', 'G8', 'G7', 'ASEAN', 'ASEAN-', 'APEC', 'Arctic Council', 'G-8', 'NATO', 'CARICOM', 'Gulf Cooperation Council', 'GCC', 'G-7', 'Summit of the Americas', 'East Asia Summit', 'Strategic and Economic Dialogue']

for country in country_name_list:
    if 'Summit' not in country:
        if country not in multilater_country_list:
            country_num = country_numberifier(country)
            print(country, query_list[country_num])

