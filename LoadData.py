# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:05:17 2019

@author: eason.lu
"""

import pandas as pd
import matplotlib.pyplot as plt

LocalRange=10
AverageLen=9
AdjClose="Adj Close"


# load the csv data into pandas list
def loadCsvData(filepath):
    data = pd.read_csv(filepath)
    return data

def test_loadCsvData():
    data=loadCsvData("spy.csv")
    findLocalMaxMin(data,LocalRange,"LocalM")
    findAverage(data,AverageLen, "Average")
    print(data.head())

def FindMaxMin(data,start,end):
    amax = data.iloc[start:end][AdjClose].max()
    amin = data.iloc[start:end][AdjClose].min()
    return amax, amin

def findLocalMaxMin(data, len, cname):
    data[cname]=0
    for i in range(len,data.shape[0]-len):
        lmax,lmin=FindMaxMin(data,i-len,i-1)
        rmax,rmin=FindMaxMin(data,i+1,i+len)
        today=data.iloc[i]
        if (rmax<today[AdjClose] and lmax<today[AdjClose]):
                data.at[i,cname]=1
        if (rmin>today[AdjClose] and lmin>today[AdjClose]):
                data.at[i,cname]=-1
    return

def findAverage(data, len, cname):
    data[cname]=data[AdjClose]
    for i in range(len-1,data.shape[0]):
        ave=data.iloc[i-len+1:i+1][AdjClose].mean()
        data.at[i,cname]=ave
    return

def DownloadQuota():
    link = "https://finance.yahoo.com/quote/C/history"
    from urllib.request import urlopen
    f=urlopen(link)
    myfile=f.read()
    myfilearray=bytearray(myfile)
    fb=open("filename2.txt","wb")
    fb.write(myfilearray)
    fb.close()
    return

def BuyOnceOrManyTimes():
    data=loadCsvData('spy.csv')
    CDistributePurchase="DistributePurchase"
    CDiff="Diff"
    
    data[CDistributePurchase]=0.0
    data["Diff"]=0.0
    distributedays=180
    total=500000.0
    for i in range(0,data.shape[0]-distributedays):
        pshare=0.0
        for j in range(i,i+distributedays):
            pshare = pshare + (total/distributedays)/data.iloc[j][AdjClose]
        data.at[i,CDistributePurchase]=pshare
        data.at[i,CDiff]=pshare*data.iloc[i][AdjClose]-total
        print(i, data.iloc[i]["Date"], data.iloc[i][CDiff])
    return

"""
    strategy based on put/call ratio 
"""
def BuyByPCR():
    sdata=loadCsvData('spy.csv')
    pdata=loadCsvData("equitypc.csv")
    cash=100000.0
    share=0.0
    total_row=sdata.shape[0]
    buy_pcr=0.78
    sell_pcr=0.42
    PCR_column="P/C Ratio"
    gg=sdata[["Date", AdjClose]]
    gg[PCR_column]=pdata[[PCR_column]]
    return

"""
    Simple stratgy by the 100 MovingAverage
"""
sdata=loadCsvData('spy.csv')
sdata["total"]=0.0
pdata=loadCsvData("equitypc.csv")
total=0.0
cash=100000.0
share=0.0
order=0
orderp=0
orderadjustp=0
total_row=sdata.shape[0]
#findLocalMaxMin(sdata,LocalRange,"LocalM")
findAverage(sdata,AverageLen, "Average")
sdata["Comments"]=" "
today=sdata.iloc[0]
delta=1.02
for i in range(AverageLen,total_row):
    today=sdata.iloc[i]
    
    # process the order
    if ((order>0 and orderp>today["Low"]) or (order>1)):
        if (order>1):
            orderadjustp=orderadjustp+today["Open"]-orderp            
        elif (orderp>today["High"]):
            orderadjustp=orderadjustp+today["High"]-orderp
        share+=cash/orderadjustp
        cash=0
        sdata.at[i,"Comments"]="Bought " + today["Date"] +" "+str(orderadjustp)
        print("Bought ", today["Date"], orderadjustp, share)
        order=0
    elif (order<0 and orderp<today["High"]):
        if (orderp<today["Low"]):
            orderadjustp=orderadjustp+today["Low"]-orderp
        cash+=share*orderadjustp
        share=0
        sdata.at[i,"Comments"]="Sold " + today["Date"] +" "+str(orderadjustp)
        print("Sold ", today["Date"], orderadjustp, cash)
        order=0   
    
    #calculate account
    total = cash+share*today[AdjClose]
    sdata.at[i,"total"]=total
    if (i%50 ==0):
        print("total ", today["Date"], total)
        
    
    #decide the current order
    if (order>0): # buy order
        order+=1
        if (today[AdjClose] <= today["Average"] ):
            order=0
            print("Cancel order")
    if (order<0): # sell order
        if (today[AdjClose] >= today["Average"]):
            order=0
            print("Cancel order")
    if (order != 0):
        continue
       
    # place order 
    if (today["Average"]<today[AdjClose]):
        if (cash>0):
            order=1
            orderp=today["Close"]
            orderadjustp=today[AdjClose]
            print("Buy ", today["Date"], orderadjustp)
    
    if (today["Average"]>today[AdjClose]*delta):
        if (share>0):
            order=-1
            orderp=today["Close"]
            orderadjustp=today["Average"]
            print("Sell ", today["Date"], orderadjustp)

print("Finish ", today["Date"], total)
sdata.to_csv("result.csv", sep=',')
        
