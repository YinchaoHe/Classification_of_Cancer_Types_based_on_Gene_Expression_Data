import argparse
import time

import ioprocess
import apriori_assosiaterule
def get_reference(dic_freset, class_name, l, l_scount_dic):
    largest_number = 0
    if len(l) == 0:
        dic_freset[class_name] = "NONE"
    else:
        for reference in l[len(l)-1]:
            if l_scount_dic[reference] > largest_number:
                largest_number = l_scount_dic[reference]

        for reference in l[len(l)-1]:
            if l_scount_dic[reference] == largest_number:
                if class_name == 'PRAD':
                    dic_freset[class_name] = reference
                elif class_name == 'LUAD':
                    dic_freset[class_name] = reference
                elif class_name == 'BRCA':
                    dic_freset[class_name] = reference
                elif class_name == 'KIRC':
                    dic_freset[class_name] = reference
                else:
                    dic_freset[class_name] = reference

def train(min_support, min_confi, method_name, attribution_number):
    dic_freset ={}.fromkeys(['PRAD','LUAD','BRCA', 'KIRC', 'COAD'],'default_value')
    min_supports = []
    MP, ML, MB, MK, MC = ioprocess.sub_csv2martix(method_name, attribution_number)

    flag = min_support
    min_supports.append(min_support)

    l_MP, l_MP_scount_dic = apriori_assosiaterule.find_frequent_set_apriori(MP, min_support)
    l_MP.remove([])
    l_MP.sort()
    get_reference(dic_freset, 'PRAD', l_MP, l_MP_scount_dic)
    assio_rule_list_MP = apriori_assosiaterule.generate_assio_rules(l_MP, l_MP_scount_dic, min_confi, MP)
    ioprocess.rule2txt(assio_rule_list_MP, min_support, flag, len(assio_rule_list_MP), min_confi, l_MP, str(attribution_number) + 'attributions/' +method_name+ "_assio_rule_PRAD.txt")

    l_ML, l_ML_scount_dic = apriori_assosiaterule.find_frequent_set_apriori(ML, min_support)
    l_ML.remove([])
    l_ML.sort()
    get_reference(dic_freset, 'LUAD', l_ML, l_ML_scount_dic)
    assio_rule_list_ML = apriori_assosiaterule.generate_assio_rules(l_ML, l_ML_scount_dic, min_confi, ML)
    ioprocess.rule2txt(assio_rule_list_ML, min_support, flag, len(assio_rule_list_ML), min_confi, l_ML, str(attribution_number) + 'attributions/' +method_name+ "_assio_rule_LUAD.txt")

    l_MB, l_MB_scount_dic = apriori_assosiaterule.find_frequent_set_apriori(MB, min_support)
    l_MB.remove([])
    l_MB.sort()
    get_reference(dic_freset, 'BRCA', l_MB, l_MB_scount_dic)
    assio_rule_list_MB = apriori_assosiaterule.generate_assio_rules(l_MB, l_MB_scount_dic, min_confi, MB)
    ioprocess.rule2txt(assio_rule_list_MB, min_support, flag, len(assio_rule_list_MB), min_confi, l_MB, str(attribution_number) + 'attributions/' +method_name+ "_assio_rule_BRCA.txt")

    l_MK, l_MK_scount_dic = apriori_assosiaterule.find_frequent_set_apriori(MK, min_support)
    l_MK.remove([])
    l_MK.sort()
    get_reference(dic_freset, 'KIRC', l_MK, l_MK_scount_dic)
    assio_rule_list_MK = apriori_assosiaterule.generate_assio_rules(l_MK, l_MK_scount_dic, min_confi, MK)
    ioprocess.rule2txt(assio_rule_list_MK, min_support, flag, len(assio_rule_list_MK), min_confi, l_MK, str(attribution_number) + 'attributions/' + method_name+ "_assio_rule_KIRC.txt")

    l_MC, l_MC_scount_dic = apriori_assosiaterule.find_frequent_set_apriori(MC, min_support)
    l_MC.remove([])
    l_MC.sort()
    get_reference(dic_freset, 'COAD', l_MC, l_MC_scount_dic)
    assio_rule_list_MC = apriori_assosiaterule.generate_assio_rules(l_MC, l_MC_scount_dic, min_confi, MC)
    ioprocess.rule2txt(assio_rule_list_MC, min_support, flag, len(assio_rule_list_MC), min_confi, l_MC, str(attribution_number) + 'attributions/' + method_name+ "_assio_rule_COAD.txt")

    return dic_freset

def test(dic_freset, class_name, method_name, attribution_number, dataset):

    labels_list = ioprocess.csv2list()
    tt_count = 0.0
    ff_count = 0.0
    total_count = len(dataset)
    row_number = 0
    BRCA_number= 0
    COAD_number = 0
    KIRC_number = 0
    LUAD_number = 0
    PRAD_number = 0
    target_number = 0
    if dic_freset[class_name] == 'NONE':
        print(class_name + str(tt_count))
        return 0
    while row_number < total_count:
        if set(dataset[row_number]) > dic_freset[class_name]:
            target_number += 1
            if class_name == labels_list[row_number]:
                tt_count += 1
            elif labels_list[row_number] == 'BRCA':
                BRCA_number += 1
            elif labels_list[row_number] == 'COAD':
                COAD_number += 1
            elif labels_list[row_number] == 'KIRC':
                KIRC_number += 1
            elif labels_list[row_number] == 'LUAD':
                LUAD_number += 1
            else:
                PRAD_number += 1
        else:
            if labels_list[row_number] != class_name:
                ff_count += 1
        row_number += 1

    for tumor_type in ['PRAD',  'LUAD', 'BRCA', 'KIRC','COAD']:
        if tumor_type == class_name:
            print(class_name + ": " + str(tt_count))
        elif tumor_type == 'BRCA':
            print(tumor_type + ": " + str(BRCA_number))
        elif tumor_type == 'COAD':
            print(tumor_type + ": " + str(COAD_number))
        elif tumor_type == 'KIRC':
            print(tumor_type + ": " + str(KIRC_number))
        elif tumor_type == 'LUAD':
            print(tumor_type + ": " + str(LUAD_number))
        else:
            print(tumor_type + ": " + str(PRAD_number))
    return tt_count


def main():
    parser = argparse.ArgumentParser(description='Test for CSCE474 Apriori Algrithm')
    parser.add_argument('--minsupport', '-s', help='min support', default= 0.6)
    parser.add_argument('--minconfi', '-c', help='min confi', default = 0.4)
    parser.add_argument('--method_name','-m', help='method_name', default='mean')
    parser.add_argument('--attribution_number', '-n', help='attribution_number', default = 11)
    args = parser.parse_args()
    start_time = time.time()
    min_support = float(args.minsupport)
    min_confi = float(args.minconfi)
    method_name = args.method_name
    attribution_number = args.attribution_number
    dic_freset = train(min_support, min_confi, method_name, attribution_number)

    dataset = ioprocess.csv2matrix('ordered_' + method_name + '_data.csv', attribution_number)
    accuracy = 0.0
    tt_number = 0
    total_count = len(dataset)
    for class_name in dic_freset.keys():
        print("-------" + class_name + "-------")
        tt_number += test(dic_freset, class_name, method_name, attribution_number, dataset)
    accuracy = tt_number * 100 / total_count
    end_time = time.time()
    print(end_time - start_time)
    print("accuracy" + " : " + str(accuracy) + "%")


if __name__ == '__main__':
    main()