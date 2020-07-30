#!/usr/bin/env python
# coding: utf-8

# In[3]:


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
              "resultRecordCount": "4000",
              "resultType": "standard",
              "cacheHint": "true"
    }
    url='https://services8.arcgis.com/PXQv9PaDJHzt8rp0/arcgis/rest/services/Merge_Buffer_0227_View/FeatureServer/0/query?'+ urlencode(params)
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        content = r.json()
    return content

def save_to_csv(content):
    OBJECTID = []
    case_num = []
    GlobalID = []
    date_confirm = []
    date_onset = []
    gender = []
    age = []
    hospital = []
    resident = []
    Case_classification = []
    confirmed = []
    status = []
    district = []
    shape_area = []
    shape_length = []
    Hospitalised_Discharged_Decease =[]
    
    cases = content.get('features')
    
    for case in cases:
        case_num.append(case.get('attributes').get('Case_no_'))
        date_confirm.append(case.get('attributes').get('Date_of_laboratory_confirmation'))
        date_onset.append(case.get('attributes').get('Date_of_onset'))
        gender.append(case.get('attributes').get('Gender'))
        age.append(case.get('attributes').get('Age'))
        hospital.append(case.get('attributes').get('Name_of_hospital_admitted')) 
        resident.append(case.get('attributes').get('HK_Non_HK_resident')) 
        Case_classification.append(case.get('attributes').get('Case_classification')) 
        confirmed.append(case.get('attributes').get('Confirmed')) 
        status.append(case.get('attributes').get('Status')) 
        district.append(case.get('attributes').get('District'))
        shape_area.append(case.get('attributes').get('Shape__Area')) 
        shape_length.append(case.get('attributes').get('Shape__Length'))
        Hospitalised_Discharged_Decease.append(case.get('attributes').get('Hospitalised_Discharged_Decease'))
        OBJECTID.append(case.get('attributes').get('OBJECTID'))
        GlobalID.append(case.get('attributes').get('GlobalID'))
    df = pd.DataFrame(data=[OBJECTID,case_num,GlobalID,date_confirm,date_onset,Hospitalised_Discharged_Decease,gender,age,hospital,resident,Case_classification,confirmed,status,district,shape_area,shape_length]).T
    df.columns = ['OBJECTID','case_num','GlobalID','date_confirm','date_onset','Hospitalised_Discharged_Decease','gender','age','hospital','resident','Case_classification','confirmed','status','district','shape_area','shape_length']
    date = time.strftime('%d_%m',time.localtime())
    df.to_csv('covid19case{}.csv'.format(date), index=False)                     

if __name__ == '__main__':
    print('Starting collect...')
    content = get_page()
    save_to_csv(content)
    print('Successfully saved csv file. The programe will shutdown in 5 seconds.')
    time.sleep(5)
    print('done')

