#coding:utf8
import csv
import re
import random
from scipy.stats import ttest_ind
import numpy
import pylab as pl
import xlwt


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
'Zea mays subsp. mays' ]

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

def average(list):
    sum = 0
    for i in list:
        sum += i
    avg = float(sum)/float(len(list))
    return avg

def each_point_trans_number():
    '''细胞器每个位点转移次数，字典'''
    dicti = {}
    for i in range(1, lenth + 1):
        dicti[i] = 0
    q_range = get_range(filename_mt_hittable)  # 转移的细胞器基因组范围      #需替换2
    for i in q_range:
        for j in range(i[0], i[1]):  # 若在范围内，计数+1
            d = dicti[j]
            dicti[j] = d + 1
    return dicti

def count(times):
    count_number = 0
    for i in list(dicti.values()):
        if i > trans_lenth_avg_all * int(times) * 0.5:
            count_number += 1
    return count_number


def GC_content(file):
    '''GC 含量'''
    lenth = len(file)
    C = file.count('C')
    G = file.count('G')
    CG = (int(C) + int(G)) / float(lenth)
    return CG


def distribution_xls(list_lenth):
    '''柱形图分组，excel输出'''
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    sheet1.write(row, 0, str(s))

    list_hist = pl.hist(list_lenth)
    aa = 1
    while aa <= len(list_hist):
        for i in list_hist[0]:
            sheet1.write(row, aa, i)
            aa += 1
    book.save('C:\\Users\\ASUS\\Desktop\\distribution.xls')


def build_list_100bp():
    list3 = []
    for i in range(1, lenth - 98):
        list2 = []
        for j in range(i, 100 + i):  # 每100bp
            list2.append(dicti[j])
        mean_100 = numpy.mean(list2)  # 转移平均次数
        list3.append(mean_100)
    return list3

row = -1
for s in species:
    row += 1
    filename_mt_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' mitochondrion' + '-HitTable.csv'
    filename_chl_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' chloroplast' + '-HitTable.csv'
    filename_mt = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' mitochondrion' + '.fasta'
    filename_chl = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' chloroplast' + '.fasta'

    dic = build_dic(filename_mt)  # 构建第n个是什么碱基的字典         #需替换1
    lenth = len(dic)  # 细胞器基因组长度
    # print lenth
    dicti = each_point_trans_number()                                  #构建每个位点转移次数字典
    list_dicti_values = list(dicti.values())
    trans_lenth_avg_all = numpy.mean(list_dicti_values)                #转移次数 平均数
    #print trans_lenth_avg_all

    list_100bp_avg = build_list_100bp()                               #每100bp转移的平均数

    list1 = []
    for i in get_range(filename_mt_hittable):              #需替换3
        list1.append(i[1] - i[0])
    #print numpy.mean(list1)                                        #转移平均长度


    import scipy.stats
    n = scipy.stats.kstest(list1, 'norm')
    print n



'''
    files = open('C:\\Users\\ASUS\Desktop\\0315_range_result.txt', 'w')     # 分布结果
    files.write(str(pl.hist(list_dicti_values)[0]) + '\n')
    files.close()


    list3 = []
    for i in range(1,lenth-98):
        list2 = []
        for j in range(i,100+i):                                           #每100bp
            list2.append(dicti[j])
        mean_100 = numpy.mean(list2)                                      #转移平均次数
        list3.append(mean_100)


    files = open('C:\\Users\\ASUS\Desktop\\raimondii mit result.txt', 'w')  # 结果
    for i in range(len(list3)):
        files.write(str(list3[i]) + '\n')
    files.close()
'''
















