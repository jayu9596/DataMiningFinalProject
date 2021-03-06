# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 18:57:31 2020

@author: JAYU
"""
import json
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import csv


def processAreaName(areaName):
    temp = areaName.lower().replace(' ','').replace('district','').replace('state','').replace('-','').replace('*','')
    for i in range(0, 10):
        temp = temp.replace(str(i),'')
    return temp

def processAreaType(areaType):
    temp = areaType.lower().replace(' ','')
    return temp

def processAgeName(ageName):
    temp = ageName.lower().replace(' ','')
    return temp

################## PROGRAM | START ##################

# raw_data1 and raw_data2 csv files for data before 04/25/2020
with open("GujaratOverall2001.csv") as csvFile1:
    rawdata2001 = pd.read_csv(csvFile1)
with open("Overall2011.csv") as csvFile2:
    rawdata2011 = pd.read_csv(csvFile2)
    
data2011 = rawdata2011.dropna()
data2001 = rawdata2001.dropna()

totalDist = set()
mapData2001 = {}
mapData2001 = defaultdict(lambda:[0]*5, mapData2001)
mapData2011 = {}
mapData2011 = defaultdict(lambda:[0]*5, mapData2011)

for index, row in data2001.iterrows():
    distname = processAreaName(row['Area Name'])
    totalDist.add(distname)
    tempList = []
    tempList.append(int(row['Population Persons']))
    tempList.append(int(row['Literate Persons']))
    tempList.append(int(row['Main workers Persons']))
    tempList.append(int(row['Marginal workers Persons']))
    tempList.append(int(row['Non-workers Persons']))
    mapData2001[distname] = tempList
    
for index, row in data2011.iterrows():
    distname = processAreaName(row['Area Name'])
    tempList = []
    tempList.append(int(row['Population Persons']))
    tempList.append(int(row['Literate Persons']))
    tempList.append(int(row['Main workers Persons']))
    tempList.append(int(row['Marginal workers Persons']))
    tempList.append(int(row['Non-workers Persons']))
    mapData2011[distname] = tempList

mapRate = {}
pos = 0
neg = 0
for dist in totalDist:
    key = dist
    value2011 = mapData2011[key]
    value2001 = mapData2001[key]
    tempList = []
    for i in range(0 , 5):
        if value2001[i] >= value2011[i]:
            neg+=1
        else:
            pos+=1
        if value2001[i] == 0:
            tempList.append(0)
        else:
            rate = pow( (value2011[i] / value2001[i]), 0.1) - 1
            tempList.append(rate)
    mapRate[key] = tempList



fileName = 'Generated Gujrat_district-Overall '
for n in range(7, 18):
    dataList = []
    dataList.append(['Area Name','Population Persons','Literate Persons','Main workers Persons','Marginal workers Persons','Non-workers Persons'])
    for dist in totalDist:
        key = dist
        tempList = []
        tempList.append(dist)           
        for j in range(0, 5):
            P = mapData2001[key][j]
            r = mapRate[key][j]
            tempList.append( int( (pow(float(1 + r), n)) * P ) )
        dataList.append(tempList)
    my_df = pd.DataFrame(dataList)
    my_df.to_csv(fileName + str(2000 + n + 1) + '.csv', index=False, header=False)