#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO:
# 1. read two excel file by row
# 2. loop excel one and store diff in a separate array
# 3. write 2 to a new excel
# 4. generate new excel

import pandas as pd
from numpy import array
from pprint import pprint


def get_excel(excel):
    return pd.read_excel(excel_file)


excel_file1 = './src/June_2018_Revenue_by_Shop.xlsx'
excel_file2 = './src/201806.xlsx'
df1 = pd.read_excel(excel_file1)
df2 = pd.read_excel(excel_file2)

df2_queried = df2.query('c1 == [u"TS初期",u"TSその他初期",u"TS機器"]')
data = {
    u'蠎苓・ID': [],
    u'c2': [],
    u'Initial': [],
    u'PAYG': [],
    u'Maitsuki': [],
    u'Nankagetsu': [],
    u'Total': []
}

for index, row in df2_queried.iterrows():
    compare1 = row[u"貸方金額"]
    code1 = str(row[u"c2"])
    df1_queried = df1.query('c2 == ["' + code1 + '"]')

    for index2, row2 in df1_queried.iterrows():
        compare2 = row["c2"]
        if compare2 != compare1:
            for key in data:
                if key == u'蠎苓・ID':
                    index3 = 0
                elif key == u'c2':
                    index3 = 1
                elif key == u'Initial':
                    index3 = 2
                elif key == u'PAYG':
                    index3 = 3
                elif key == u'Maitsuki':
                    index3 = 4
                elif key == u'Nankagetsu':
                    index3 = 5
                elif key == u'Total':
                    index3 = 6

                new = data[key].append(row2[index3])

# data_formatted = array(data)
# columns=[蠎苓・ID,c2,Initial,PAYG,Maitsuki,Nankagetsu,Total]
print data
df = pd.DataFrame(data)
writer = pd.ExcelWriter("./src/hoge1.xlsx")
df.to_excel(writer, sheet_name="hoge1", index=False)
workbook = writer.book
worksheet1 = writer.sheets['hoge1']

writer.save()
