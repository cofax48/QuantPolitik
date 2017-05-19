
"""
from pytz import utc, timezone
import time
from datetime import datetime
import os, sys, inspect

pres_path = os.path.abspath("hello/Schedule_Scraping/Presidential_2017_Bureaucratic_Exchange")
print(pres_path)
from hello.Schedule_Scraping.Presidential_2017_Bureaucratic_Exchange import main as PresMain
PresMain()



fmt = '%Y-%m-%d %H:%M:%S %Z%z'
utc_dt = utc.localize(datetime.utcfromtimestamp(time.time()))
print(utc_dt.strftime(fmt))
nyc_tz = timezone('US/Eastern')
nyc_dt = utc_dt.astimezone(nyc_tz)
print(nyc_dt)
print(str(datetime.tzinfo))


"""
from sqlalchemy import create_engine
import json
#from django.http import HttpResponse, JsonResponse
#from api.country_to_number import iso_numberifier
engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')
conn = engine.connect()

country = 'Israel'
conn.execute('''UPDATE "Presidential_Exchange" SET "Pres_2017" = 2 WHERE "Country_Name" = '{}';'''.format(country))

"""
conn.execute('''INSERT INTO "CProfile_SCORE" ("Country_Name") VALUES ('Afghanistan');''')

ABRV_table_name = 'Sec_State_Bureaucratic_Exchange'
conn = engine.connect()
todays_date = "April-10-2017"
ABRV_Country_name = "Afghanistan"
#conn.execute('''UPDATE "Security" SET "US Military Bases Abroad" = 8  WHERE "Country_Name" = 'Italy';''')
QP_Score_query = conn.execute('''SELECT "{}" FROM "QP_Score" WHERE "Country_Name" = '{}';'''.format(todays_date, ABRV_Country_name))
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

Country_Name = ABRV_Country_name
all_the_data = [{"Country Name":ABRV_Country_name}, {"QP_Score":QPSResult[0][0]}, {"Population in Millions":PQResult[0][0]}, {"GDP":GDPResult[0][0]}, {"GDP per Capita":PerCapitaResult[0][0]}, {"HDI":HDIResult[0][0]}, {"Size":SizeResult[0][0]}]
print(all_the_data)
print(JsonResponse(all_the_data, safe=False))

from datetime import datetime
import time



score_to_subtract_dict = {'Syria': 49.95}
country = 'Yemen'
print(score_to_subtract_dict.get(country))
print(score_to_subtract_dict.get('Syria'))
if score_to_subtract_dict.get(country) != None:

#Current_Military_Engagement AKA ARE WE BOMBING YOU AND IF SO, HOW LONG AGO?
query = conn.execute('''SELECT "Current_Military_Engagement" FROM "Security" ORDER BY "Country_Name";''')
query_list = query.cursor.fetchall()
country_name_query = conn.execute('''SELECT "Country_Name" FROM "Security" ORDER BY "Country_Name";''')
cnl = country_name_query.cursor.fetchall()
date_format = '%B-%d-%Y'
todays_date = datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y')
score_to_subtract_dict = {}
for index, value in enumerate(query_list):
    if len(value[0]) > 2:
        a = datetime.strptime(value[0], date_format)
        b = datetime.strptime(todays_date, date_format)
        delta = b - a
        days_til_penalty_removed = 1000 - int(delta.days)
        days_til_penalty_removed_as_percentage = days_til_penalty_removed / 1000
        score_to_subtract = days_til_penalty_removed_as_percentage * 50
        score_to_subtract_dict[cnl[index][0]] = score_to_subtract

if 'Syria' in score_to_subtract_dict:
    print('yao')
    print(score_to_subtract_dict['Syria'])
    print()
print(score_to_subtract_dict)
#conn.execute('''ALTER TABLE "Security" ADD COLUMN "Current_Military_Engagement" VARCHAR;''')
#conn.execute('''UPDATE "Security" SET "Current_Military_Engagement" = 0;''')
#conn.execute('''UPDATE "Security" SET "Current_Military_Engagement" = 'April-06-2017'  WHERE "Country_Name" = 'Syria';''')

#conn.execute('''UPDATE "QP_Score" SET "March-31-2017" = 0;''')
#conn.execute('''ALTER TABLE "QP_Score" DROP "April-07-2017";''')
#conn.execute('''ALTER TABLE "QP_Score" DROP COLUMN IF EXISTS "April-07-2017";''')

list_return = []
col_query = conn.execute('''SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}';'''.format(ABRV_table_name))
col_names = []
[col_names.append(q[3]) for q in col_query]
query = conn.execute('SELECT * FROM "{}" ORDER BY "Country_Name";'.format(ABRV_table_name))
query_list = query.cursor.fetchall()

iso3_codes = conn.execute('''SELECT "Iso3" FROM "QP_Score" ORDER BY "Country_Name";''')
iso3_codes_list = iso3_codes.cursor.fetchall()

for i in iso3_codes_list:
    print(i)

country_and_data_dict = []
for i in range(len(query_list)):
    print(i)
    country = query_list[i][0]
    temp_list = {}
    for c in range(len(col_names)):
        temp_list[col_names[c]] = query_list[i][c]
    temp_list["Iso3"] = iso3_codes_list[i][0]
    print(temp_list)
    country_and_data_dict.append(temp_list)


list_return.append(country_and_data_dict)

codex = {
    "Kosovo":"-099",
    "Afghanistan":"004",
    "Albania":"008",
    "Antarctica":"010",
    "Algeria":"012",
    "American Samoa":"016",
    "Andorra":"020",
    "Angola":"024",
    "Antigua and Barbuda":"028",
    "Azerbaijan":"031",
    "Argentina":"032",
    "Australia":"036",
    "Austria":"040",
    "Bahamas, The":"044",
    "Bahrain":"048",
    "Bangladesh":"050",
    "Armenia":"051",
    "Barbados":"052",
    "Belgium":"056",
    "Bermuda":"060",
    "Bhutan":"064",
    "Bolivia":"068",
    "Bosnia and Herzegovina":"070",
    "Botswana":"072",
    "Bouvet Island":"074",
    "Brazil":"076",
    "Belize":"084",
    "British Indian Ocean Territory":"086",
    "Solomon Islands":"090",
    "Virgin Islands":"092",
    "Brunei":"096",
    "Bulgaria":"100",
    "Myanmar":"104",
    "Burundi":"108",
    "Belarus":"112",
    "Cambodia":"116",
    "Cameroon":"120",
    "Canada":"124",
    "Cape Verde":"132",
    "Cayman Islands":"136",
    "Central African Republic":"140",
    "Sri Lanka":"144",
    "Chad":"148",
    "Chile":"152",
    "China":"156",
    "Taiwan":"158",
    "Christmas Island":"162",
    "Cocos (Keeling) Islands":"166",
    "Colombia":"170",
    "Comoros":"174",
    "Mayotte":"175",
    "Congo, Republic of the":"178",
    "Democratic Republic of the Congo":"180",
    "Cook Islands":"184",
    "Costa Rica":"188",
    "Croatia":"191",
    "Cuba":"192",
    "Cyprus":"196",
    "Czech Republic":"203",
    "Benin":"204",
    "Denmark":"208",
    "Dominica":"212",
    "Dominican Republic":"214",
    "Ecuador":"218",
    "El Salvador":"222",
    "Equatorial Guinea":"226",
    "Ethiopia":"231",
    "Eritrea":"232",
    "Estonia":"233",
    "Faroe Islands":"234",
    "Falkland Islands (Malvinas)":"238",
    "South Georgia and the South Sandwich Islands":"239",
    "Fiji":"242",
    "Finland":"246",
    "Åland Islands":"248",
    "France":"250",
    "French Guiana":"254",
    "French Polynesia":"258",
    "French Southern Territories":"260",
    "Djibouti":"262",
    "Gabon":"266",
    "Georgia":"268",
    "Gambia, The":"270",
    "Palestine":"275",
    "Germany":"276",
    "Ghana":"288",
    "Gibraltar":"292",
    "Kiribati":"296",
    "Greece":"300",
    "Greenland":"304",
    "Grenada":"308",
    "Guadeloupe":"312",
    "Guam":"316",
    "Guatemala":"320",
    "Guinea":"324",
    "Guyana":"328",
    "Haiti":"332",
    "Heard Island and McDonald Islands":"334",
    "Vatican City":"336",
    "Honduras":"340",
    "Hong Kong":"344",
    "Hungary":"348",
    "Iceland":"352",
    "India":"356",
    "Indonesia":"360",
    "Iran":"364",
    "Iraq":"368",
    "Ireland":"372",
    "Israel":"376",
    "Italy":"380",
    "Côte d'Ivoire":"384",
    "Ivory Coast":"384",
    "Jamaica":"388",
    "Japan":"392",
    "Kazakhstan":"398",
    "Jordan":"400",
    "Kenya":"404",
    "North Korea":"408",
    "South Korea":"410",
    "Kuwait":"414",
    "Kyrgyzstan":"417",
    "Laos":"418",
    "Lebanon":"422",
    "Lesotho":"426",
    "Latvia":"428",
    "Liberia":"430",
    "Libya":"434",
    "Liechtenstein":"438",
    "Lithuania":"440",
    "Luxembourg":"442",
    "Madagascar":"450",
    "Malawi":"454",
    "Malaysia":"458",
    "Maldives":"462",
    "Mali":"466",
    "Malta":"470",
    "Martinique":"474",
    "Mauritania":"478",
    "Mauritius":"480",
    "Mexico":"484",
    "Monaco":"492",
    "Mongolia":"496",
    "Moldova":"498",
    "Montenegro":"499",
    "Montserrat":"500",
    "Morocco":"504",
    "Mozambique":"508",
    "Oman":"512",
    "Namibia":"516",
    "Nauru":"520",
    "Nepal":"524",
    "Netherlands":"528",
    "Curaçao":"531",
    "Aruba":"533",
    "Sint Maarten (Dutch part)":"534",
    "Bonaire":"535",
    "New Caledonia":"540",
    "Vanuatu":"548",
    "New Zealand":"554",
    "Nicaragua":"558",
    "Niger":"562",
    "Nigeria":"566",
    "Niue":"570",
    "Norway":"578",
    "Northern Mariana Islands":"580",
    "United States Minor Outlying Islands":"581",
    "Micronesia":"583",
    "Marshall Islands":"584",
    "Palau":"585",
    "Pakistan":"586",
    "Panama":"591",
    "Papua New Guinea":"598",
    "Paraguay":"600",
    "Peru":"604",
    "Philippines":"608",
    "Pitcairn":"612",
    "Poland":"616",
    "Portugal":"620",
    "Guinea-Bissau":"624",
    "East Timor":"626",
    "Puerto Rico":"630",
    "Qatar":"634",
    "Réunion":"638",
    "Romania":"642",
    "Russia":"643",
    "Rwanda":"646",
    "Saint Barthélemy":"652",
    "Saint Helena":"654",
    "Saint Kitts and Nevis":"659",
    "Anguilla":"660",
    "Saint Lucia":"662",
    "Saint Martin (French part)":"663",
    "Saint Pierre and Miquelon":"666",
    "Saint Vincent and the Grenadines":"670",
    "San Marino":"674",
    "São Tomé and Príncipal":"678",
    "Saudi Arabia":"682",
    "Senegal":"686",
    "Serbia":"688",
    "Seychelles":"690",
    "Sierra Leone":"694",
    "Singapore":"702",
    "Slovakia":"703",
    "Vietnam":"704",
    "Slovenia":"705",
    "Somalia":"706",
    "South Africa":"710",
    "Zimbabwe":"716",
    "Spain":"724",
    "South Sudan":"728",
    "Sudan":"729",
    "Western Sahara":"732",
    "Suriname":"740",
    "Svalbard and Jan Mayen":"744",
    "Swaziland":"748",
    "Sweden":"752",
    "Switzerland":"756",
    "Syria":"760",
    "Tajikistan":"762",
    "Thailand":"764",
    "Togo":"768",
    "Tokelau":"772",
    "Tonga":"776",
    "Trinidad and Tobago":"780",
    "United Arab Emirates":"784",
    "Tunisia":"788",
    "Turkey":"792",
    "Turkmenistan":"795",
    "Turks and Caicos Islands":"796",
    "Tuvalu":"798",
    "Uganda":"800",
    "Ukraine":"804",
    "Macedonia":"807",
    "Egypt":"818",
    "United Kingdom":"826",
    "Guernsey":"831",
    "Jersey":"832",
    "Isle of Man":"833",
    "Tanzania":"834",
    "United States":"840",
    "Virgin Islands":"850",
    "Burkina Faso":"854",
    "Uruguay":"858",
    "Uzbekistan":"860",
    "Venezuela":"862",
    "Wallis and Futuna":"876",
    "Samoa":"882",
    "Yemen":"887",
    "Zambia":"894"
}

table_list = ['Business_Relations', 'Trade_Relations', 'Governmental_Perspective', 'Country_Profile', 'Security', 'UN', 'QP_Score', 'Cultural_Diffusion', 'Prestige', 'Sec_State_Bureaucratic_Exchange', 'Presidential_Exchange']
for tab in table_list:
    #conn.execute('''UPDATE "{}" SET "Country_Name" = 'Bosnia and Herzegovina' WHERE "Country_Name" = 'Bosnia and Herzgrovina';'''.format(tab))
    conn.execute('''UPDATE "{}" SET "Country_Name" = 'Saint Kitts and Nevis' WHERE "Country_Name" = 'Saint Kitss and Nevis';'''.format(tab))


query = conn.execute('SELECT "Country_Name" FROM "{}" ORDER BY "Country_Name";'.format('QP_Score'))
query_list = query.cursor.fetchall()
#conn.execute('''ALTER TABLE "QP_Score" ADD COLUMN "Iso3" VARCHAR;''')
conn.execute('''UPDATE "QP_Score" SET "Iso3" = 0;''')
for q in query_list:
    conn.execute('''UPDATE "QP_Score" SET "Iso3" = "Iso3"::int + {} WHERE "Country_Name" = '{}';'''.format(codex[q[0]], q[0]))
    print(q[0], codex[q[0]])




#connect to database
conn = engine.connect()
#preform query and return json data
ABRV_table_and_column = 'Sec_State_Bureaucratic_Exchange/Sec_of_State_2017'

#Eliminate WSGI Get notation
ABRV_table_name = str(request)[24:]
ABRV_table_name = ABRV_table_name[:-2]
ABRV_table_name != 'favicon.ico'
ABRV_table_name != '/favicon.ico'

table_name, column_name = ABRV_table_and_column.split("/")
ABRV_table_name = table_name

print(table_name, column_name)

query = conn.execute('SELECT "Sec_of_State_2017" FROM "{}";'.format(table_name))
query_list = query.cursor.fetchall()


country_names = conn.execute('SELECT "Country_Name" FROM "{}";'.format(table_name))
country_list = country_names.cursor.fetchall()

country_and_data_list = []
for i in range(len(query_list)):
    country_and_data_dict = {}
    country_and_data_dict['Country_Name']  = country_list[i][0]
    country_and_data_dict[column_name] = query_list[i][0]
    country_and_data_list.append(country_and_data_dict)

print(country_and_data_list)






filename = 'countries_additional.json'
with open(filename) as f:
    pop_data = json.load(f)

country_name_list = []
for pop_dict in pop_data:
    country_name = pop_dict["name"]
    country_name_list.append(country_name)
country_dem_list = []
filename = 'indepth_country_list.json'
with open(filename) as f:
    pop_data = json.load(f)
for pop_dict in pop_data:
    country_demonym = pop_dict["name"]["common"], pop_dict["demonym"]
    country_name_list.append(country_demonym[1])
    country_dem_list.append(country_demonym)


table_name ='Sec_State_Bureaucratic_Exchange'
column_name = '*'
engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')
conn = engine.connect()

conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 1 WHERE "Country_Name" = 'Ukraine';''')

for c in country_name_list:
    if c == "Cote d'Ivoire":
        pass
    elif c == "Cote d'Ivoire":
        pass
    else:
        conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = 10 WHERE "Country_Name" = '{}';'''.format(str(c)))

#conn.execute('''ALTER TABLE "Sec_State_Bureaucratic_Exchange" DROP COLUMN "None";''')

#conn.execute('''ALTER TABLE "Sec_State_Bureaucratic_Exchange" ADD COLUMN "Sec_of_State_2017" VARCHAR;''')
#

conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = 10;''')

query = conn.execute('SELECT {} FROM "{}";'.format(column_name, table_name))
query_list = query.cursor.fetchall()
col_query = conn.execute('''SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}';'''.format(table_name))
col_names = []
[col_names.append(q[3]) for q in col_query]

print(query_list)
print(col_names)



conn.execute('''ALTER TABLE "Sec_State_Bureaucratic_Exchange" ADD COLUMN "Sec_of_State_2017" VARCHAR;''')
conn.execute('''ALTER TABLE "Presidential_Exchange" ADD COLUMN "Pres_2017" VARCHAR;''')

conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = 0;''')
conn.execute('''UPDATE "Presidential_Exchange" SET "Pres_2017" = 0;''')
#Create New Column in Presidentil Exchange for Trump in 2017
#Create New Column in Sec_State_Bureaucratic_Exchange for Sec_of_State_2017
#Crate new table "QP_Score"
#ALTER TABLE "Presidential_Exchange" ADD COLUMN "Pres_2017" VARCHAR;

import time

import datetime
print(
    datetime.datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y')
)


import re
import json

filename = '/Users/cofax48/coding/QP_2016/countries_additional.json'
with open(filename) as f:
    pop_data = json.load(f)

country_name_list = ['G-20', 'G20', 'G8', 'G7', 'ASEAN', 'ASEAN-', 'APEC', 'G-8', 'NATO', 'CARICOM', 'Gulf Cooperation Council', 'GCC', 'G-7', 'Summit of the Americas', 'East Asia Summit', 'Strategic and Economic Dialogue']
for pop_dict in pop_data:
    country_name = pop_dict["name"]
    country_name_list.append(country_name)
country_dem_list = []
filename = '/Users/cofax48/coding/QP_2016/indepth_country_list.json'
"""
