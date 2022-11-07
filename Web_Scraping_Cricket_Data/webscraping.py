import os.path

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import openpyxl

def team_test_data_extraction(format_type):

    ## The list of these following teams have been removed because they do not have data in test matches  -{ '29':'Ireland', '28': 'Namibia', '33': 'Nepal','15': 'Netherlands','37':'Oman', '20': 'Papua New Guinea', '30': 'Scotland', '27': 'UAE', '11': 'USA'}
    team_name = {"2":'Australia',"25":'Bangladesh', '1':'England', '6':'India', '5':'New Zealand', '7': 'Pakistan', '3':'South Africa', '8':'Sri Lanka', '4':'West Indies', '9': 'Zimbabwe', '40': 'Afghanistan'}
    format_dict = {'1': 'Test', '2': 'ODIs', '3':'T20I'}
    df_lst = []

    for n,id in enumerate(team_name.keys()):

        print(f'ID={id}')
        URL = f'https://stats.espncricinfo.com/ci/engine/records/team/results_summary.html?class={str(format_type)};id={str(id)};type=team'
        page = requests.get(URL)
        bs = BeautifulSoup(page.content, features="html.parser")
        table_body = bs.findAll('tbody')
        # print(table_body[0:4:2])

        df = pd.DataFrame(
            columns=['Opposition', 'Span', 'Matches', 'Won', 'Lost', 'Tied', 'Draw', 'W/L', 'Win%', 'Loss%', 'Draw%'])

        for i,table in enumerate(table_body):
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                # print(cols)

                df = df.append(pd.Series(cols, index=df.columns),ignore_index=True)
        print(f'df={df}')
        df['Opposition'] = df['Opposition'].str.replace("v ","")
        df_lst.append(df)

        # df.to_excel(f'{format_dict[format_type]}_match_list.xlsx')
        df.to_excel(f'{format_dict[format_type]}_match_list.xlsx', sheet_name= team_name[id], index=False)

    with pd.ExcelWriter(f'{format_dict[format_type]}_match_list.xlsx', mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        for id,df in zip(team_name.keys(),df_lst):
            df.to_excel(writer,sheet_name=team_name[id], index=False)


def team_odi_data_extraction(format_type):
    team_name = {"2": 'Australia', "25": 'Bangladesh', '1': 'England', '6': 'India', '5': 'New Zealand',
                 '7': 'Pakistan', '3': 'South Africa', '8': 'Sri Lanka', '4': 'West Indies', '9': 'Zimbabwe',
                 '40': 'Afghanistan'}
    format_dict = {'1': 'Test', '2': 'ODIs', '3': 'T20I'}
    df_lst = []

    for n, id in enumerate(team_name.keys()):

        print(f'ID={id}')
        URL = f'https://stats.espncricinfo.com/ci/engine/records/team/results_summary.html?class={str(format_type)};id={str(id)};type=team'
        page = requests.get(URL)
        bs = BeautifulSoup(page.content, features="html.parser")
        table_body = bs.findAll('tbody')
        # print(table_body[0:4:2])

        df = pd.DataFrame(
            columns=['Opposition', 'Span', 'Matches', 'Won', 'Lost', 'Tied', 'NR', 'Win%'])

        for i, table in enumerate(table_body):
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                # print(cols)

                df = df.append(pd.Series(cols, index=df.columns), ignore_index=True)
        print(f'df={df}')
        df['Opposition'] = df['Opposition'].str.replace("v ", "")
        df_lst.append(df)

        
        df.to_excel(f'{format_dict[format_type]}_match_list.xlsx', sheet_name=team_name[id], index=False)

    with pd.ExcelWriter(f'{format_dict[format_type]}_match_list.xlsx', mode='a', engine='openpyxl',
                        if_sheet_exists='overlay') as writer:
        for id, df in zip(team_name.keys(), df_lst):
            df.to_excel(writer, sheet_name=team_name[id], index=False)

def team_t20_data_extraction(format_type):

    team_name = {"2": 'Australia', "25": 'Bangladesh', '1': 'England', '6': 'India', '5': 'New Zealand',
                 '7': 'Pakistan', '3': 'South Africa', '8': 'Sri Lanka', '4': 'West Indies', '9': 'Zimbabwe',
                 '40': 'Afghanistan'}
    format_dict = {'1': 'Test', '2': 'ODIs', '3': 'T20I'}
    df_lst = []

    for n, id in enumerate(team_name.keys()):

        print(f'ID={id}')
        # https://stats.espncricinfo.com/ci/engine/records/team/results_summary.html?class=1;id=2;type=team
        URL = f'https://stats.espncricinfo.com/ci/engine/records/team/results_summary.html?class={str(format_type)};id={str(id)};type=team'
        page = requests.get(URL)
        bs = BeautifulSoup(page.content, features="html.parser")
        table_body = bs.findAll('tbody')
        

        df = pd.DataFrame(
            columns=['Opposition', 'Span', 'Matches', 'Won', 'Lost', 'Tied', 'Tie+W', 'Tie+L', 'NR', 'Win%'])

        for i, table in enumerate(table_body):
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                

                df = df.append(pd.Series(cols, index=df.columns), ignore_index=True)
        print(f'df={df}')
        df['Opposition'] = df['Opposition'].str.replace("v ", "")
        df_lst.append(df)

        # df.to_excel(f'{format_dict[format_type]}_match_list.xlsx')
        df.to_excel(f'{format_dict[format_type]}_match_list.xlsx', sheet_name=team_name[id], index=False)

    with pd.ExcelWriter(f'{format_dict[format_type]}_match_list.xlsx', mode='a', engine='openpyxl',
                        if_sheet_exists='overlay') as writer:
        for id, df in zip(team_name.keys(), df_lst):
            df.to_excel(writer, sheet_name=team_name[id], index=False)

if __name__ == '__main__':

    # for format class =1-> Test matches ;class=2-> ODIs; class=3-> T20I
    # format_type = {'Test': 1, 'ODIs':2, 'T20I': 3}
    # team_name = {'Australia': 2, 'Bangladesh': 25}

    ## For Test Matches
    format_type = '1'

    team_test_data_extraction(format_type)

    ## For ODIs
    format_type = '2'
    team_odi_data_extraction(format_type)

    ## For T20I
    format_type = '3'
    team_t20_data_extraction(format_type)
