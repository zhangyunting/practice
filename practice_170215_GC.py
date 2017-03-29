#coding:utf8
import re
def build_diction(files):   #构建第n个是什么碱基的字典
    genomoall = []
    for i in files.readlines():
        genomo = re.findall(r'[A-Z]', i)
        genomoall = genomoall + genomo
    diction = {}
    for i in range(1,lenth2+1):
        diction[i] = genomoall[i-1]
    return diction

def lenth2_count(files):   #细胞器基因组长度
    genomoall = []
    for i in files.readlines():
        genomo = re.findall(r'[A-Z]', i)
        genomoall = genomoall + genomo
    #print genomoall
    lenth = len(genomoall)
    return lenth

def CG(file):
    lenth = len(file)
    CC = re.findall(r'C',file)
    lenthC = len(CC)
    GG = re.findall(r'G', file)
    lenthG = len(GG)
    CG = (int(lenthC) + int(lenthG)) / float(lenth)
    print str(lenthC) + '+' + str(lenthG) + '/' + str(lenth) + '=' + str(CG)


files = open('C:\\Users\\ASUS\Desktop\\hirsutum chloroplast.txt')
lenth2 = lenth2_count(files)
print lenth2
files.close()

file2 = open('C:\\Users\\ASUS\Desktop\\hirsutum chloroplast.txt')
dic = build_diction(file2)


diction = {
'a0':1,
'a1':88815,
'a2':114406,
'a3':134837,
'a4':int(lenth2)

}

for i in range(4):
    rangebegin = diction[str('a' + str(i))]
    rangedend = diction[str('a' + str(i+1))]
    area = ''
    for j in range(rangebegin,rangedend):
        area = area + dic[j]
    print rangebegin,rangedend
    CG(area)

