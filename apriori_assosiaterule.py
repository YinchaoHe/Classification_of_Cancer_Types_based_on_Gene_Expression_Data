import argparse
import time
from numpy import *

import ioprocess



def loadDataSet():
    #return [[1, 2, 3, 4, 6], [2, 3, 4, 5, 6], [1, 2, 3, 5, 6], [1, 2, 4, 5, 6]]
    #return  [[1,2,3], [2,3,4], [1,2,4], [1,2,3,4]]
    return [[1,2,3,4, 5]]
def generate_c0(dataset):
    c0 = []
    c0_scount_dic = {}
    for transaction in dataset:
        for item in transaction:
            key = frozenset([item])
            if key in c0:
                c0_scount_dic[key] += 1
            else:
                    c0.append(key)
                    c0_scount_dic[key] = 1
    c0.sort()
    return c0, c0_scount_dic

def generate_lk(dataset, ck, ck_scount_dic, min_support):
    lk = []
    lk_scount_dic = {}
    for item in ck:
        support = ck_scount_dic[item] / float(len(dataset))
        if support >= min_support:
            lk.append(item)
            lk_scount_dic[item] = ck_scount_dic[item]

    return lk, lk_scount_dic

def generate_ck(lk, k, dataset):
    ck = []
    for i in range(len(lk)):
        for j in range(i + 1, len(lk)):
            l1 = list(lk[i])[:k-1]
            l2 = list(lk[j])[:k-1]
            if l1 == l2:
                ck.append(lk[i]|lk[j])
    ck_scount_dic = cal_ck_scount(ck, dataset)
    return ck, ck_scount_dic

def cal_ck_scount(ck, dataset):
    ck_scount_dic = {}
    for itemset in ck:
        ck_scount_dic[itemset] = 0
    for transaction in dataset:
        for itemset in ck:
            if itemset.issubset(transaction):
                if itemset in ck_scount_dic.keys():
                    ck_scount_dic[itemset] += 1

    return ck_scount_dic

def find_frequent_set_apriori(dataset, min_support):

    c0, c0_scount_dic = generate_c0(dataset)
    l0, l0_scount_dic = generate_lk(dataset, c0, c0_scount_dic, min_support)
    l = [l0]
    l_scount_dic = {}
    l_scount_dic.update(l0_scount_dic)
    k = 1
    while len(l[k - 1]) != 0:
        ck, ck_scount_dic = generate_ck(l[k-1], k, dataset)
        lk, lk_scount_dic = generate_lk(dataset, ck, ck_scount_dic, min_support)
        lk.sort()
        l.append(lk)
        l_scount_dic.update(lk_scount_dic)
        k += 1
    # for itemset in l:
    #     for item in itemset:
    #         print(len(item))
    return l, l_scount_dic

def generate_subassio_rule_L1(fre_itemset, items, l_scount_dic, assic_rules, minConf):

    for item in items:
        new_item = list(item)
        #print("new_item", new_item)
        conf = l_scount_dic[fre_itemset] / l_scount_dic[frozenset(new_item)]
        #print(conf)
        right = list(set(fre_itemset).difference(set(item)))
        #print("difference:", right)
        if conf >= minConf and len(right) > 0:
            assic_rules.append((new_item, right, conf))


def generate_subassio_rule_L2(fre_itemset, items, l_scount_dic, assic_rules, minConf, dataset):
    m = len(items[0])
    if len(fre_itemset) > m+1:
        Hmp1, scount = generate_ck(items, m, dataset)
        if len(Hmp1) > 1:
            generate_subassio_rule_L2(fre_itemset, Hmp1, l_scount_dic, assic_rules, minConf, dataset)
            #print(Hmp1)
        generate_subassio_rule_L1(fre_itemset, Hmp1, l_scount_dic, assic_rules, minConf)
    if m == 1:
        #print(items)
        generate_subassio_rule_L1(fre_itemset, items, l_scount_dic, assic_rules, minConf)


def generate_assio_rules(l, l_scount_dic, minConf, dataset):
    assic_rules = []
    for i in range(1, len(l)):
        for itemset in l[i]:
            #print("fre_itemset: ", itemset)
            items = [frozenset([item]) for item in itemset]
            #print("items:", items)
            if i > 1:
                generate_subassio_rule_L2(itemset, items, l_scount_dic, assic_rules, minConf, dataset)
            else:
                generate_subassio_rule_L1(itemset, items, l_scount_dic, assic_rules, minConf)
    return assic_rules




