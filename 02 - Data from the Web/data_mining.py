from bs4 import BeautifulSoup

import requests
import pandas as pd
import re

"""
Example usage:
>>> from data_mining import *
>>> mine_data('2009', 'B1', 'Spring')
...


Will output a dict containing a global data frame
The data frame is indexed by the the year, semester, season and section
"""

years = {
	'2007': '978181',
	'2008': '978187',
	'2009': '978195',
	'2010': '39486325',
	'2011': '123455150',
	'2012': '123456101',
	'2013': '213637754',
	'2014': '213637922',
	'2015-2016': '213638028',
	'2016': '355925344'
}

semesters = {
	'B1': '249108',
	'B6': '942175',
	'B6b': '2226785',
	'M1': '2230106',
	'M3': '2230128',
	'M4': '2230140',
	'PMAut': '249127',
	'PMSpr': '3781783'
}

seasons = {
    'Autumn': '2936286',
    'Spring': '2936295'
    }

indexes =  ["year", "semester", "season"]

def get_url(year, semester, season):
    """Get the url corresponding to a given year and semester"""
    y, sem, sea = years[year], semesters[semester], seasons[season]
    return 'http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?ww_x_GPS=-1&ww_i_reportModel=133685247&ww_i_reportModelXsl=133685270&ww_x_UNITE_ACAD=249847&ww_x_PERIODE_ACAD='+ y +'&ww_x_PERIODE_PEDAGO=' + sem + '&ww_x_HIVERETE=' + sea

def request(year, semester, season):
    """return the http request corresponding to a given year and semester"""
    url = get_url(year, semester, season)
    return requests.get(url, verify=False)

def get_soup(year, semester, season):
    """return the data soup (BeautifulSoup) corresponding to a given year and semester"""
    r = request(year, semester, season)
    data = r.text
    return BeautifulSoup(data)


def get_table(soup, year, semester, season):
    """Transform the data soup into a dict containing the data frame
    Each dict contains the section, the year, and the dataframe containing all the corresponding data
    The dataframe contains all the columns returned by the html page + the index corresponding to "indexes"
    """
    global indexes
    table = soup.html.body.table ##get to the table
    list_df  = [] ##init list of data frame
    tc = table.children ##every rows of the table
    first_row = next(tc, None)
    attrs = first_row.text.split(',') ##extract the attributes from the header row
    section = attrs[0]
    year = attrs[1]
    nb_student = int(attrs[2].split("(")[1].split(" ")[0])
    if nb_student != 0: ##next row should contain columns info (except if there is no student)
        next_row = next(tc, None) ##directly iterate our iterator the next row
        columns = indexes + list(map(lambda l: l.text, next_row.children)) ##transform the children into a list of the inner text of each children
        df = pd.DataFrame(columns=columns) ##create the data frame with the columns from this list

    for c in tc:
        t = [year, semester, season] + list(map(lambda l: l.text, c.children))[:-1] ##transform the children into a list of the inner text of each children (corresponding here to each column)
        df.loc[df.shape[0]] = t ##append the data to the last dataframe created


    return {"year": year, "semester": semester, "season": season, "data": df}

def mine_data(year, semester, season):
    soup = get_soup(year, semester, season) ##get the soup
    return get_table(soup, year, semester, season) ##process the soup
