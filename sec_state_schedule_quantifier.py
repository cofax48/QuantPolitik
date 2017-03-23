# -*- coding: utf-8 -*-
import datetime, time
time1 = time.time()
import re
import requests
import json
from leader_list_getter_2016 import leader_name_list_getter
from Foreign_minister_getter_2016 import foreign_minister_list_getter
from sqlalchemy import create_engine
from unidecode import unidecode 

def daily_sched_search():
    url_list = []
    res = requests.get('https://www.state.gov/r/pa/prs/appt/2017/index.htm')
    res.raise_for_status()
    for chunk in res.iter_content(100000):
        url_list.append(chunk)

    daily_schedule_links = re.compile('<a href=".*?">Public Schedule: ', re.DOTALL)
    dsl = daily_schedule_links.findall(str(url_list))

    list_of_sched_links = []
    for links in dsl:
        list_of_sched_links.append(links)

    sec_state_schedule_urls = []
    for l in list_of_sched_links:
        if len(str(l)) < 90:
            new_L = str(l).replace('<a href="', 'https://www.state.gov')
            newest_L = str(new_L).replace('">Public Schedule: ', '')
            sec_state_schedule_urls.append(newest_L)
    sec_state_schedule = []
    for url in sec_state_schedule_urls:
        new_res = requests.get(url)

        for new_chunk in new_res.iter_content(100000):
            sec_state_schedule.append(new_chunk)

    schedule_block = re.compile('<!-- CENTERBLOCK START -->.*?<!-- CENTERBLOCK END -->', re.DOTALL)
    sb = schedule_block.findall(str(sec_state_schedule))

    each_day_schedule = []
    for eds in sb:
        each_day_schedule.append(eds)
        
    SecState_daily_meetings_list = []
    specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')

    #finds SecState's schedule within each particular day
    for i in each_day_schedule:
        sd_all_matches = specific_day.findall(i)
        sd = sd_all_matches[0]
        SecState_search = re.compile(r'((SECRETARY REX TILLERSON|SECRETARY TILLERSON)(.*?<span style=|.*?UNDER SECRETARY FOR|.*?ASSISTANT SECRETARY|.*?ACTING|.*?\*\*\*|.*?</div>))', re.DOTALL)
        SecState_daily_meeting = SecState_search.findall(i)
        for meets in SecState_daily_meeting:
            whole_meet = '\n' + str(sd) + '\n' + str(meets)
            if whole_meet not in SecState_daily_meetings_list:
                SecState_daily_meetings_list.append(whole_meet)

    print('Searching the schedule')

    return {'SecState_daily_meetings_list':SecState_daily_meetings_list}


list_setter = 'new_PRES_MEETING_LIST'
def country_name_acquistion():
    """A function that imports a list of countries and compiles it into a list"""
    filename = 'countries_additional.json'
    with open(filename) as f:
        pop_data = json.load(f)
        
    country_name_list = ['G-20', 'G20', 'G8', 'G7', 'ASEAN', 'ASEAN-', 'APEC', 'Arctic Council', 'G-8', 'NATO', 'CARICOM', 'Gulf Cooperation Council', 'GCC', 'G-7', 'Summit of the Americas', 'East Asia Summit', 'Strategic and Economic Dialogue']
    for pop_dict in pop_data:
        country_name = unidecode(pop_dict["name"])
        country_name_list.append(country_name)
    country_dem_list = []
    filename = 'indepth_country_list.json'
    with open(filename) as f:
        pop_data = json.load(f)
    for pop_dict in pop_data:
        country_demonym = unidecode(pop_dict["name"]["common"]), unidecode(pop_dict["demonym"])
        country_name_list.append(country_demonym[1])
        country_dem_list.append(country_demonym)
    return {'country_name_list':country_name_list, 'country_dem_list':country_dem_list}


def meeting_search(SecState_daily_meetings_list, country_name_list):
    """Finds out who Kerry met with and from what country"""

    specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')
    schedule_snippet = re.compile(r'\d{1,2}:\d{1,2} \w{2}.*?\n\n', re.DOTALL)
    old_bilateral_meetings_list = []

    meeting_name_list = ['met', 'mets', 'meet', 'meets', 'host', 'addresses', 'greets', 'welcomed', 'accompanies',
                         'greet', 'greeted', 'address', 'attend', 'attends', 'meeting', 'meetings', 'joins', 'has an audience with',
                         'joined', 'welcome', 'welcomes', 'welcomed', 'participates', 'deliver statements', 'delivers remarks',
                         'lunch', 'State Dinner']


    bilateral_meetings_list = []
    for a in SecState_daily_meetings_list:
        if 'Northern Ireland' in str(a):
            a = a.replace('Northern Ireland', '')
            bilateral_meetings_list.append(a)
        elif 'Port of Spain' in str(a):
            a = a.replace('Port of Spain', '')
            bilateral_meetings_list.append(a)
        elif "Cote d’Ivoire" in str(a):
            a = a.replace("Cote d’Ivoire", 'Ivory Coast')
            bilateral_meetings_list.append(a)
        elif "Côte d'Ivoire" in str(a):
            a = a.replace("Côte d'Ivoire", 'Ivory Coast')
            bilateral_meetings_list.append(a)
        elif 'Deputy Crown Prince' in str(a):
            a = a.replace("Deputy Crown Prince", 'Deputy CroPri')
            bilateral_meetings_list.append(a)
        elif 'Holy See' in str(a):
            a = a.replace('Holy See', 'Vatican City')
            bilateral_meetings_list.append(a)
        elif 'Special Envoy for ' in str(a):
            a = re.sub(r'Special Envoy for \w{0,15}', '', a, count=2)
            bilateral_meetings_list.append(a)            
        elif "Timor-Leste" in str(a):
            a = a.replace("Timor-Leste", 'East Timor')
            bilateral_meetings_list.append(a)
        elif 'Secretary of Defense Ashton Carter' in str(a):
            a = a.replace("Secretary of Defense Ashton Carter", '')
            bilateral_meetings_list.append(a)            
        elif 'Environment Minister' in str(a):
            a = a.replace('Environment Minister', 'Minister of Environment')
            bilateral_meetings_list.append(a)
        elif 'Minister of Defense' in str(a):
            a = a.replace('Minister of Defense', 'Defense Minister')
            bilateral_meetings_list.append(a)            
        elif 'Foreign Secretary' in str(a):
            a = a.replace('Foreign Secretary', 'Foreign Minister')
            bilateral_meetings_list.append(a)
        elif 'Climate Change Secretary' in str(a):
            a = a.replace('Climate Change Secretary', 'Minister of Environment')
            bilateral_meetings_list.append(a)
        elif 'working lunch' in str(a):
            a = a.replace('working lunch', 'working dinner')
            bilateral_meetings_list.append(a)            
        elif "European Commission President" in str(a):
            a = a.replace("European Commission President", '')
            bilateral_meetings_list.append(a)
        elif 'Democratic Congo, Republic of the' in str(a):
            a = a.replace("Democratic Congo, Republic of the", 'Democratic Republic of the Congo')
            bilateral_meetings_list.append(a)            
        elif "The Bahamas" in str(a):
            a = a.replace("The Bahamas", 'Bahamas, The')
            bilateral_meetings_list.append(a)
        elif 'on Syria' in str(a):
            a = a.replace("on Syria", '')
            bilateral_meetings_list.append(a)
        elif 'Chairman and General Secretary of the National League of Democracy' in str(a):
            a = a.replace("Chairman and General Secretary of the National League of Democracy", 'Opposition Leader of Myanmar')
            bilateral_meetings_list.append(a)
        elif 'The Gambia' in str(a):
            a = a.replace("The Gambia", 'Gambia, The')
            bilateral_meetings_list.append(a)
        elif 'Israeli-Palestinian Negotiations' in str(a):
            a = a.replace('Israeli-Palestinian Negotiations', '')
            bilateral_meetings_list.append(a)            
        elif 'Director for North Africa and Yemen' in str(a):
            a = a.replace('Director for North Africa and Yemen', '')
            if 'Special Envoy for Libya' in str(a):
                a = a.replace('Special Envoy for Libya', '')
                bilateral_meetings_list.append(a)
            else:
                bilateral_meetings_list.append(a)
        elif 'UN Envoy for Syria' in str(a):
            a = a.replace('UN Envoy for Syria', '')
            bilateral_meetings_list.append(a)
        elif 'Panel for Sudan and South Sudan' in str(a):
            a = a.replace('Panel for Sudan and South Sudan', '')
            if 'former President' in str(a):
                a = a.replace('former President', 'former Prez')
                bilateral_meetings_list.append(a)
            else:
                bilateral_meetings_list.append(a)
        elif "Sao Tome" in str(a):
            a = a.replace("Sao Tome and Principal", "São Tomé and Príncipal")
            bilateral_meetings_list.append(a)            
        elif 'Republic of the Congo' in str(a):
            a = a.replace('Republic of the Congo', 'Congo, Republic of the')
            bilateral_meetings_list.append(a)
        elif 'St.' in str(a):
            a = a.replace('St.', 'Saint')
            bilateral_meetings_list.append(a)
        elif 'Secretary of Defense' in str(a):
            if 'Chuck Hagel' in str(a):
                a = a.replace('Secretary of Defense Chuck Hagel', '')
                bilateral_meetings_list.append(a)
            elif 'Ash Carter' in str(a):
                a = a.replace('Secretary of Defense Ash Carter', '')
                bilateral_meetings_list.append(a)
            else:
                bilateral_meetings_list.append(a)
        elif 'Secretary of State' in str(a):
            if 'Hillary Clinton' in str(a):
                a = a.replace('Secretary of State Hillary Clinton', '')
                bilateral_meetings_list.append(a)
        elif 'will depart' in str(a):
            pass
        elif 'upcoming trip to ' in str(a):
            pass
        elif 'briefing to preview' in str(a):
            pass
        elif 'Ambassador to ' in str(a):
            a = re.sub(r'\w{0,10} Ambassador to \w{0,15}', '', a, count=20)
            bilateral_meetings_list.append(a) 
        elif 'meets with his national security team' in str(a):
            pass
        elif 'hold a meeting on ' in str(a):
            pass
        elif 'former President' in str(a):
            a = a.replace('former President', 'former Prez')
            bilateral_meetings_list.append(a)
        elif 'G8' in str(a):
            a = a.replace('G8', 'G-8')
            bilateral_meetings_list.append(a)
        elif 'G20' in str(a):
            a = a.replace('G20', 'G-20')
            bilateral_meetings_list.append(a)
        elif 'Vice Premier' in str(a):
            a = a.replace('Vice Premier', 'Vice-Premeir')
            bilateral_meetings_list.append(a)
        elif 'former Prime Minister' in str(a):
            a = a.replace('former Prime Minister', 'former PM')
            bilateral_meetings_list.append(a)
        elif 'former British Prime Minister' in str(a):
            a = a.replace('former British Prime Minister', 'former PM of the United Kingdom')
            bilateral_meetings_list.append(a)
        elif 'ASEAN-' in str(a):
            a = a.replace('-', '')
            bilateral_meetings_list.append(a)
        elif 'Burma' in str(a):
            a = a.replace('Burma', 'Myanmar')
            bilateral_meetings_list.append(a)
        elif 'will remain' in str(a):
            pass
        elif 'Secretary of Defense Leon Panetta' in str(a):
            a = a.replace('Secretary of Defense Leon Panetta', '')
            bilateral_meetings_list.append(a)            
        elif 'U.S. Secretary of Defense' in str(a):
            a = a.replace('U.S. Secretary of Defense', '')
            bilateral_meetings_list.append(a)
        elif 'Vice President Biden' in str(a):
            a = a.replace('Vice President Biden', '')
            bilateral_meetings_list.append(a)
        elif 'President Obama' in str(a):
            a = a.replace('President Obama', '')
            bilateral_meetings_list.append(a)
        elif 'ideo conference' in str(a):
            pass
        elif 'Deputy Prime Minister' in str(a):
            a = a.replace('Deputy Prime Minister', 'Deputy PM')
            bilateral_meetings_list.append(a)
        else:           
            bilateral_meetings_list.append(a)


    new_PRES_MEETING_LIST = bilateral_meetings_list
    country_meeting_list = []
        
    return {'new_PRES_MEETING_LIST':new_PRES_MEETING_LIST}

def country_and_leader_getter(new_PRES_MEETING_LIST, country_name_list, country_dem_list):
    newest_country_and_list_thats_useable = leader_name_list_getter()['newest_country_and_list_thats_useable']
    new_country_leader_list = leader_name_list_getter()['new_country_leader_list']
    foreign_minister_name_list = foreign_minister_list_getter()['newest_country_and_list_thats_useable']
    foreign_min_country = foreign_minister_list_getter()['new_country_leader_list']
    
    leader_list = ['President', 'Prime Minister', 'Prime Minster', 'King ', 'Chancellor', 'Taoiseach', 'Queen', 'Amir', 'Emperor', 'Pope', 'Sultan',
                   'CEO', 'Crown Prince', 'Defense Minister', 'Deputy Crown Prince', 'Deputy PM', 'Finance Minister', 'margins', 'leaders meeting', 'Working Session', 'Plenary Session', 'working session', 'Secretary of State',
                          'Foreign Minister', 'Foregin Minster', 'Foreign Secretary', 'Chairman and General Secretary of the National League of Democracy', 'family photo', 'Secretary of Defense',
                          'Minister of Foreign Affairs', 'Minister of External Relations', 'Opposition Leader', 'Premier', 'former Prez', 'former PM', 'Sate Dinner', 'working dinner', 'working lunch', 'Ministerial Meeting', 'closing session', 'Deputy CroPri',
                          'Defense Minister', 'Minister of Defense', 'Minister for Foreign Affairs', 'Minister of Foreign Affairs', 'Minister of Finance', 'Minister of Foreign Trade', 'Vice-Premeir', 'State Counselor', 
                          'Minister of Environment', 'Minister of Natural Resources', 'Secretary of Foreign Relations', 'State Councilor', 'Secretary of Interior', 'Secretary of Finance',
                          'Minister of Power', 'Minister of State for Foreign Affairs','Vice Prez', 'Vice Premier']
    total_meeting_list = ['place holder']

    #This tests countries by country name
    for meeting in eval(list_setter):
        for leader in leader_list:
            for country in country_name_list:
                if str(leader) in str(meeting):
                    if str(country) in str(meeting):
                        if str(country) != 'United States':
                            if str(country) != 'American':
                                new_meeting = re.sub(r', in \w{}, {}.\.'.format("{1,30}", (country), re.IGNORECASE), '', str(meeting), count=10)
                                specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')
                                sd_all_matches = specific_day.findall(new_meeting)
                                sd = sd_all_matches[0]
                                yao = sd + '\n' + country + '\t' + leader + '\n'
                                searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}(?!\.)'.format(str(leader), "{0,9}", str(country), re.IGNORECASE))
                                backwards_searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}'.format(str(country), "{0,5}", str(leader), re.IGNORECASE))
                                exact_match = searcher.findall(new_meeting)
                                other_exact_match = backwards_searcher.findall(new_meeting)
                                for matches in exact_match:
                                    if ',' not in str(matches):
                                        if 'and ' not in str(matches):
                                            if 'Obama' not in str(matches):
                                                if yao not in total_meeting_list:
                                                    if str(country) in yao:
                                                        total_meeting_list.append(yao)
                                for matches in other_exact_match:
                                    if ',' not in str(matches):
                                        if 'and ' not in str(matches):
                                            if yao not in total_meeting_list:
                                                if str(country) in yao:
                                                    total_meeting_list.append(yao)
    foreign_minister_name_list = foreign_minister_list_getter()['new_country_leader_list']
    dual_leader_list = ['Brunei', 'Fiji', 'Israel', 'Kiribati', 'Nauru', 'Oman', 'Pakistan', 'Saint Lucia', 'Samoa', 'Seychelles', 'Tonga', 'Yemen']
    for countries in foreign_minister_name_list:
        if len(foreign_min_country[countries]) < 3:
            pass
        else:
            leader_country = str(foreign_min_country[countries][0])
            leader_name = str(foreign_min_country[countries][2])
            specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')
            for meeting in eval(list_setter):
                sd_all_matches = specific_day.findall(meeting)
                sd = sd_all_matches[0]
                if str(leader_name) in str(meeting):
                    if leader_country in dual_leader_list:
                        pass
                    else:
                        yao = sd + '\n' + leader_country + '\t' + 'Foreign Minister' + '\n'
                        if yao not in total_meeting_list:
                            total_meeting_list.append(yao)

    roman_numeral_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'EFI', 'Prime Minister', 'President', 'Sultan', 'Sabah Al-Ahmad Al-Jaber Al-Sabah', 'le', 'Ao', 'Malo']
    asian_country_last_name_first_list = ['China', 'South Korea', 'Taiwan', 'Vietnam', 'North Korea', 'Singapore', 'Japan']                     

    #This tests for Leaders last names and titles
    for diff_country in newest_country_and_list_thats_useable:
        leader_name = str(new_country_leader_list[diff_country][2])
        leader_name = leader_name + ' '
        leader_country = str(new_country_leader_list[diff_country][0])
        other_leader = str(new_country_leader_list[diff_country][-1])
        other_leader = other_leader + ' '
        other_leader_title = str(new_country_leader_list[diff_country][-2])
        leader_title = str(new_country_leader_list[diff_country][1])
        specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')                   
        leader_last_name = re.sub('\w{0,10} ', '', leader_name, count=1)
        other_leader_last_name = re.sub('\w{0,10} ', '', other_leader, count=1)
        asian_leader_last_name = re.sub(' \w{0,5}-\w{0,5}| \w{0,10}', '', leader_name, count=1)
        asian_leader_last_name = asian_leader_last_name + ' '
        asian_other_leader_last_name = re.sub(' \w{0,5}-\w{0,5}| \w{0,10}', '', other_leader, count=1)
        asian_other_leader_last_name = asian_other_leader_last_name + ' '
        if len(str(other_leader_last_name)) < 2:
            pass
        elif len(str(leader_last_name)) < 2:
            pass
        elif any(numeral in leader_last_name for numeral in roman_numeral_list):
            pass
        elif any(numeral in other_leader_last_name for numeral in roman_numeral_list):
            pass
        elif any(numeral in leader_title for numeral in roman_numeral_list):
            pass
        elif any(numeral in other_leader_title for numeral in roman_numeral_list):
            pass
        else:
            if leader_name != other_leader:
                for meeting in eval(list_setter):
                    specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')
                    sd_all_matches = specific_day.findall(meeting)
                    sd = sd_all_matches[0]
                    if str(leader_name) in str(meeting):
                        yao = sd + '\n' + diff_country + '\t' + leader_title + '\n'
                        if yao not in total_meeting_list:
                            total_meeting_list.append(yao)
                    elif str(other_leader) in str(meeting):
                        yao = sd + '\n' + diff_country + '\t' + other_leader_title + '\n'
                        if yao not in total_meeting_list:
                            total_meeting_list.append(yao)
            else:
                for meeting in eval(list_setter):
                    if str(leader_last_name) in str(meeting):
                        searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}'.format(str(leader_title), "{0,5}", str(leader_last_name), re.IGNORECASE))
                        exact_match = searcher.findall(meeting)
                        for match in exact_match:
                            yao = sd + '\n' + diff_country + '\t' + leader_title + '\n'
                            if yao not in total_meeting_list:
                                if any(country in meeting for country in country_name_list):
                                    for country in country_name_list:
                                        if country in yao:
                                            if country in meeting:
                                                total_meeting_list.append(yao)
                                else:
                                    total_meeting_list.append(yao)
                    elif str(other_leader_last_name) in str(meeting):
                        searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}'.format(str(other_leader_title), "{0,5}", str(other_leader_last_name), re.IGNORECASE))
                        exact_match = searcher.findall(meeting)
                        for match in exact_match:
                            yao = sd + '\n' + diff_country + '\t' + other_leader_title + '\n'
                            if yao not in total_meeting_list:
                                if any(country in meeting for country in country_name_list):
                                    for country in country_name_list:
                                        if country in yao:
                                            if country in meeting:
                                                total_meeting_list.append(yao)
                                else:                           
                                    total_meeting_list.append(yao)
                    elif str(asian_leader_last_name) in str(meeting):
                        searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}'.format(str(leader_title), "{0,5}", str(asian_leader_last_name), re.IGNORECASE))
                        exact_match = searcher.findall(meeting)
                        for match in exact_match:
                            yao = sd + '\n' + diff_country + '\t' + leader_title + '\n'                       
                            if yao not in total_meeting_list:
                                if any(country in meeting for country in country_name_list):
                                    for country in country_name_list:
                                        if country in yao:
                                            if country in meeting:
                                                total_meeting_list.append(yao)
                                else:
                                    total_meeting_list.append(yao)
                    elif str(asian_other_leader_last_name) in str(meeting):
                        searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}'.format(str(other_leader_title), "{0,5}", str(asian_other_leader_last_name), re.IGNORECASE))
                        exact_match = searcher.findall(meeting)
                        for match in exact_match:
                            yao = sd + '\n' + diff_country + '\t' + other_leader_title + '\n'
                            if yao not in total_meeting_list:
                                if any(country in meeting for country in country_name_list):
                                    for country in country_name_list:
                                        if country in yao:
                                            if country in meeting:
                                                total_meeting_list.append(yao)
                                else:
                                    total_meeting_list.append(yao)
                    elif str('State Dinner') in str(meeting):
                        searcher = re.compile(r'{}\W+(?:\w+\W+){}?{}'.format(str('attend'), "{0,80}", str('a toast'), re.IGNORECASE))
                        exact_match = searcher.findall(meeting)
                        for match in exact_match:
                            yao = sd + '\n' + match + '\n'
                            if yao not in total_meeting_list:
                                total_meeting_list.append(yao)

        
    additional_filtration_list = []
    multilateral_country_list = ['G-20', 'G20', 'G8', 'G7', 'ASEAN', 'ASEAN-', 'APEC', 'G-8', 'Arctic Council', 'NATO', 'CARICOM', 'Gulf Cooperation Council', 'GCC', 'G-7', 'Summit of the Americas', 'East Asia Summit', 'Strategic and Economic Dialogue']
    alternative_title_list = ['CEO', 'Crown Prince', 'Sultan', 'Defense Minister', 'Deputy Crown Prince', 'Deputy PM', 'Finance Minister', 'Pope', 'Secretary of State', 'Minister of Enviornment',
                          'Foreign Minister', 'Foregin Minster', 'Foreign Secretary', 'Vice-Premeir', 'Deputy CroPri',
                          'Minister of Foreign Affairs', 'Minister of External Relations', 'Opposition Leader', 'Premier', 'Chairman and General Secretary of the National League of Democracy',
                          'Defense Minister', 'Minister for Foreign Affairs', 'Minister of Foreign Affairs', 'Minister of Finance', 'Minister of Foreign Trade', 'State Counselor',
                          'Minister of Environment', 'Minister of Natural Resources', 'Secretary of Foreign Relations', 'State Councilor', 'Premier of the State Council',
                          'Minister of Power', 'Minister of State for Foreign Affairs','Vice Prez', 'Vice Premier', 'former Prez', 'former PM']

    #To make sure title matches with country, so canada/UK dosn't have a president
    for diff_country in newest_country_and_list_thats_useable:
        leader_name = str(new_country_leader_list[diff_country][2])
        leader_country = str(new_country_leader_list[diff_country][0])
        other_leader = str(new_country_leader_list[diff_country][-1])
        other_leader_title = str(new_country_leader_list[diff_country][-2])
        leader_title = str(new_country_leader_list[diff_country][1])
        for meetings in total_meeting_list:
            print('line 481', meetings)
            if any(str(country) in str(meetings) for country in country_name_list):
                if str('CEO') in str(meetings):
                    if ('Afghan') in str(meetings):
                        additional_filtration_list.append(meetings)
                elif str('Taoiseach') in str(meetings):
                    if ('Ireland') in str(meetings):
                        additional_filtration_list.append(meetings)
                elif str('working dinner') in str(meetings):
                    if any(multi in meetings for multi in multilateral_country_list):
                        if meetings not in additional_filtration_list:
                            additional_filtration_list.append(meetings)
                elif str('working lunch') in str(meetings):
                    if any(multi in meetings for multi in multilateral_country_list):
                        if meetings not in additional_filtration_list:
                            additional_filtration_list.append(meetings)
                    else:
                        pass
                else:
                    if meetings not in additional_filtration_list:
                        additional_filtration_list.append(meetings)


    duplicate_check_meetings_list = ['place_holder']
    #This filters for specific errors
    for meeting in additional_filtration_list:
        meeting = str(meeting)
        prvious_element = duplicate_check_meetings_list[-1]
        last_appended_item = prvious_element
        if meeting[:18] != prvious_element[:18]:
            if 'Mali' in str(meeting) and 'Iraq' in str(prvious_element):
                pass
            elif str('Nigeria') in str(meeting) and str('Niger') in last_appended_item:
                duplicate_check_meetings_list.pop()
                duplicate_check_meetings_list.append(meeting)
            elif str('of the Dominica ') in str(meeting):
                pass
            elif str('working lunch') in str(meeting):
                lunch = meeting.replace('working lunch', 'working dinner')
                if lunch not in duplicate_check_meetings_list:
                    duplicate_check_meetings_list.append(lunch)
            elif str('Minster') in str(meeting):
                meeting = meeting.replace('Minster', 'Minister')
                if meeting not in duplicate_check_meetings_list:
                    duplicate_check_meetings_list.append(meeting)
            elif str('Dominican Republic') in str(meeting) and str('Dominica') in last_appended_item:
                duplicate_check_meetings_list.pop()
                duplicate_check_meetings_list.append(meeting)
            elif str('China, Peoples Republic of') in str(meeting):
                new_china = meeting.replace("China, Peoples Republic of", "China")
                duplicate_check_meetings_list.append(new_china)            
            elif 'Peoples Republic of China' in str(meeting):
                new_china = meeting.replace('Peoples Republic of China', "China")
                duplicate_check_meetings_list.append(new_china)
            elif str('Republic of Korea') in str(meeting):
                new_korea = meeting.replace("Republic of Korea", "South Korea")
                duplicate_check_meetings_list.append(new_korea)
            elif str('G8') in str(meeting):
                g8 = meeting.replace("G8", "G-8")
                duplicate_check_meetings_list.append(g8)
            elif str('G7') in str(meeting):
                g7 = meeting.replace("G7", "G-7")
                if g7 not in duplicate_check_meetings_list:
                    duplicate_check_meetings_list.append(g7)
            elif str('G20') in str(meeting):
                g20 = meeting.replace("G20", "G-20")
                if g20 not in duplicate_check_meetings_list:
                    duplicate_check_meetings_list.append(g20)
            elif str('United States') in str(meeting):
                pass
            elif str('China, Republic of (Taiwan)') in str(meeting):
                new_taiwan = meeting.replace("China, Republic of (Taiwan)", "Taiwan")
                duplicate_check_meetings_list.append(new_taiwan)
            elif str('President of the Council of Ministers') in str(meeting):
                pass
            elif str('President of the Government') in str(meeting):
                pass
            else:
                if meeting not in duplicate_check_meetings_list:
                    duplicate_check_meetings_list.append(meeting)
        else:
            for country in country_name_list:
                if str(country) in str(meeting) and str(prvious_element):
                    for title in leader_list:
                        if str(title) in meeting:
                            if str(title) not in str(prvious_element):
                                if meeting not in duplicate_check_meetings_list:
                                    duplicate_check_meetings_list.append(meeting)
                else:
                    if meeting not in duplicate_check_meetings_list:
                        duplicate_check_meetings_list.append(meeting)

    #Further filtration
    new_duplicate_sorting = ['place holder']                         
    for dup in sorted(duplicate_check_meetings_list):
        if dup != new_duplicate_sorting[-1]:
            if str('Federal') in str(dup) and str('Chancellor') in str(new_duplicate_sorting[-1]):
                pass
            elif 'UK' in str(dup):
                dup = dup.replace("UK", "United Kingdom")
                if dup not in new_duplicate_sorting:
                    new_duplicate_sorting.append(dup)
            elif str('Chancellor') in str(dup):
                if str('Germany') in str(dup):
                    if dup not in new_duplicate_sorting:
                        new_duplicate_sorting.append(dup)                   
                elif str('Merkel') in str(dup):
                    if dup not in new_duplicate_sorting:
                        new_duplicate_sorting.append(dup)
            elif 'Nigeria ' in str(dup) and str('Niger ') in str(new_duplicate_sorting[-1]):
                new_duplicate_sorting.pop()
                new_duplicate_sorting.append(dup)
            elif 'Nigerian' in str(dup):
                pass
            elif str('Foreign Secretary') in str(dup):
                dup = dup.replace("Foreign Secretary", "Foreign Minister")
                if dup not in duplicate_check_meetings_list:
                    duplicate_check_meetings_list.append(dup)
            elif str('Minister of State for Foreign Affairs') in str(dup):
                if 'United Arab Emirates' in str(dup):
                    dup = dup.replace("Minister of State for Foreign Affairs", "Foreign Minister")
                    if dup not in duplicate_check_meetings_list:
                        duplicate_check_meetings_list.append(dup)
                else:
                    pass
            elif 'a href=' in str(dup):
                pass
            elif 'Taoiseach' in str(dup) and str('Ireland	Prime Minister') in str(new_duplicate_sorting[-1]):
                pass
            elif 'ession' in str(dup):
                for country in multilateral_country_list:
                    if country not in str(dup):
                        pass
                    else:
                        new_duplicate_sorting.append(dup)
            elif 'eeting' in str(dup):
                for country in multilateral_country_list:
                    if country not in str(dup):
                        pass
                    else:
                        new_duplicate_sorting.append(dup)           
            else:
                if dup not in new_duplicate_sorting:
                    new_duplicate_sorting.append(dup)

    different_country_list_names = ['Niger', 'Ivory Coast']
    new_list = ['place holder']
    multilateral_event_list = ['photo', 'inner', 'eeting', 'ession', 'argins']

    #Final Filtration to check if country, demonym or multlateral organization is in string
    for a in new_duplicate_sorting:
        for country in country_dem_list:
            if str(country[1]) in str(a):
                for leader in leader_list:
                    if str(leader) in str(a):
                        specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')
                        sd_all_matches = specific_day.findall(a)
                        sd = sd_all_matches[0]
                        all_in_one = sd + '\n' + str(country[0]) + '\t' + str(leader) + '\n'
                        if all_in_one not in new_list:
                            if any(str(event) in str(all_in_one) for event in multilateral_event_list):
                                pass
                            else:
                                if 'Sudan' in str(a) and 'South Sudan' in str(new_list[-1]):
                                    pass
                                elif 'Republic of the Congo' in str(a) and 'Democratic Republic of the Congo' in str(new_list[-1]):
                                    pass
                                else:
                                    new_list.append(all_in_one)
            elif str(country[0]) in str(a):
                if str(a) not in new_list:
                    if any(str(event) in str(a) for event in multilateral_event_list):
                        pass
                    else:
                        if 'Sudan' in str(a) and 'South Sudan' in str(new_list[-1]):
                            pass
                        elif 'Republic of the Congo' in str(a) and 'Democratic Republic of the Congo' in str(new_list[-1]):
                            pass
                        else:
                            new_list.append(a)
            else:
                for country in multilateral_country_list:
                    if str(country) in str(a):
                        if 'President' in str(a):
                            a = a.replace('President', 'Summit Meeting')
                            if a not in new_list:
                                new_list.append(a)
                        elif 'remier' in str(a):
                            pass
                        elif 'Prime Minister' in str(a):
                            a = a.replace('Prime Minister', 'Summit Meeting')
                            if a not in new_list:
                                new_list.append(a)
                        elif 'GCC' in str(a):
                            a = a.replace('GCC', 'Gulf Cooperation Council')
                            if a not in new_list:
                                new_list.append(a)
                        elif 'G20' in str(a):
                            a = a.replace('G20', 'G-20')
                            if a not in new_list:
                                new_list.append(a)
                        elif 'G7' in str(a):
                            a = a.replace('G7', 'G-7')
                            if a not in new_list:
                                new_list.append(a)
                        elif str(country) in str(new_list[-1]):
                            specific_day = re.compile(r'\w{3,9} \d{1,2}, \d\d\d\d')
                            sd_all_matches = specific_day.findall(a)
                            sd = sd_all_matches[0]
                            if sd in new_list[-1] and a:
                                pass
                            else:
                                if a not in new_list:
                                    new_list.append(a)
                        else:
                            if a not in new_list:
                                new_list.append(a)
                for diff_count in different_country_list_names:
                    if str(diff_count) in str(a):
                        if a not in new_list:
                            new_list.append(a)                        

    return {'new_list':new_list}

def database_updater(country_name_list, new_list):

    engine = create_engine('postgres://gbwbpntofkrmsw:2507b82970b5a13014f347ca1e2d3858f306698fe700ac8c859ce5f7ac2598bc@ec2-107-20-191-76.compute-1.amazonaws.com:5432/d2tm6s6rp66r9p')
    conn = engine.connect()

    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = 0;''')
    
    Two_pt_leader_list = ['President', 'Prime Minister', 'Prime Minster', 'King', 'Chancellor', 'Taoiseach', 'Queen', 'Amir', 'Emperor', 'Pope', 'Sultan']
    One_pt_leader_list = ['CEO', 'Crown Prince', 'Defense Minister', 'Deputy Crown Prince', 'Deputy PM', 'Finance Minister', 'Secretary of State',
                          'Foreign Minister', 'Foregin Minster', 'Foreign Secretary', 'State Counselor', 'Secretary of Defense', 'Minister of Oil', 'Minister of Defense',
                          'Minister of Foreign Affairs', 'Minister of External Relations', 'Opposition Leader', 'Premier', 'Chairman and General Secretary of the National League of Democracy',
                          'Defense Minister', 'Minister for Foreign Affairs', 'Minister of Foreign Affairs', 'Minister of Finance', 'Minister of Foreign Trade', 'Deputy CroPri',
                          'Minister of Environment', 'Minister of Natural Resources', 'Secretary of Interior', 'Secretary of Finance', 'Secretary of Foreign Relations', 'State Councilor', 'Premier of the State Council', 'Minister of Enviornment',
                          'Minister of Power', 'Minister of State for Foreign Affairs','Vice Prez', 'Vice Premier', 'Vice-Premeir']
    half_pt_leader_list = ['former Prez', 'former PM', 'President-elect']

    processed_list = ['place holder']
    for meeting in new_list:
        for country in country_name_list:
            if str(country) in str(meeting):
                for leader in Two_pt_leader_list:
                    if str(leader) in str(meeting):
                        if meeting not in processed_list:
                            print(str(country), 'aaa')
                            conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                            processed_list.append(meeting)
                for leader in One_pt_leader_list:
                    if str(leader) in str(meeting):
                        if meeting not in processed_list:
                            conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 1 WHERE "Country_Name" = '{}';'''.format(country))
                            print(str(country), 'bbb')
                            processed_list.append(meeting)
                for leader in half_pt_leader_list:
                    if str(leader) in str(meeting):
                        if meeting not in processed_list:
                            conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + .5 WHERE "Country_Name" = '{}';'''.format(country))
                            print(str(country), 'ccc')
                            processed_list.append(meeting)

    caricom = ['Antigua and Barbuda', 'Bahamas, the', 'Barbados', 'Belize', 'Dominica', 'Grenada', 'Guyana', 'Haiti', 'Jamaica', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago']
    apec = ['Australia', 'Brunei', 'Canada', 'Chile', 'China', 'Taiwan', 'Indonesia', 'Japan', 'South Korea', 'Malaysia', 'Mexico', 'New Zealand', 'Peru', 'Philippines', 'Papua New Guinea', 'Russia', 'Singapore', 'Thailand', 'Vietnam']
    Summit_of_the_Americas = ['Antigua and Barbuda', 'Argentina', 'Barbados', 'Brazil', 'Belize', 'Bahamas', 'Bolivia', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Saint Kitts and Nevis', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela']
    G_8_List = ['Russia', 'United Kingdom', 'France', 'Italy', 'Canada', 'Germany', 'Japan']
    G_7_List = ['United Kingdom', 'France', 'Italy', 'Canada', 'Germany', 'Japan']
    Artic_Council_List = ['Canada', 'Denmark', 'Finland', 'Iceland', 'Norway', 'Russia', 'Sweden']
    G_20_List = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Italy', 'Japan', 'South Korea', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa', 'Turkey', 'United Kingdom']
    NATO = ['Albania', 'Belgium', 'Bulgaria', 'Canada', 'Croatia', 'Czech Republic', 'Denmark', 'Estonia', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Turkey', 'United Kingdom']
    GCC = ['Bahrain', 'Kuwait', 'Oman', 'Qatar', 'Saudi Arabia', 'United Arab Emirates']
    East_asia_summit = ['Australia', 'Brunei', 'Cambodia', 'China', 'India', 'Indonesia', 'Japan', 'Laos', 'Malaysia', 'Myanmar', 'New Zealand', 'Philippines', 'Russia', 'Singapore', 'South Korea', 'Thailand', 'Vietnam']
    ASEAN = ['Brunei', 'Cambodia', 'Indonesia', 'Laos', 'Malaysia', 'Myanmar', 'Philippines', 'Singapore', 'Thailand', 'Vietnam', 'Papua New-Guinea', 'East Timor']


    for meeting in new_list:
        #State Dinner = 5 Points
        if str('State Dinner') in str(meeting):
            for country in country_name_list:
                if str(country) in str(meeting):
                    if meeting not in processed_list:
                        conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 5 WHERE "Country_Name" = '{}';'''.format(country))
                        processed_list.append(meeting)
        #Bilateal Events
        if str('Strategic and Economic Dialogue') in str(meeting):
            if meeting not in processed_list:
                conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = 'China';''')
                processed_list.append(meeting)
        if str('Her Majesty the Queen') in str(meeting):
            if meeting not in processed_list:
                conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = 'United Kingdom';''')
                processed_list.append(meeting)
        # Multilateal Events
        if str('G-20') in str(meeting):
            if meeting not in processed_list:
                for country in G_20_List:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting)
        if str('Arctic Council') in str(meeting):
            if meeting not in processed_list:
                for country in Artic_Council_List:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting)                            
        if str('CARICOM') in str(meeting):
            if meeting not in processed_list:
                for country in caricom:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting) 
        if str('Summit of the Americas') in str(meeting):
            if meeting not in processed_list:
                for country in Summit_of_the_Americas:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting) 
        if str('NATO') in str(meeting):
            if meeting not in processed_list:
                for country in NATO:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting) 
        if str('Gulf Cooperation Council') in str(meeting):
            if meeting not in processed_list:
                for country in GCC:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting) 
        if str('G-8') in str(meeting):
            if meeting not in processed_list:
                if 'Prime Minister' not in str(meeting):
                    for country in G_8_List:
                        conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                    processed_list.append(meeting) 
        if str('ASEAN') in str(meeting):
            if meeting not in processed_list:
                for country in ASEAN:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting)
        if str('East Asia Summit') in str(meeting): 
            if meeting not in processed_list:
                for country in East_asia_summit:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting)
        if str('G-7') in str(meeting):
            if meeting not in processed_list:
                if 'Prime Minister' not in str(meeting):
                    for country in G_7_List:
                        conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                    processed_list.append(meeting) 
        if str('APEC') in str(meeting):
            if meeting not in processed_list:
                for country in apec:
                    conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                processed_list.append(meeting)
        else:
            for country in country_name_list:
                if str(country) in str(meeting):
                    for leader in Two_pt_leader_list:
                        if str(leader) in str(meeting):
                            if meeting not in processed_list:
                                print(str(country), 'aaa')
                                conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 2 WHERE "Country_Name" = '{}';'''.format(country))
                                processed_list.append(meeting)
                    for leader in One_pt_leader_list:
                        if str(leader) in str(meeting):
                            if meeting not in processed_list:
                                conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + 1 WHERE "Country_Name" = '{}';'''.format(country))
                                print(str(country), 'bbb')
                                processed_list.append(meeting)
                    for leader in half_pt_leader_list:
                        if str(leader) in str(meeting):
                            if meeting not in processed_list:
                                conn.execute('''UPDATE "Sec_State_Bureaucratic_Exchange" SET "Sec_of_State_2017" = "Sec_of_State_2017"::int + .5 WHERE "Country_Name" = '{}';'''.format(country))
                                print(str(country), 'ccc')
                                processed_list.append(meeting)

    
def main():
    country_name_list = country_name_acquistion()['country_name_list']
    kerry_daily_meetings_list = daily_sched_search()['SecState_daily_meetings_list']       
    country_dem_list = country_name_acquistion()['country_dem_list']
    
    meeting_search(kerry_daily_meetings_list, country_name_list)
    new_PRES_MEETING_LIST = meeting_search(kerry_daily_meetings_list, country_name_list)['new_PRES_MEETING_LIST']
    new_list = country_and_leader_getter(new_PRES_MEETING_LIST, country_name_list, country_dem_list)['new_list']

    
    database_updater(country_name_list, new_list)
    
    time2 = time.time()
    print("Total Time to run", time2-time1, 'seconds')
main()

