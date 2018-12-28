#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 23:30 2017/11/7 

@author: acer
'''
import xlrd
import re
import sqlite3

def read_xlsx():
    workbook = xlrd.open_workbook('kuaidi.xlsx')
    booksheet = workbook.sheet_by_name('1')
    p = list()
    for row in range(booksheet.nrows):
        row_data = []
        for col in range(booksheet.ncols):
            cel = booksheet.cell(row, col)
            val = cel.value
            try:
                val = cel.value
                val = re.sub(r'\s+', '', val)
            except:
                pass

            if type(val) == float:
                val = int(val)
            else:
                val = str(val)
            row_data.append(val)
        p.append(row_data)
    return p


def operat_sqlite(*data):
    # print(type(data))
    # print(data)
    # print(data[0])
    try:
        conn = sqlite3.connect('D:/Pythonwork/blogproject/blogproject/db.sqlite3')
    except:
        print('open sqlite3 failed.')
        return
    else:  # 操作数据库
        c = conn.cursor()
        for item in data:
            for obj in item:
                try:
                    name = obj[0]
                    alias = obj[1]
                    print(name,alias)
                    c.execute("insert into weixin_express (name, alias) values (?,?)",
                              (name,alias))
                    conn.commit()
                except:
                    print('insert roadky failed ')
                    pass
        conn.close()

    return

if __name__ == '__main__':
    p=read_xlsx()
    print(type(p))
    # print(p)
    import json
    print(json.loads(p))
    # operat_sqlite(p)