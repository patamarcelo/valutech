#!/usr/local/bin/python3
from pytrends.request import TrendReq
import pandas as pd
import time

import json


pytrends = TrendReq(hl='pt-PT', tz=180)

def combine_dicts(dict_list):
    d = {}    
    for dct in dict_list:
        d.setdefault(dct['id'], {}).update(dct)
    data = list(d.values())
    return data


def related_queries(keyword):
    kw_list = [keyword] # list of keywords to get data 
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='BR') 
    #get related queries
    related_queries = pytrends.related_queries()
    top = list(related_queries.values())[0]['top']
    rising = list(related_queries.values())[0]['rising']

    try:
        if not top.empty:
            top = top.to_dict()
            combine_top = []
            for k,v in top.items():
                for i,l in v.items():
                    nd = {'id': i, k: l}
                    combine_top.append(nd)
            top = combine_dicts(combine_top)
    except Exception as e:
        print(f'Error: {e}')

    try:
        if not rising.empty:
            rising = rising.to_dict()
            combine_rising = []
            for k,v in rising.items():
                for i,l in v.items():
                    nd = {'id': i, k: l}
                    combine_rising.append(nd)
            rising = combine_dicts(combine_rising)
    except Exception as e:
        print(f'Error: {e}')
    return {'top': top, 'rising': rising}
