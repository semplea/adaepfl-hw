from bs4 import BeautifulSoup

import requests
import pandas as pd
import re

"""
Example usage:
>>> from data_mining import *
>>> mine_data('2009', 'B1')
...


Will output a list of dict.
Each dict contains the section, the year, and the dataframe containing all the data.
"""

years = {'2007': '978181', '2008': '978187', '2009': '978195', '2010': '39486325', '2011': '123455150', '2012': '123456101', '2013': '213637754', '2014': '213637922', '2015-2016': '213638028', '2016':'355925344'}
semesters = {'B1': '249108', 'B6': '942175', 'B6b': '2226785', 'M1': '2230106', 'M3': '2230128', 'M4': '2230140', 'PMAut': '249127', 'PMPri': '3781783'}

def get_url(year, semester):
    y, s = years[year], semesters[semester]
    return 'http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?ww_x_GPS=-1&ww_i_reportModel=133685247&ww_i_reportModelXsl=133685270&ww_x_UNITE_ACAD=null&ww_x_PERIODE_ACAD='+ y +'&ww_x_PERIODE_PEDAGO=' + s + '&ww_x_HIVERETE=null'

def request(year, semester):
    url = get_url(year, semester)
    return requests.get(url, verify=False)

def get_soup(year, semester):
    r = request(year, semester)
    data = r.text
    return BeautifulSoup(data)


def get_table(soup):
    table = soup.html.body.table
    last_section = ""
    list_df  = []
    tc = table.children
    for c in tc:
        tagName = next(c.children).name
        if tagName == "th":
            attrs = c.text.split(',')
            nb_student = int(attrs[2].split("(")[1].split(" ")[0])
            if nb_student != 0:
                next_row = next(tc, None)
                columns = map(lambda l: l.text, next_row.children)
                df = pd.DataFrame(columns=columns)
                d = {"section": attrs[0], "year": attrs[1], "nb": nb_student, "df": df}
                list_df.append(d)
        else:
            t = list(map(lambda l: l.text, c.children))[:-1]
            df.loc[df.shape[0]] = t

    return list_df

def mine_data(year, semester):
    soup = get_soup(year, semester)
    return get_table(soup)
