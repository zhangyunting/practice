#coding:utf8
import csv
import re
import random
from scipy.stats import ttest_ind
import numpy


species = ['Arabidopsis thaliana','Sorghum bicolor','Zea mays subsp. mays',
'Cucumis sativus','Glycine max','Ectocarpus siliculosus',
'Gossypium hirsutum','Gossypium raimondii','Elaeis guineensis','Capsicum annuum','Sesamum indicum','Phaseolus vulgaris',
           'Capsicum annuum','Vigna radiata','Vitis vinifera']

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

def find_range_high():
    '''找到连续的>=平均值2倍的片段'''
    i = 1
    j = 1
    list = []
    dic_GC = {}
    while i <= len(dicti):
        if dicti[i] >= avg * 3:
            list.append(i)
            dic_GC[j] = list
            i += 1
        else:
            list = []
            i += 1
            j += 1
    return dic_GC

def find_range_low():
    '''找到连续的<平均值2倍的片段'''
    i = 1
    j = 1
    list = []
    dic_GC = {}
    while i <= len(dicti):
        if dicti[i] < avg * 3:
            list.append(i)
            dic_GC[j] = list
            i += 1
        else:
            list = []
            i += 1
            j += 1
    return dic_GC

def GC_low():
    '''随机找长度>highGC的片段，返回ATGC序列'''
    key = []
    list_GC_low = []
    for x in dic_GC_low:
        key.append(x)
    a = random.randrange(len(key))    #随机选择一个低GC序列
    while 1:
        if len(dic_GC_low[key[a]]) >= len(j):  #如果低GC的长度大于高GC
            for i in dic_GC_low[key[a]]:
                list_GC_low.append(dic[i])
                if len(list_GC_low) < len(j):
                    pass
                else:
                    break

            break
        else:
            a = random.randrange(len(key))
    return list_GC_low

def GC_content(file):
    '''GC 含量'''
    lenth = len(file)
    C = file.count('C')
    G = file.count('G')
    CG = (int(C) + int(G)) / float(lenth)
    return CG

for s in species:
    filename_mt_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' mitochondrion' + '-HitTable.csv'
    filename_chl_hittable = 'C:\\Users\\ASUS\\Desktop\\hittable\\' + s + ' chloroplast' + '-HitTable.csv'
    filename_mt = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' mitochondrion' + '.fasta'
    filename_chl = 'C:\\Users\\ASUS\\Desktop\\organelle_data\\' + s + ' chloroplast' + '.fasta'

    dic = build_dic(filename_chl)  # 构建第n个是什么碱基的字典               #需替换1
    lenth = len(dic)  # 细胞器基因组长度
    # print lenth

    dicti = {}
    for i in range(1, lenth + 1):
        dicti[i] = 0
    q_range = get_range(filename_chl_hittable)  # 转移的细胞器基因组范围  #需替换2
    trans_lenth = []
    for i in q_range:
        for j in range(i[0], i[1]):  # 若在范围内，计数+1
            d = dicti[j]
            dicti[j] = d + 1
        trans_lenth.append(i[1] - i[0])   #转移的平均长度
    print numpy.mean(trans_lenth)

    files = open('C:\\Users\\ASUS\Desktop\\0220result.txt', 'w')  # 结果
    for i in range(1, len(dicti) + 1):
        files.write(str(dicti[i]) + '\n')
    files.close()


    list_trans = []
    for i in range(1, lenth + 1):
        list_trans.append(dicti[i])
    avg = numpy.mean(list_trans)
    print avg   #求平均值


    dic_GC_high = find_range_high()  # 找到连续片段
    dic_GC_low = find_range_low()


    ss = 0
    pp = []
    while ss < 10:              #需调整
        list_result_high = []
        list_result_low = []
        for (i, j) in dic_GC_high.items():  # 如果长度>100bp，计算GC含量
            if len(j) >= 100:  # 如果找到的转移大于平均值2倍的连续长度>100
                GC_list_high = []
                GC_list_low = []
                for k in j:  # 这个片段的AGTC序列
                    GC_list_high.append(dic[k])

                result_high = GC_content(GC_list_high)
                list_result_high.append(result_high)

                GC_list_low = GC_low()  # 随机找到一个长度>highGC的片段，返回ATCG序列
                result_low = GC_content(GC_list_low)  # 计算GC含量
                list_result_low.append(float(result_low))


        t, p = ttest_ind(list_result_high, list_result_low)
        #print p

        #print numpy.mean(list_result_high),numpy.mean(list_result_low)

        #pp.append(p)
        ss += 1

    #print numpy.mean(pp)

    files = open('C:\\Users\\ASUS\Desktop\\hirsutum chloroplast.txt', 'a')
    files.write('>[' + str(s) + ']' + '\n')
    for i in GC_list_high:
        files.write(str(i))
    files.write('\n')
    files.close()







