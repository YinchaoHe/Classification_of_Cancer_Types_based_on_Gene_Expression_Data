import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neural_network import MLPClassifier
import random

file1 = open('Data/11PCAData.csv','r')
file2 = open('Data/PCALabels.csv','r')
x = []
y = []
uniqueLables = {}
for i in file1.readlines():
    line = i.split(",")
    x.append(line[1:])
    
for i in file2.readlines():
    line = i.split(",")
    y.append(line[-1])
    if(line[-1] not in uniqueLables.keys()):
        uniqueLables[line[-1]] = 0
    else:
        uniqueLables[line[-1]] += 1
print(uniqueLables)
#print(len(uniqueLables))


def printResults(predictions,y_test,name):
    correct = 0
    wrong = 0
    for i in range(len(predictions)):
        if(predictions[i] == y_test[i]):
            correct += 1
        else:
            wrong += 1
    print(name)
    print("Accuracy :",correct/(correct+wrong))
    print()
    
x = np.array(x)


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5, shuffle=True)
clf = svm.SVC(gamma='scale')
clf = clf.fit(X_train, y_train) 
predictions = clf.predict(X_test)
printResults(predictions,y_test,"SVM")

PP = 0
PL = 0
PB = 0
PK = 0
PC = 0
LP = 0
LL = 0
LB = 0
LK = 0
LC = 0
BP = 0
BL = 0
BB = 0
BK = 0
BC = 0
KP = 0
KL = 0
KB = 0
KK = 0
KC = 0
CP = 0
CL = 0
CB = 0
CK = 0
CC = 0
for i in range(len(predictions)):
    if("PRAD" in predictions[i] and "PRAD" in y_test[i]):
        PP += 1
    elif("PRAD" in predictions[i] and "LUAD" in y_test[i]):
        PL += 1
    elif("PRAD" in predictions[i] and "BRCA" in y_test[i]):
        PB += 1
    elif("PRAD" in predictions[i] and "KIRC" in y_test[i]):
        PK += 1
    elif("PRAD" in predictions[i] and "COAD" in y_test[i]):
        PC += 1
    elif("LUAD" in predictions[i] and "PRAD" in y_test[i]):
        LP += 1
    elif("LUAD" in predictions[i] and "LUAD" in y_test[i]):
        LL += 1
    elif("LUAD" in predictions[i] and "BRCA" in y_test[i]):
        LB += 1
    elif("LUAD" in predictions[i] and "KIRC" in y_test[i]):
        LK += 1
    elif("LUAD" in predictions[i] and "COAD" in y_test[i]):
        LC += 1
    elif("BRCA" in predictions[i] and "PRAD" in y_test[i]):
        BP += 1
    elif("BRCA" in predictions[i] and "LUAD" in y_test[i]):
        BL += 1
    elif("BRCA" in predictions[i] and "BRCA" in y_test[i]):
        BB += 1
    elif("BRCA" in predictions[i] and "KIRC" in y_test[i]):
        BK += 1
    elif("BRCA" in predictions[i] and "COAD" in y_test[i]):
        BC += 1
    elif("KIRC" in predictions[i] and "PRAD" in y_test[i]):
        KP += 1
    elif("KIRC" in predictions[i] and "LUAD" in y_test[i]):
        KL += 1
    elif("KIRC" in predictions[i] and "BRCA" in y_test[i]):
        KB += 1
    elif("KIRC" in predictions[i] and "KIRC" in y_test[i]):
        KK += 1
    elif("KIRC" in predictions[i] and "COAD" in y_test[i]):
        KC += 1
    elif("COAD" in predictions[i] and "PRAD" in y_test[i]):
        CP += 1
    elif("COAD" in predictions[i] and "LUAD" in y_test[i]):
        CL += 1
    elif("COAD" in predictions[i] and "BRCA" in y_test[i]):
        CB += 1
    elif("COAD" in predictions[i] and "KIRC" in y_test[i]):
        CK += 1
    elif("COAD" in predictions[i] and "COAD" in y_test[i]):
        CC += 1
    




print(PP,PL,PB,PK,PC)
print(LP,LL,LB,LK,LC)
print(BP,BL,BB,BK,BC)
print(KP,KL,KB,KK,KC)
print(CP,CL,CB,CK,CC)

