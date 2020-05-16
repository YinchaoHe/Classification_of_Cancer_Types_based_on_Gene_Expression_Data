import csv
import itertools
from concepts import Context
import numpy as np
np.set_printoptions(threshold=np.inf)
import sys

with open('forFCA-11PCA_data.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    tableCells = [[word for word in line] for line in csv_reader]
    number_of_objects = len(tableCells)
    number_of_columns = len(tableCells[0]) - 1
    class_array = np.array([float(tableCells[x][number_of_columns]) for x in range(number_of_objects)])
    unique_classes = list(range(int(max(class_array)) + 1))
    matrix = np.array([[float(tableCells[x][y]) for y in range(number_of_columns)] for x in range(number_of_objects)])
    th = 0.6
    context_matrix = [['X' if y >= th else '' for y in x] for x in matrix]
    output_matrix = [['' for j in range(number_of_columns+1)] for i in range(number_of_objects + 1)]
    outputCSVFile = open('train_output.csv', 'w+')
    wtr = csv.writer(outputCSVFile, delimiter=',', lineterminator='\n')
    for i in range(number_of_objects+1):
        for j in range(number_of_columns+1):
            if i == 0 and j == 0:
                output_matrix[i][j] = ''
            elif i == 0 and j > 0:
                output_matrix[i][j] = 'c' + str(j-1)
            elif i > 0 and j == 0:
                output_matrix[i][j] = str(i-1)
            else:
                output_matrix[i][j] = str(context_matrix[i-1][j-1])
        wtr.writerow(output_matrix[i])
    outputCSVFile.close()
    train_dict = {}
    c = Context.fromfile('train_output.csv', 'csv')

    # sys.stdout = open('output1.txt', 'w+')
    for extent, intent in c.lattice:
        #print('%r %r' % (extent, intent))
        # attribute_combinations = np.asarray(intent)
        if intent not in train_dict:
            count = 0
            extent_array = np.asarray(extent)
            for row in extent_array:
                if count == 0:
                    train_dict[intent] = [int(float(tableCells[int(row)][number_of_columns]))]
                    count = count + 1
                else:
                    train_dict[intent].append(int(float(tableCells[int(row)][number_of_columns])))

    #print(train_dict)
    final_train_dict = {}
    for key_combination in train_dict:
        total_classes = len(train_dict[key_combination])
        class_dict = {}
        class_sorted_array = []
        class_dict = {class_id: 0 for class_id in unique_classes}
        for class_id in train_dict[key_combination]:
            class_dict[class_id] += 1
        for class_id in class_dict:
            class_sorted_array.append(class_dict[class_id] / total_classes)

        final_train_dict[key_combination] = class_sorted_array
    #print(final_train_dict)
    csv_file.close()

with open('forFCA-11PCA_data.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    tableCells = [[word for word in line] for line in csv_reader]
    number_of_objects = len(tableCells)
    #print(number_of_objects)
    number_of_columns = len(tableCells[0]) - 1
    class_array = np.array([float(tableCells[x][number_of_columns]) for x in range(number_of_objects)])
    class_test_dict = {idx: val for idx, val in sorted(enumerate(class_array))}
    #print(class_test_dict)
    unique_classes = list(range(int(max(class_array)) + 1))
    matrix = np.array([[float(tableCells[x][y]) for y in range(number_of_columns)] for x in range(number_of_objects)])
    th = 0.6
    context_matrix = [['X' if y >= th else '' for y in x] for x in matrix]
    output_matrix = [['' for j in range(number_of_columns+1)] for i in range(number_of_objects + 1)]
    outputCSVFile = open('test_output.csv', 'w+')
    wtr = csv.writer(outputCSVFile, delimiter=',', lineterminator='\n')
    for i in range(number_of_objects+1):
        for j in range(number_of_columns+1):
            if i == 0 and j == 0:
                output_matrix[i][j] = ''
            elif i == 0 and j > 0:
                output_matrix[i][j] = 'c' + str(j-1)
            elif i > 0 and j == 0:
                output_matrix[i][j] = str(i-1)
            else:
                output_matrix[i][j] = str(context_matrix[i-1][j-1])
        wtr.writerow(output_matrix[i])
    outputCSVFile.close()
    outputCSVFile.close()
test_dict = {}
c = Context.fromfile('test_output.csv', 'csv')
    # sys.stdout = open('output1.txt', 'w+')
for extent, intent in c.lattice:
    #print('%r %r' % (extent, intent))
    # attribute_combinations = np.asarray(intent)
    if intent not in test_dict:
        count = 0
        extent_array = np.asarray(extent)
        for row in extent_array:
            if count == 0:
                test_dict[intent] = [int(row)]
                count = count + 1
            else:
                test_dict[intent].append(int(row))

#print(test_dict)
bc = list()
count = 0
for combination in test_dict:
    if combination in final_train_dict:
        bc.append((test_dict[combination],final_train_dict[combination]))
    else:
        count = count + 1
objClassProbDists = {}
temp_dict = {}
#print("ls")
#print(count)
#print(bc)
#print("lgggs")
for rows in bc:
    for objIdx in rows[0]:
        if objIdx in objClassProbDists:
            objClassProbDists[objIdx].append(rows[1])
        else:
            objClassProbDists[objIdx] = [rows[1]]
#print(objClassProbDists)
for key in sorted(objClassProbDists):
    temp_dict[key] = np.argmax(np.sum(np.array(objClassProbDists[key]), axis=0))
#print(len(temp_dict))
diffkeys = np.array([k for k in temp_dict if temp_dict[k] == class_test_dict[k]])
print(1-(len(diffkeys)/800))