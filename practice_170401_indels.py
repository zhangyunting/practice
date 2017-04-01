#coding:utf8
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
'Zea mays subsp. mays',
'Vigna angularis'
]

import csv
import re

def get_range(file):
    '''得到转移序列的范围'''
    file_open = open(file)
    bk = csv.reader(file_open)
    q_range = []
    for row in bk:
        if len(row) != 0:
            q_start = int(row[8])
            q_end = int(row[9])
            s_start = int(row[10])
            s_end = int(row[11])
            if s_start <= s_end:
                q_range.append([q_start, q_end, s_start, s_end])
            else:
                s_start, s_end = s_end, s_start
                q_range.append([q_start, q_end, s_start, s_end])
    file_open.close()
    return q_range


def same_start():
    '''找到起始相同的转移，不删除'''
    samestartnumber = 0
    for i in range(len(q_range_sorted)-2, -1, -1):
        if int(q_range_sorted[i][0]) == int(q_range_sorted[i+1][0]):
            #q_range_sorted.pop(i)
            samestartnumber += 1
    return samestartnumber

def same():
    '''找到起始和结束相同的转移'''
    samenumber = 0
    for i in range(len(q_range_sorted)-1):                 #若删除可用倒序：for i in range(len(q_range_sorted)-2,-1,-1):
        if int(q_range_sorted[i][0]) == int(q_range_sorted[i+1][0]) and int(q_range_sorted[i][1]) == int(q_range_sorted[i+1][1]):
            #q_range_sorted.pop(i)
            samenumber += 1
    return samenumber

def including():
    '''排序后，后者包含前者的数量'''
    including_n = 0
    for i in range(len(q_range_sorted)-1):
        if int(q_range_sorted[i][0]) == int(q_range_sorted[i + 1][0]) and int(q_range_sorted[i][1]) < int(
                q_range_sorted[i + 1][1]):
            including_n += 1
    return including_n

def overlap():
    '''排序后，重叠大于9'''
    overlap_n = 0
    for i in range(len(q_range_sorted)-1):
        if int(q_range_sorted[i][1]) - int(q_range_sorted[i + 1][0]) > 9 and int(q_range_sorted[i+1][1]) >= int(
                q_range_sorted[i][1]):
            overlap_n += 1
    return overlap_n

def insertion():
    '''mt中重叠小于3，核中间隔大于3'''
    insertion_n = 0
    for i in range(len(q_range_sorted)-1):
        if 3 > int(q_range_sorted[i+1][0]) - int(q_range_sorted[i][1]) >= 0 and int(q_range_sorted[i+1][2]) - int(q_range_sorted[i][3]) > 3:
            insertion_n += 1
    return insertion_n

def deletion():
    '''核中重叠小于3，mt中间隔大于3'''
    deletion_n = 0
    for i in range(len(q_range_sorted)-1):
        if 3 > int(q_range_sorted[i+1][2]) - int(q_range_sorted[i][3]) >= 0 and int(q_range_sorted[i+1][0]) - int(q_range_sorted[i][1]) > 3:
            deletion_n += 1
    return deletion_n

for s in species:
    filename_mt_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' mitochondrion' + '-HitTable.csv'
    filename_chl_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' chloroplast' + '-HitTable.csv'
    filename_mt = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' mitochondrion' + '.fasta'
    filename_chl = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' chloroplast' + '.fasta'

    q_range = get_range(filename_mt_hittable)  # 转移的细胞器基因组范围  #需替换2
    q_range_sorted = sorted(q_range)

    print str(s) + '\t' + str(len(q_range_sorted)) + '\t' + str(same_start()) + '\t' + str(same()) + '\t' + str(
        including()) + '\t'+ str(overlap())+ '\t' + str(insertion()) + '\t' + str(deletion())




