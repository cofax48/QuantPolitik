from sqlalchemy import create_engine
import time
from datetime import datetime
import json
engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')
conn = engine.connect()

#This command creates a new table with the country_name column as the primary key
#conn.execute('''CREATE TABLE "QuantPolitik_Score" ("Country_Name" varchar(50) NOT NULL, PRIMARY KEY ("Country_Name"));''')

#This command drops a table
#conn.execute('''DROP TABLE "QuantPolitik_Score";''')

#This command creates a new column
#conn.execute('''ALTER TABLE "QuantPolitik_Score" ADD COLUMN "Afghanistan" VARCHAR(50);''')

#This command adds a row to a table
#conn.execute('''INSERT INTO "Scored_QP_NEW" VALUES ('place_holder for afghanistan');''')

#This comand drops a column from a table
#conn.execute('''ALTER TABLE "Scored_QP_NEW" DROP COLUMN "Afghanistan";''')

#This command changes the value of a cell
#conn.execute('''UPDATE "Scored_QP_NEW" SET "Country_Name" = 'Afghanistan' WHERE "Country_Name" = 'place_holder for afghanistan';''')

#This deletes all data from the table
#conn.execute('''DELETE FROM "{}";'''.format(t))

#This command creates a new column
#conn.execute('''ALTER TABLE "Scored_QP_NEW" ADD COLUMN "Afghanistan" VARCHAR(50);''')

#This counts the number of columns
#conn.execute('''SELECT COUNT(*) from information_schema.columns WHERE table_name='TABLE_NAME';''')

#This Renames a Column_Name
#conn.execute('''ALTER TABLE "{}" RENAME "Bosnia and Herzgrovina" TO "Bosnia and Herzegovina";'''.format(TABLE_NAME))

#This deletes a specific row
#conn.execute('''DELETE FROM "{}" WHERE "Date" = 'July-18-2017';'''.format(TABLE_NAME))

#conn.execute('''UPDATE "Scored_QP_NEW" SET "Row_Name" = '7-7-17' WHERE "Country_Name" = 'Afghanistan';''')
#conn.execute('''UPDATE "Scored_QP_NEW" SET "Column_Name" = 'Value to Enter' WHERE "Column_Name" = 'Existing value';''')
#conn.execute('''UPDATE "Scored_QP_NEW" SET "Row_Name" = '7-7-17' WHERE "Country_Name" = 'Afghanistan';''')
#conn.execute('''UPDATE "Scored_QP_NEW" SET "{}" = "{}"::bigint + {} WHERE "Country_Name" = '{}';'''.format(todays_date, todays_date, float(QP_value[table_name][count_num]), country))




#TABLE_NAME = 'BusinessRelationsOverallScore'
#Creates New Table
#1. conn.execute('''CREATE TABLE "{}" ("Date" varchar(50) NOT NULL, PRIMARY KEY ("Date"));'''.format(TABLE_NAME))
#2 conn.execute('''ALTER TABLE "{}" ADD COLUMN "Date" VARCHAR(50);'''.format(TABLE_NAME))
#3 conn.execute('''ALTER TABLE "{}" ADD COLUMN "Country_Name" VARCHAR(50);'''.format(TABLE_NAME))
#Adds country_name Column because thats how everything is sorted

#This makes a new row with default values IF DATE IS FIRST COLUMN, I CAN ITINIALIZE THROUGH DATE
#conn.execute('''INSERT INTO "{]" VALUES ('July-17-2017');'''.format(TABLE_NAME))

#conn.execute('''UPDATE "{}" SET "Country_Name" = 'July-18-17' WHERE "Date" = 'July-18-17';'''.format(TABLE_NAME))

#5. conn.execute('''INSERT INTO "{}" VALUES ('July-18-17');'''.format(TABLE_NAME))
Country = 'Algeria'
Data = 123
#conn.execute('''UPDATE "{}" SET "{}" = '{}' WHERE "Date" = '{}';'''.format(TABLE_NAME, Country, Data, 'July-18-17'))
#conn.execute('''INSERT INTO "{}" VALUES ('{}');'''.format(TABLE_NAME, DATE))


#This makes a new row with default values IF DATE IS FIRST COLUMN, I CAN ITINIALIZE THROUGH DATE
#conn.execute('''INSERT INTO "Scored_QP_NEW" VALUES ('July-17-2017');''')
#This enables me to update

#conn.execute('''UPDATE "Scored_QP_NEW" SET "Afghanistan" = 'Succes' WHERE "Country_Name" = 'July-17-2017';''')

#conn.execute('''ALTER TABLE "Scored_QP_NEW" ADD COLUMN "Albania" VARCHAR(50);''')

#conn.execute('''ALTER TABLE "Scored_QP_NEW" ADD COLUMN "Row_Name" VARCHAR(50);''')

#conn.execute('''ALTER TABLE "{}" RENAME "Bosnia and Herzegovina" TO "Bosnia and Herzegovina";'''.format(TABLE_NAME))

#conn.execute('''DELETE FROM "{}" WHERE "Date" = 'July-18-2017';'''.format('QP_SCORE2'))

ABRV_table_name = 'QP_SCORE2'
todays_date = datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y')

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
print(new_query_list)
print(new_column_list)
bosnia = new_column_list[-2] #23
stkitts = new_column_list[-1] #148
new_new_column_list = new_column_list[:23] + [bosnia] + new_column_list[23:147] + [stkitts] + new_column_list[147:-2]
print(new_new_column_list)

country_data_dictionary_in_json = {}
for i in range(len(new_new_column_list)):
    country_data_dictionary_in_json[new_new_column_list[i]] = new_query_list[i]
print(country_data_dictionary_in_json)

def function_stuff():
    conn.execute('''ALTER TABLE "{}" RENAME "Bosnia and Herzgrovina" TO "Bosnia and Herzegovina";'''.format('QP_SCORE2'))
    conn.execute('''ALTER TABLE "{}" RENAME "Saint Kitss and Nevis" TO "Saint Kitts and Nevis";'''.format('QP_SCORE2'))
    truncate_table = ['QP_SCORE2', 'Sec_State_SCORE2', 'Presidential_SCORE2', 'BR_SCORE2', 'Trade_SCORE2', 'GP_SCORE2', 'Prestige_SCORE2', 'Security_SCORE2', 'CD_SCORE2', 'CProfile_SCORE2']
    #truncate_table = ['QP_SCORE2']
    for TABLE_NAME in truncate_table:
        print(TABLE_NAME)
        conn.execute('''DELETE FROM "{}" WHERE "Date" = 'July-19-2017';'''.format(TABLE_NAME))
        """
        conn.execute('''CREATE TABLE "{}" ("Date" varchar(50) NOT NULL, PRIMARY KEY ("Date"));'''.format(TABLE_NAME))
        conn.execute('''ALTER TABLE "{}" ADD COLUMN "Country_Name" VARCHAR(50);'''.format(TABLE_NAME))
        conn.execute('''INSERT INTO "{}" VALUES ('{}');'''.format(TABLE_NAME, DATE))
        print(TABLE_NAME)


        for country in country_names:
            conn.execute('''ALTER TABLE "{}" ADD COLUMN "{}" VARCHAR(50);'''.format(TABLE_NAME, country["Country_Name"]))
            #counter += 1
            #conn.execute('''INSERT INTO "QuantPolitik_Score" VALUES ({});'''.format(counter))
            print(country["Country_Name"])
        """
"""
truncate_table = ['Sec_State_SCORE2', 'Presidential_SCORE2', 'BR_SCORE2', 'Trade_SCORE2', 'GP_SCORE2', 'Prestige_SCORE2', 'Security_SCORE2', 'CD_SCORE2', 'CProfile_SCORE2']
for TABLE_NAME in truncate_table:
    print(TABLE_NAME)
    conn.execute('''CREATE TABLE "{}" ("Date" varchar(50) NOT NULL, PRIMARY KEY ("Date"));'''.format(TABLE_NAME))
    conn.execute('''ALTER TABLE "{}" ADD COLUMN "Country_Name" VARCHAR(50);'''.format(TABLE_NAME))
    conn.execute('''INSERT INTO "{}" VALUES ('{}');'''.format(TABLE_NAME, DATE))
"""
"""
col_query = conn.execute('''SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}';'''.format('Business_Relations'))
col_names = []
[col_names.append(q[3]) for q in col_query]
query = conn.execute('SELECT * FROM "{}" ORDER BY "Country_Name";'.format('Business_Relations'))
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
for i in country_and_data_dict:
    print('{"Country_Name": "' + str(i["Country_Name"]) + '", "id": "'+str(i["Iso3"])+'"},')
"""
