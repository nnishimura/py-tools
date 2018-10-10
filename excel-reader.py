#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from numpy import array
from numpy import nan_to_num
from collections import OrderedDict
from pprint import pprint

# 1
# 取引先コードごとに、
# 201806のC列＝TS初期orTSその他初期orTS機器の
# G列の合計＝June_2018エクセルの
# C列Initialが一致するはずなので、
# 差分があればそのリスト欲しいです。
out = {
    u'取引先コード': [],
    u'取引先名': [],
    u'補助科目': [],
    u'Initial': [],
    u'貸方金額': []
}

target_excel = './src/initial/target.xlsx'
compare_excel = './src/initial/compare.xlsx'
df_target = pd.read_excel(target_excel)
df_compare = pd.read_excel(compare_excel)

df_target_queried = df_target.query('c2 == [u"TS初期",u"TSその他初期",u"TS機器"]')

for index, row in df_target_queried.iterrows():
    compare1 = 0
    code1 = str(row["c1"])
    df_target_matched = df_compare.query('c1 == ["' + code1 + '"]')
    for i, r in df_target_matched.iterrows():
        compare1 += nan_to_num(row[u"貸方金額"])

    df_compare_queried = df_compare.query('c1 == ["' + code1 + '"]')
    compare2 = 0
    for index2, row2 in df_compare_queried.iterrows():
        compare2 += nan_to_num(row2[u"Initial"])
    if compare2 != compare1:
        for key in out:
            if key == u'取引先コード':
                value = row[4]
            elif key == u'取引先名':
                value = row[5]
            elif key == u'補助科目':
                value = row[2]
            elif key == u'Initial':
                value = compare2
            elif key == u'貸方金額':
                value = compare1
            if row[4] not in out[u'取引先コード']:
                out[key].append(value)

df_out = pd.DataFrame(
    out,
    columns=[u'取引先コード', u'取引先名', u'補助科目', u'Initial', u'貸方金額']
)
writer = pd.ExcelWriter("./src/initial.xlsx")
df_out.to_excel(writer, sheet_name="initial", index=False)

writer.save()

# 2
# 取引先コードごとに、
# 201806のC列＝TS従量SMSorTS従量みせばんorTS従量CNPorTS従量CTIの
# G列の合計＝June_2018エクセルの
# D列PAYGが一致するはずなので、差分があればそのリスト欲しいです。
out = {
    u'取引先コード': [],
    u'取引先名': [],
    u'補助科目': [],
    u'PAYG': [],
    u'貸方金額': []
}

target_excel = './src/initial/target.xlsx'
compare_excel = './src/initial/compare.xlsx'
df_target = pd.read_excel(target_excel)
df_compare = pd.read_excel(compare_excel)

df_target_queried = df_target.query(
    'c2 == [u"TS従量SMS",u"TS従量みせばん",u"TS従量CNP",u"TS従量CTI"]'
)

for index, row in df_target_queried.iterrows():
    compare1 = row[u"貸方金額"]
    code1 = str(row["c1"])
    df_target_matched = df_compare.query('c1 == ["' + code1 + '"]')
    for i, r in df_target_matched.iterrows():
        compare1 += nan_to_num(row[u"貸方金額"])

    df_compare_queried = df_compare.query('c1 == ["' + code1 + '"]')
    compare2 = 0
    for index2, row2 in df_compare_queried.iterrows():
        compare2 += nan_to_num(row2[u"PAYG"])

    if compare2 != compare1:
        for key in out:
            if key == u'取引先コード':
                value = row[4]
            elif key == u'取引先名':
                value = row[5]
            elif key == u'補助科目':
                value = row[2]
            elif key == u'PAYG':
                value = compare2
            elif key == u'貸方金額':
                value = compare1
            if row[4] not in out[u'取引先コード']:
                out[key].append(value)

df_out = pd.DataFrame(
    out,
    columns=[u'取引先コード', u'取引先名', u'補助科目', u'PAYG', u'貸方金額']
)
writer = pd.ExcelWriter("./src/payg.xlsx")
df_out.to_excel(writer, sheet_name="payg", index=False)

writer.save()


# 3
# 取引先コードごとに、
# 201806のC列＝TS基本料金orTSOP月額orAPI保守費用の
# G列の合計＝June_2018エクセルのE列Maitsuki+F列Nankagetsuが一致するはずなので、差分があればそのリスト欲しいです。
# 取引先コードは、201806のエクセルはE列、June_2018のエクセルはB列です。
out = {
    u'取引先コード': [],
    u'取引先名': [],
    u'補助科目': [],
    u'Maitsuki + Nankagetsu': [],
    u'貸方金額': []
}

target_excel = './src/initial/target.xlsx'
compare_excel = './src/initial/compare.xlsx'
df_target = pd.read_excel(target_excel)
df_compare = pd.read_excel(compare_excel)

df_target_queried = df_target.query('c2 == [u"TS基本料金",u"TSOP月額",u"API保守費用"]')

for index, row in df_target_queried.iterrows():
    compare1 = row[u"貸方金額"]
    code1 = str(row["c1"])
    df_target_matched = df_compare.query('c1 == ["' + code1 + '"]')
    for i, r in df_target_matched.iterrows():
        compare1 += nan_to_num(row[u"貸方金額"])

    df_compare_queried = df_compare.query('c1 == ["' + code1 + '"]')
    compare2 = 0
    for index2, row2 in df_compare_queried.iterrows():
        total = nan_to_num(row2[u"Maitsuki"]) + nan_to_num(row2[u"Nankagetsu"])
        compare2 += total

    if compare2 != compare1:
        for key in out:
            if key == u'取引先コード':
                value = row[4]
            elif key == u'取引先名':
                value = row[5]
            elif key == u'補助科目':
                value = row[2]
            elif key == u'Maitsuki + Nankagetsu':
                value = compare2
            elif key == u'貸方金額':
                value = compare1
            if row[4] not in out[u'取引先コード']:
                out[key].append(value)

df_out = pd.DataFrame(
    out,
    columns=[u'取引先コード', u'取引先名', u'補助科目', u'Maitsuki + Nankagetsu', u'貸方金額']
)
writer = pd.ExcelWriter("./src/maitsuki.xlsx")
df_out.to_excel(writer, sheet_name="maitsuki", index=False)

writer.save()
