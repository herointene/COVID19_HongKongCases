#!/usr/bin/env python
# coding: utf-8

# In[21]:


import requests
from urllib.parse import urlencode
import pandas as pd
import time

def get_page():
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    params = {"f": "json",
              "where": "1=1",
              "returnGeometry": "false",
              "spatialRel": "esriSpatialRelIntersects",
              "outFields": "*",
              "orderByFields": "個案編號 desc",
              "resultOffset": "0",
              "resultRecordCount": "30000",
              "resultType": "standard",
              "cacheHint": "true"
    }
    url='https://services8.arcgis.com/PXQv9PaDJHzt8rp0/arcgis/rest/services/Merge_Display_0227_test_view/FeatureServer/0/query?'+ urlencode(params)
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        content = r.json()
    return content

def save_to_csv(content):
    cases = content['features']
    df = pd.DataFrame([case.get('attributes')for case in cases])
    date = time.strftime('%d_%m',time.localtime())
    df.to_csv('covid19case_full_{}.csv'.format(date), index=False, encoding='utf-8-sig')  

if __name__ == '__main__':
    print('Starting collect...')
    content = get_page()
    save_to_csv(content)
    print('Successfully saved csv file. The programe will shutdown in 5 seconds.')
    time.sleep(5)
    print('done')

