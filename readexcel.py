# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 15:03:53 2021

@author: chloe
"""

import xlrd
import json

def read_excel(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    
    
    s_rows = table.nrows  #获取表格行数
    s_cols = table.ncols  #获取表格列数
    
    slots = []

    titles = table.row_values(0)
    name = titles[0]
    major = titles[1]
    
    t = 1 

    for t in range(1,s_rows) : #空闲时间汇总
        values2= table.row_values(t)
        spare_data = dict(zip(titles,values2)) #把标题和单元格内容对应
        for key in list(spare_data.keys()):
            if spare_data.get(key):
                del spare_data[key]
                
            spare_slots=list(spare_data.keys())
            slots.append({name:values2[0],
                          major:values2[1],
                          'slots':spare_slots})
    
        t = t + 1
        
        
    new_file, form = filename.split('.')
    with open (new_file+'.json', mode = 'w', encoding='utf-8') as f:
        json.dump(slots, f)
    
    print('文件'+ new_file+'.json 已生成')



def generate_subject_list(file): # 生成一份科目列表 
    teacher_data = xlrd.open_workbook(file)
    table = teacher_data.sheets()[0]
    
    subjects_data = table.col_values(1, start_rowx=1, end_rowx = None)
    subjects_list = []
    
    for subject in subjects_data: #科目名称去重，然后生成列表
        if not subject in subjects_list:
            subjects_list.append(subject)
        
    with open('科目列表.json','w') as filename:
        json.dump(subjects_list, filename)    
        
    print('文件 科目列表.json  已生成')