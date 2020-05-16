import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score
import operator

mydata = pd.read_csv('5PCA_data.csv')

records = []
records = np.array(mydata.values.tolist())
kmeans = KMeans(n_clusters=5)
kmeans.fit(records)
m = list(kmeans.labels_)
my_dict = {i:m.count(i) for i in m}
print(my_dict)
mydata2 = pd.read_csv('Data/labels.csv')

my_dict = dict(sorted(my_dict.items(), key=operator.itemgetter(1), reverse=True))
finaldict = list(my_dict.keys())
print(finaldict)
records2 = []
records2 = np.array(mydata2.values.tolist())
m2 = mydata2['V1'].tolist()
s = []
for i in m2 :
    if i == 'LUAD':
        s.append(finaldict[1])
    elif i == 'PRAD':
        s.append(finaldict[3])
    elif i == 'BRCA':
        s.append(finaldict[0])
    elif i == 'KIRC':
        s.append(finaldict[2])
    elif i == 'COAD':
        s.append(finaldict[4])
        
results = confusion_matrix(s, m)
accuracy = accuracy_score(s, m)
print(results)
print(accuracy)


