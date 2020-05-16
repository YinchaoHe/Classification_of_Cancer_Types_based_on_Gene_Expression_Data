import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import FactorAnalysis
from sklearn.datasets import load_digits
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
import matplotlib.pyplot as plt


df= pd.read_csv('Data/data.csv', header = None)
nums = []

columnNum = 0
columnNames = []
for column in df:
    if(columnNum > 0):
        count = 0
        for i in df[column]:
            if(i > 0):
                count += 1
        if(count < 800):
            columnNames.append(column)
        nums.append(count)
    else:
        columnNames.append(column)
    columnNum += 1
print(columnNum)
print(len(columnNames))


for i in columnNames:
    df.drop(i,axis = 1,inplace = True)
 
df = df.round(3)
print(df)    
df.to_csv('Data/reducedData.csv')


#print(nums)
#nums = np.histogram(nums)
#plt.hist(nums)
#plt.show()
"""    
file1 = open(Data/data.csv','r')
#file2 = open('cleaned.csv','w+')
linenum = 0
for i in file1.readlines():
    if (linenum > -1):
        count = 0
        i = i.split(",")
        newline = ""
        for x in i:
            if(x != "0"):
                count += 1
            newline = newline + x + ","
        if(count > 10):
            newline = newline[:-1]
            #file2.write(newline)
    else:
        file2.write(i)
    linenum += 1

file1.close()
#file2.close()
"""
