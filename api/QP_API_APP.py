from flask import Flask, request, Response, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from country_to_number import country_numberifier
from country_to_number import codex
from country_to_number import Business_Relations_Table_Name
from country_to_number import iso_numberifier

engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')

app = Flask(__name__)
api = Api(app)


class VAR3DataBaseQuery(Resource):
    def get(self, table_name, column_name, country):
        #connect to database
        #connect to database
        conn = engine.connect()
        #preform query and return json data
        country_num = country_numberifier(country)
        query = conn.execute('SELECT "{}" FROM "{}";'.format(column_name, table_name))
        query_list = query.cursor.fetchall()
        country_num = country_numberifier(country)
        whole_api_for_country = {column_name: {country: query_list[country_num][0]}}
        return whole_api_for_country

class VAR2DataBaseQuery(Resource):
    def get(self, table_name, column_name):
        #http://localhost:8000/api/Business_Relations?column_name=Remittances
        #connect to database
        conn = engine.connect()
        #preform query and return json data
        query = conn.execute('SELECT "{}" FROM "{}";'.format(column_name, table_name))
        query_list = query.cursor.fetchall()

        #Gets Country Names
        country_name_list = sorted([key for key, value in codex.items()])

        country_value_api_to_send = []
        #Combines The Column info, country_name info
        for country in country_name_list:
            country_num = country_numberifier(country)
            country_and_value = {"Country_Name": country, column_name: query_list[country_num][0]}
            country_value_api_to_send.append(country_and_value)

        return country_value_api_to_send

class VAR1DataBaseQuery(Resource):
    def get(self, table_name):
        #connect to database
        conn = engine.connect()
        #preform query and return json data
        query = conn.execute('SELECT * FROM "{}";'.format(table_name))
        query_list = query.cursor.fetchall()

        #Gets Country Names
        country_name_list = sorted([key for key, value in codex.items()])
        #Gets Column Names
        col_query = conn.execute('''SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}';'''.format(table_name))
        col_names = []
        [col_names.append(q[3]) for q in col_query]

        country_value_dict = []
        #Combines The Column info, country_name info
        for country in country_name_list:
            country_num = country_numberifier(country)
            iso_num = iso_numberifier(country)
            country_dict = {"Iso3":int(iso_num)}
            for i in range(0, int(len(col_names)) - 1):
                key = col_names[i]
                value = query_list[country_num][i]
                country_dict[key] = value
            country_value_dict.append(country_dict)

        country_value_dict = sorted(country_value_dict, key=lambda k: k['Country_Name'])

        return country_value_dict

api.add_resource(VAR3DataBaseQuery, '/<string:table_name>/<string:column_name>/<string:country>')
api.add_resource(VAR2DataBaseQuery, '/<string:table_name>/<string:column_name>')
api.add_resource(VAR1DataBaseQuery, '/<string:table_name>')

if __name__=='__main__':
    app.run()
