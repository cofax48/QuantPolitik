# -*- coding: utf-8 -*-
#! List of Leaders from country and title by specific year
import re
import json
import requests

def leader_name_list_getter():
    filename = 'countries_additional.json'
    with open(filename) as f:
        pop_data = json.load(f)
    country_name_list = ['G-20', 'ASEAN', 'APEC', 'G-8', 'NATO', 'Gulf Cooperation Council', 'GCC', 'G-7', 'Summit of the Americas', 'East Asia Summit', 'Strategic and Economic Dialogue',]
    for pop_dict in pop_data:
        country_name = pop_dict["name"]
        country_name_list.append(country_name)

    url_list = []
    res = requests.get('https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government')
    res.raise_for_status()
    for chunk in res.iter_content(100000):
        url_list.append(chunk)

    searcher = re.compile(r'<tr>.*?</tr>', re.DOTALL)
    readable_search = searcher.findall(str(url_list))

    country_and_list_thats_useable = []
    country_and_leader_info = {}
    relevent_snippet = re.compile(r'</span>.*?</tr>', re.DOTALL)
    country_name_getter = re.compile(r'">.*?</a>')
    for snippet in readable_search:
        yao = relevent_snippet.findall(snippet)
        country_list = ['']

        for deeper_search in yao:

            country_snippet = country_name_getter.findall(deeper_search)
            relvent_info = []
            for unicode_country in country_snippet:
                for unicode_territory in country_name_list:
                    country = unicode_country.encode('ascii', 'ignore')
                    territory = unicode_territory.encode('ascii', 'ignore')
                    country = country.decode('utf-8')
                    territory = territory.decode('utf-8')

                    if str(territory) in str(country):
                        if territory not in country_list:
                            country_list.append(territory)
                            country_and_list_thats_useable.append(territory)

                    if str(territory) not in str(country):
                        if country not in relvent_info:
                            relvent_info.append(country)

            last_country = country_list[-1]
            country_and_leader_info[last_country] = relvent_info


    not_country_name_list = ['G-20', 'ASEAN', 'APEC', 'G-8', 'NATO', 'Gulf Cooperation Council', 'GCC', 'G-7', 'Summit of the Americas', 'East Asia Summit', 'Strategic and Economic Dialogue']

    new_country_leader_list = {}
    newest_country_and_list_thats_useable = []
    for country in country_and_list_thats_useable:
        temp_list = []
        if 'Equatorial Guinea' in str(country):
            pass
        elif 'Iraq' in str(country):
            pass
        elif 'Samoa' in str(country):
            pass
        elif 'Cook Islands' in str(country):
            pass
        elif 'Kosovo' in str(country):
            pass
        elif 'Switzerland' in str(country):
            pass
        elif 'South Sudan' in str(country):
            pass
        elif 'United States' in str(country):
            pass
        elif 'Micronesia, Federated States of' in str(country):
            pass
        else:
            yao_length = len(country_and_leader_info[country])
            for i in range(yao_length):
                whole_snippet = country_and_leader_info[country][i]
                whole_snippet = whole_snippet.replace('"', '')
                whole_snippet = whole_snippet.replace("'", '')
                whole_snippet = whole_snippet.replace('</a>', '')
                whole_snippet = whole_snippet.replace('>', '')
                if len(str(country_and_leader_info[country][i])) > 40:
                    whole_snippet = country_and_leader_info[country][i]
                    extracted_title = re.sub('^(.*)(?=President)',"", whole_snippet)
                    extracted_title = str(extracted_title).replace('</a>', '')
                    temp_list.append(str(extracted_title))
                if len(str(country_and_leader_info[country][i])) < 40:
                    temp_list.append(str(whole_snippet))

                if i == int(yao_length - 1):
                    yao = temp_list[0]
                    newest_country_and_list_thats_useable.append(str(yao))
                    new_country_leader_list[yao] = temp_list

    for name, countries in new_country_leader_list.items():
        if name == 'Brunei':
            countries[1] = 'Sultan'
        elif name == 'North Korea':
            countries[1] = 'Supreme Leader'
            countries[2] = 'Kim Jong-Un'
        elif name == 'Belize':
            countries[3] = ''
            countries[4] = ''
        elif name == 'Antigua and Barbuda':
            countries[3] = ''
            countries[4] = ''
        elif name == 'North Korea':
            countries[2] = 'Kim Jong-un'
        elif name == 'Australia':
            countries[3] = ''
            countries[4] = ''
            countries[5] = ''
        elif name == 'United Kingdom':
            countries[3] = ''
            countries[4] = 'Prime Minister'
        elif name == 'Bahamas':
            countries[3] = ''
            countries[4] = ''
        elif name == 'Barbados':
            countries[3] = ''
            countries[4] = ''
        elif name == 'Bosnia and Herzegovina':
            countries[1] = 'High Representative'
        elif name == 'Canada':
            countries[1] = ''
            countries[2] = ''
        elif name == 'Switzerland':
            countries[1] = 'President'
            countries[2] = 'Doris Leuthard'
        elif name == 'Saudi Arabia':
            countries[1] = ''
            countries[2] = 'King'
        elif name == 'Iran':
            countries[1] = 'Supreme Leader'
        elif name == 'Oman':
            countries[1] = 'Sultan'
        elif name == 'San Marino':
            countries[1] = 'Captain Regent'

    return {'newest_country_and_list_thats_useable': newest_country_and_list_thats_useable, 'new_country_leader_list':new_country_leader_list}

leader_name_list_getter()['newest_country_and_list_thats_useable']
