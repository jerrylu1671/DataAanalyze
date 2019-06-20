# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:40:11 2019

@author: eason.lu
"""

import pandas as pd
# import matplotlib.pyplot as plt

result_file_path="result.csv"
StartIndex=9
StartAnalzyeDate=180

rdata=pd.read_csv(result_file_path)
rdata["Yrate"]=0.0
rdata["MaxDropPercent"]=0.0
rdata["MaxDropDays"]=0
rdata["MaxDropDate"]=""

today=rdata.iloc[StartIndex]
Xmax=0.0
Xmaxindex=0
Xmin=0.0
Xlen=0
Ymax=1.0
Ymaxindex=0
Ymin=10.0
Ylen=0

bmax=today["total"]
bmin=bmax
bindex=StartIndex

tradeCount=0

for i in range(StartIndex+1, rdata.shape[0]):
    t=rdata.iloc[i]["Comments"]
    if (t.startswith("Sold")):
        tradeCount+=1
    cmax=rdata.iloc[i]["total"]    
    if (cmax>=bmax):
        if (((bmax-bmin)/bmax)>((Ymax-Ymin)/Ymax)):
            Ymax=bmax
            Ymin=bmin
            Ylen=i-bindex
            Ymaxindex=bindex
        if ((i-bindex)>Xlen):
            Xmax=bmax
            Xmin=bmin
            Xlen=i-bindex
            Xmaxindex=bindex
        bmax=cmax
        bmin=cmax
        bindex=i
    if (cmax<bmin):
        bmin=cmax

print("Max length of drop ", rdata.iloc[Xmaxindex]["Date"], Xmax, Xmin, Xlen, 1-Xmin/Xmax)
print("Max percent of drop ", rdata.iloc[Ymaxindex]["Date"], Ymax, Ymin, Ylen, 1-Ymin/Ymax)
print("total trade:", tradeCount)

y=20.5
total=rdata.iloc[rdata.shape[0]-1]["total"]
import numpy as np
a=np.power(10, np.log10(total/10000)/y)
print("Yearly rate:", a)



        




