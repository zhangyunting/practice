#coding:utf8
import csv
import re
import random
from scipy.stats import ttest_ind
import numpy


species = ['Arabidopsis thaliana',
'Brassica oleracea',
'Capsicum annuum',
'Cucumis sativus',
'Ectocarpus siliculosus',
'Glycine max',
'Gossypium hirsutum',
'Gossypium raimondii',
'Medicago truncatula',
'Oryza sativa Japonica',
'Sorghum bicolor',
'Vigna radiata',
'Vitis vinifera',
'Zea mays subsp. mays']

def get_range(file):
    '''得到转移序列的范围'''
    file_open = open(file)
    bk = csv.reader(file_open)
    q_range = []
    for row in bk:
        if len(row) != 0:
            q_start = int(row[8])
            q_end = int(row[9])
            q_range.append([q_start,q_end+1])
    file_open.close()
    return q_range


def build_dic(file):
    '''构建第n个是什么碱基的字典'''
    with open(file) as files:
        genomoall = []
        for ii in files.readlines():
            if re.match(r'^>', ii):
                pass
            else:
                genomo = re.findall(r'[A-Z]', ii)
                genomoall = genomoall + genomo
                # print genomoall
        lenth = len(genomoall)
        serial_number = []
        for i in range(1, lenth + 1):
            serial_number.append(int(i))
        dic = dict(zip(serial_number, genomoall))
        files.close()
    return dic

def counting():
    lenth_200 = 0
    lenth_400 = 0
    lenth_600 = 0
    lenth_800 = 0
    lenth_1000 = 0
    lenth_5000 = 0
    lenth_10000 = 0
    lenth_largest = 0
    for i in trans_lenth:
        if int(i) <= 200:
            lenth_200 += 1
        elif 200 < int(i) <= 400:
            lenth_400 += 1
        elif 400 < int(i) <= 600:
            lenth_600 += 1
        elif 600 < int(i) <= 800:
            lenth_800 += 1
        elif 800 < int(i) <= 1000:
            lenth_1000 += 1
        elif 1000 < int(i) <= 5000:
            lenth_5000 += 1
        elif 5000 < int(i) <= 10000:
            lenth_10000 += 1
        elif int(i) > 10000:
            lenth_largest += 1
    print lenth_200
    print lenth_400
    print lenth_600
    print lenth_800
    print lenth_1000
    print lenth_5000
    print lenth_10000
    print lenth_largest


for s in species:
    filename_mt_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' mitochondrion' + '-HitTable.csv'
    filename_chl_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' chloroplast' + '-HitTable.csv'
    filename_mt = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' mitochondrion' + '.fasta'
    filename_chl = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' chloroplast' + '.fasta'

    dic = build_dic(filename_mt)  # 构建第n个是什么碱基的字典               #需替换1
    lenth = len(dic)  # 细胞器基因组长度
    # print lenth

    dicti = {}
    for i in range(1, lenth + 1):
        dicti[i] = 0
    q_range = get_range(filename_mt_hittable)  # 转移的细胞器基因组范围  #需替换2
    trans_lenth = []
    for i in q_range:
        for j in range(i[0], i[1]):  # 若在范围内，计数+1
            d = dicti[j]
            dicti[j] = d + 1
        trans_lenth.append(i[1] - i[0])   #转移的平均长度
    #print numpy.mean(trans_lenth)

    print s
    counting()

