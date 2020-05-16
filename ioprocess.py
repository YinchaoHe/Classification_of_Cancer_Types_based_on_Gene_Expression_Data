import csv
import os

import numpy as np
from matplotlib import pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


def invert_ordered(method_name, attribution_number):
    file_path = os.getcwd() + "/data/" +str(attribution_number)
    file_path_input = file_path + "US_data.csv"
    np_data = np.loadtxt(file_path_input, dtype=np.str, delimiter=',')
    amount_row = int(np_data.shape[0])
    amount_column = np_data.shape[1]
    if method_name == 'mean':
        index_row = 0
        index_column = 0
        sum = 0
        while index_column < amount_column:
            while index_row < amount_row:
                sum += float(np_data[index_row, index_column])
                index_row += 1
            index_row = 0
            mean = sum / amount_row
            while index_row < amount_row:
                if float(np_data[index_row, index_column]) > mean:
                    np_data[index_row, index_column] = 1
                else:
                    np_data[index_row, index_column] = 0
                index_row += 1
            index_row = 0
            index_column += 1
            sum = 0

        index_column = 0
        while index_row < amount_row:
            while index_column < amount_column:
                if int(np_data[index_row, index_column]) == 1:
                    np_data[index_row, index_column] = index_column + 1
                index_column += 1
            index_row += 1
            index_column = 0

    elif method_name == 'median':
        index_row = 0
        index_column = 0
        while index_column < amount_column:
            list_column = sorted(np_data[:, index_column])
            if len(list_column) % 2 == 1:
                median = float(list_column[int(len(list_column) / 2)+ 1])
            else:
                median = (float(list_column[int(len(list_column) / 2)]) + float(
                    list_column[int(len(list_column) / 2) + 1])) / 2
            index_row = 0
            while index_row < amount_row:
                if float(np_data[index_row, index_column]) > median:
                    np_data[index_row, index_column] = 1
                else:
                    np_data[index_row, index_column] = 0
                index_row += 1
            index_row = 0
            index_column += 1

        index_column = 0
        while index_row < amount_row:
            while index_column < amount_column:
                if int(np_data[index_row, index_column]) == 1:
                    np_data[index_row, index_column] = index_column + 1
                index_column += 1
            index_row += 1
            index_column = 0

    else:
        index_row = 0
        index_column = 0
        while index_column < amount_column:
            list_column = sorted(np_data[:, index_column])
            item_dic = {}.fromkeys(list_column, 0)
            largest_count = 1
            mode = 0.0
            for item in list_column:
                item_dic[item] += 1

            for item in item_dic.keys():
                if item_dic[item] > largest_count:
                    mode = float(item)
                    largest_count = item_dic[item]
            if mode == 0:
                exit('The method do not work, because their is no mode')

            index_row = 0
            while index_row < amount_row:
                if float(np_data[index_row, index_column]) > mode:
                    np_data[index_row, index_column] = 1
                else:
                    np_data[index_row, index_column] = 0
                index_row += 1
            index_row = 0
            index_column += 1

        index_column = 0
        while index_row < amount_row:
            while index_column < amount_column:
                if int(np_data[index_row, index_column]) == 1:
                    np_data[index_row, index_column] = index_column + 1
                index_column += 1
            index_row += 1
            index_column = 0


    np.savetxt(file_path +'attributions/' + 'ordered_' + method_name +'_data.csv', np_data, fmt="%s", delimiter=",")


def integrate_data(method_name, attribution_number):
    file_path = os.getcwd() + "/data/"
    np_data = np.loadtxt(file_path + str(attribution_number) + 'attributions/' + "ordered_" + method_name + "_data.csv", dtype=np.str, delimiter=',')
    PRAD_data = []
    LUAD_data = []
    BRCA_data = []
    KIRC_data = []
    COAD_data = []
    index_row = 0
    with open(file_path + 'labels.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        index_row = 0
        for row in csv_reader:
            if row[1] == "PRAD" :
                PRAD_data.append(np_data[index_row])

            elif row[1] == "LUAD":
                LUAD_data.append(np_data[index_row])

            elif row[1] == "BRCA":
                BRCA_data.append(np_data[index_row])

            elif row[1] == "KIRC":
                KIRC_data.append(np_data[index_row])

            else:
                COAD_data.append(np_data[index_row])

            index_row += 1

        file_path += str(attribution_number)
        file_path += 'attributions/'
        np.savetxt(file_path + method_name + "_PRAD.csv", PRAD_data, fmt="%s", delimiter=",")
        np.savetxt(file_path + method_name + "_LUAD.csv", LUAD_data, fmt="%s", delimiter=",")
        np.savetxt(file_path + method_name + "_BRCA.csv", BRCA_data, fmt="%s", delimiter=",")
        np.savetxt(file_path + method_name + "_KIRC.csv", KIRC_data, fmt="%s", delimiter=",")
        np.savetxt(file_path + method_name + "_COAD.csv", COAD_data, fmt="%s", delimiter=",")

def csv2list():
    l = []
    file_path = os.getcwd() + '/data/'
    with open(file_path+'labels.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            l.append(row[1])
    return l

def csv2matrix(file_name, attribution_number):
    file_path = os.getcwd() + '/data/' + str(attribution_number) + 'attributions/'
    n = 800
    m = attribution_number
    dp = [[0 for i in range(m)] for j in range(n)]
    line = 0
    column = 0
    M = []
    T = []
    with open(file_path + file_name, encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for column in range(0, attribution_number):
                dp[line][column] = int(row[column])  # 将csv中数据放入矩阵中，若写入的为零表示此人没有这个性质
            line += 1
    for r in range(0, 800):
        for c in range(0, attribution_number):
            if dp[r][c] != 0:
                T.append(dp[r][c])
        M.append(T)
        T = []
    return M

def sub_csv2martix(method_name, attribution_number):
    file_path = os.getcwd() + '/data/' + str(attribution_number) + "attributions/"
    n = 800
    m = attribution_number
    dp = [[0 for i in range(m)] for j in range(n)]
    line = 0
    column = 0
    T = []
    MP = []
    ML = []
    MB = []
    MK = []
    MC = []
    with open(file_path + method_name + '_PRAD.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for column in range(0, attribution_number):
                dp[line][column] = int(row[column])  # 将csv中数据放入矩阵中，若写入的为零表示此人没有这个性质
            line += 1
    for r in range(0, 100):
        for c in range(0, attribution_number):
            if dp[r][c] != 0:
                T.append(dp[r][c])
        MP.append(T)
        T = []

    line = 0
    with open(file_path + method_name + '_LUAD.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for column in range(0, attribution_number):
                dp[line][column] = int(row[column])  # 将csv中数据放入矩阵中，若写入的为零表示此人没有这个性质
            line += 1
    for r in range(0, 100):
        for c in range(0, attribution_number):
            if dp[r][c] != 0:
                T.append(dp[r][c])
        ML.append(T)
        T = []

    line = 0
    with open(file_path + method_name + '_BRCA.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for column in range(0, attribution_number):
                dp[line][column] = int(row[column])  # 将csv中数据放入矩阵中，若写入的为零表示此人没有这个性质
            line += 1
    for r in range(0, 200):
        for c in range(0, attribution_number):
            if dp[r][c] != 0:
                T.append(dp[r][c])
        MB.append(T)
        T = []

    line = 0
    with open(file_path + method_name + '_KIRC.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for column in range(0, attribution_number):
                dp[line][column] = int(row[column])  # 将csv中数据放入矩阵中，若写入的为零表示此人没有这个性质
            line += 1
    for r in range(0, 100):
        for c in range(0, attribution_number):
            if dp[r][c] != 0:
                T.append(dp[r][c])
        MK.append(T)
        T = []

    line = 0
    with open(file_path + method_name + '_COAD.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for column in range(0, attribution_number):
                dp[line][column] = int(row[column])  # 将csv中数据放入矩阵中，若写入的为零表示此人没有这个性质
            line += 1
    for r in range(0, 50):
        for c in range(0, attribution_number):
            if dp[r][c] != 0:
                T.append(dp[r][c])
        MC.append(T)
        T = []
    return MP, ML, MB, MK, MC

def write2csv(min_supports, min_confis, result_list_support, result_list_confi):
    with open("runtime.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["mininum_support", "run_time(s)"])

        for i in range(len(min_supports)):
            writer.writerow([min_supports[i], result_list_support[i][0]])

    with open("rulenumber.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["mininum_confi", "rulenumber"])
        for i in range(len(min_supports)):
            writer.writerow([min_supports[i], result_list_support[i][1]])


def rule2txt(assio_rule_list, minu_sppoort, flag, rulenumber, minu_confi, l, file_name):
    file_path = os.getcwd() + "/output/" + file_name
    if flag == minu_sppoort:
        f = open(file_path, 'w')
    else:
        f = open(file_path, 'a')
    f.write("minum_support:" + str(minu_sppoort) + " the amount of rules:" + str(rulenumber) + " the min_confi: " + str(minu_confi))
    f.write("\n")
    for i in range(len(l)):
        f.write("l[" + str(i) + "]: " + str(len(l[i])) + "     ")
    f.write("\n")
    for rule in assio_rule_list:
        f.write(str(rule[0]) + " ——> " + str(rule[1]) + ", confi:" + str(rule[2]))
        f.write("\n")
    f.write("\n")
    f.write("\n")
    f.close()

def reduction_PCA():
    file_path = os.getcwd() + '/data/'
    dataNumpy = np.loadtxt(file_path + "reducedData.csv", dtype=np.str, delimiter=',')
    pca = PCA(n_components=5)
    data_tsne = pca.fit_transform(dataNumpy)
    np.savetxt(file_path + "21PCA_data.csv", data_tsne, fmt="%s", delimiter=",")

def reduction_Univariate_Selection():
    file_path = os.getcwd() + '/data/'
    dataNumpy = np.loadtxt(file_path + "reducedData.csv", dtype=np.str, delimiter=',')
    array_extend = np.ones([1, 800], dtype=str)
    dataNumpy_new = np.c_[dataNumpy, array_extend.T]
    with open(file_path + 'labels.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        index_row = 0
        for row in csv_reader:
            if row[1] == "PRAD":
                dataNumpy_new[index_row][-1] = '0'

            elif row[1] == "LUAD":
                dataNumpy_new[index_row][-1] = '1'

            elif row[1] == "BRCA":
                dataNumpy_new[index_row][-1] = '2'

            elif row[1] == "COAD":
                dataNumpy_new[index_row][-1] = '3'

            else:
                dataNumpy_new[index_row][-1] = '4'

            index_row += 1
    dataNumpy_new = dataNumpy_new.astype(float)
    Y = dataNumpy_new[:, dataNumpy.shape[1]]
    X = dataNumpy_new[:, 0:dataNumpy.shape[1]]
    test = SelectKBest(score_func=f_classif, k = 10)
    fit = test.fit(X, Y)
    np.set_printoptions(precision=3)
    list_index = []
    numpy_sorted = np.sort(fit.scores_)[-11:]
    for item in numpy_sorted:
        index = 0
        while index < len(fit.scores_):
            if item == fit.scores_[index]:
                list_index.append(index)
            index += 1

    us_dataset = []
    for index in list_index:
        if len(us_dataset):
            us_dataset = np.c_[us_dataset, dataNumpy_new[:, index]]
        else:
            us_dataset = dataNumpy_new[:, index]

    np.savetxt(file_path + "11US_data.csv", us_dataset, fmt="%s", delimiter=",")






def main():
    #reduction_Univariate_Selection()
    invert_ordered('mean', 11)
    integrate_data("mean", 11)


if __name__ == '__main__':
    main()