# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 16:59:26 2021

@author: chloe
"""


import json

with open('科目列表2.json','r') as file:
    subjects_list = json.load(file)
        
with open('教师数据.json','r') as f:
    teachers_data = json.load(f)
    
with open('学生数据6(humanities).json', 'r') as file:
    students_data = json.load(file)


def generate_teacher_list(listname,subject_tomatch): 
    tomatch_list = []
    for personal_data in listname:
        subject = personal_data['Subject']
        if subject == subject_tomatch:
            tomatch_list.append(personal_data)
    with open('老师列表-'+subject_tomatch+'.json','w') as file:
        json.dump(tomatch_list,file)
            
def generate_student_list(listname,subject_tomatch):
    tomatch_list = []
    for personal_data in listname:
        subject = personal_data['Major']
        if subject == subject_tomatch:
            tomatch_list.append(personal_data)
    with open('学生列表-'+subject_tomatch+'.json','w') as file:
        json.dump(tomatch_list,file)
    

def groupby_subject(): # 按学科对老师和学生进行分组，生成json文件
    n = 0
    while n < 5:
        subject_tomatch = subjects_list[n]
        
        generate_teacher_list(teachers_data,subject_tomatch)
        generate_student_list(students_data,subject_tomatch)        
                 
        n = n + 1
      
def play_subjectlist(): #展示学科列表
    for n in range(len(subjects_list)):
        subject = subjects_list[n]
        print('#编号',n+1,'-', subject)

             
def select_subject(subjects_list): # 选择一个学科
    content = input('请输入准备进行匹配的科目编号：')
    if content == 'over':
        print('科目选择结束')
        tomatch_subject = ''
    else:
        subject_no = int(content)
        tomatch_subject = subjects_list[subject_no - 1]
    
    return tomatch_subject



def open_student_candidatelist(tomatch_subject): #打开所选学科的学生列表
    filename = '学生列表-' + tomatch_subject+'.json'     
    with open (filename,'r') as file:
        student_candidatelist = json.load(file)
    print('待匹配学生数：',len(student_candidatelist))
    return student_candidatelist



def renew_student_candidatelist(tomatch_subject,renewed_student_list): #更新学生列表的json文件
    filename = '学生列表-' + tomatch_subject+'.json'  
    with open(filename, 'w') as file:
        json.dump(renewed_student_list,file)
    
    
def open_teacher_list(tomatch_subject): #打开所选学科的老师列表
    filename = '老师列表-'+tomatch_subject+'.json'
    with open(filename,'r') as file:
        teacher_list = json.load(file)
    
    
    for no in range(len(teacher_list)):
        teacher_tomatch_personal = teacher_list[no]
        teacher_tomatch_name = teacher_tomatch_personal['Initials']
        print('#编号',no+1,'- ',teacher_tomatch_name)
    return teacher_list


def renew_teacher_list(tomatch_subject,renewed_teacher_list): #更新老师列表的json文件
    filename = '老师列表-' + tomatch_subject+'.json'  
    with open(filename, 'w') as file:
        json.dump(renewed_teacher_list,file)

    
def generate_student_personal(student_candidatelist, it):
    student_tomatch_personal = student_candidatelist[it]
    student_id = student_tomatch_personal['ID']
    student_tomatch_slots = student_tomatch_personal['student_slots']
    student_personal = {'ID':student_id, 'slots':student_tomatch_slots}
    return student_personal


def find_match_slots(student_candidatelist,teacher_group_slots): #将A、B老师的空闲时间段与每个学生匹配
    candidate_students = []
    it = 0
    while it < len(student_candidatelist): 
        student_tomatch_personal = generate_student_personal(student_candidatelist, it)
        student_tomatch_slots = student_tomatch_personal['slots']
        student_id = student_tomatch_personal['ID']
        student_teacher_match = []
        student_teacher_match_result = []
        for match_student_slot in student_tomatch_slots:
            for teacher_result_slot in teacher_group_slots:
                if match_student_slot == teacher_result_slot:
                    student_teacher_match.append(match_student_slot)
    
        for get_match in student_teacher_match:
            if get_match not in student_teacher_match_result:
                student_teacher_match_result.append(get_match)
        
        if len(student_teacher_match_result) > 0:
            candidate_students.append({'ID':student_id,'slots':student_teacher_match_result})
        
        it = it + 1     
        

    return candidate_students
    
    

def input_person_toremove(): # 删去已匹配好的人，学生为ID（数字），老师为姓名缩写（字符串），
     person_to_remove = []
     var = 1
     while var == 1:
        remove_initials = input('请输入：')
        if remove_initials == 'over':
            print('录入结束')
            break
        else:
            person_to_remove.append(remove_initials)
     
     return person_to_remove

    
def for_id(list_name): #将输入的ID转化为数字
    id_list = []
    for i in list_name:
        t = int(i)
        id_list.append(t)
     
    return id_list
        
    
def remove_matched(person_to_remove,list_name,key): #将已匹配的人从备选列表中除去
    tt = len(list_name) - 1
        
    while tt > -1:
        available = list_name[tt]
        individual = available[key]
        for i in person_to_remove:
            if i == individual:
                list_name.pop(tt)
        tt = tt - 1      
    
    return list_name


def select_teacher(): # 指定一名老师
   input_content = input('请输入老师的编号：')
   if input_content == 'over':
       print('老师分组结束')
       match_no = ''
   else:
       match_no = int(input_content)
       
   return match_no

def list_selected_teacher(list_name): # 得到指定老师的资料（首字母缩写和空闲时间段集合）
    match1 = select_teacher()
    selected_teacher = list_name[match1-1]
    
    return selected_teacher

def find_groupedteacher_slots(teacher_A, teacher_B): #找出指定老师A和老师B重合的空闲时间段
    teacher_group_match = []
    teacher_group_result = []

    for slot_A in teacher_A['Slots']: 
        for slot_B in teacher_B['Slots']:
            if slot_A == slot_B:
                teacher_group_match.append(slot_A)

    for match_slot in teacher_group_match: #去重
        if match_slot not in teacher_group_result:
            teacher_group_result.append(match_slot)

    return teacher_group_result



def display_selected_teacher(teacher_A,teacher_B,groupedteacher_slots): #展示指定老师A和B的信息
    print('')
    print('当前成组老师：', teacher_A['Initials'], '+', teacher_B['Initials'])
    print('该组可用空闲时段数：', len(groupedteacher_slots))
    for result_slot in groupedteacher_slots:
        print(result_slot)

def input_instruction_student(): # 删去已匹配学生时展示的文字说明
    print('')
    print('请记录下所有达成匹配的学生，下面将依次录入他们的ID，避免程序重复提供')
    print('1.每次输入一个ID；')
    print('2.输入over结束。')
    
def input_instruction_teacher(): # 删去已匹配老师时展示的文字说明
    print('')
    print('请记录下已参与6次的老师，下面将依次录入他们的首字母缩写，避免程序重复提供')
    print('1.每次输入一个缩写；')
    print('2.输入over结束。')

def display_matched_results(teacher_A,teacher_B,person_to_remove): #【完成匹配后】展示当前成组老师的匹配结果列表
    print('')
    print("当前成组老师：", teacher_A['Initials'], '+', teacher_B['Initials']) 
    print('匹配学生总数：', len(person_to_remove))
    print('达成匹配的学生为：')
    for rem in person_to_remove:
        print(rem)

def display_candidate_student(candidate_students): # 【匹配候选列表】一一列出跟当前成组老师空闲时间段重合的学生及信息
    print('')
    print('可选学生数：',len(candidate_students))
    for i in candidate_students:
        matched_slots = i['slots']
        print('')
        print ("可选学生ID:", i['ID'])
        print ("该学生可选时间段总数：",len(matched_slots))
        for result in matched_slots:
            print(result)
            

def round2_input_student_toremove(): # 【显示说明+录入删去的学生名单】
    input_instruction_student()
    student_to_remove = input_person_toremove()
    '''student_to_remove = for_id(person_to_remove)'''
    return student_to_remove


def round2_input_teacher_toremove(): # 【显示说明+录入删去的老师名单】
    input_instruction_teacher()
    teacher_to_remove = input_person_toremove()    
    
    return teacher_to_remove



def round2_match(tomatch_subject): # 【汇总型函数】- 打开文件，进行匹配，更新文件
    student_list = open_student_candidatelist(tomatch_subject)
    teacher_list = open_teacher_list(tomatch_subject)
    if len(student_list) == 0:
        print('没有待匹配的学生啦') # to-do 这里可以做一个说明函数 --“学科xx已匹配完毕”
    if len(student_list) > 0:
        print('输入老师A的编号')
        teacher_A = list_selected_teacher(teacher_list)
        print('输入老师B的编号')
        teacher_B = list_selected_teacher(teacher_list)
        #找到所选的两位老师的重合空闲时间段
        teacher_group_slots = find_groupedteacher_slots(teacher_A, teacher_B)
        #展示所有空闲时间段
        display_selected_teacher(teacher_A,teacher_B,teacher_group_slots)
        #将老师的重合空闲时间段与学生一一比对，找到二者的重合时间段，生成匹配候选列表
        candidate_students = find_match_slots(student_list,teacher_group_slots)
        #展示匹配候选列表
        display_candidate_student(candidate_students)
        #手动输入匹配好的学生id以删去
        students_to_remove = round2_input_student_toremove()
        #展示所有输入的id
        display_matched_results(teacher_A,teacher_B,students_to_remove)
        #更新学生列表，写入json文件
        renewed_student_list = remove_matched(students_to_remove,student_list,'ID')
        renew_student_candidatelist(tomatch_subject,renewed_student_list)
        #手动输入已匹配6场的老师以删去
        teacher_to_remove = round2_input_teacher_toremove()
        #更新老师列表，写入json文件
        renewed_teacher_list = remove_matched(teacher_to_remove,teacher_list,'Initials')
        renew_teacher_list(tomatch_subject,renewed_teacher_list)



def round2_match_ver2(student_list,teacher_list,tomatch_subject): # 【汇总型函数】- 打开文件，进行匹配，更新文件
        print('输入老师A的编号')
        teacher_A = list_selected_teacher(teacher_list)
        print('输入老师B的编号')
        teacher_B = list_selected_teacher(teacher_list)
        #找到所选的两位老师的重合空闲时间段
        teacher_group_slots = find_groupedteacher_slots(teacher_A, teacher_B)
        #展示所有空闲时间段
        display_selected_teacher(teacher_A,teacher_B,teacher_group_slots)
        #将老师的重合空闲时间段与学生一一比对，找到二者的重合时间段，生成匹配候选列表
        candidate_students = find_match_slots(student_list,teacher_group_slots)
        #展示匹配候选列表
        display_candidate_student(candidate_students)
        #手动输入匹配好的学生id以删去
        students_to_remove = round2_input_student_toremove()
        #展示所有输入的id
        display_matched_results(teacher_A,teacher_B,students_to_remove)
        #更新学生列表，写入json文件
        renewed_student_list = remove_matched(students_to_remove,student_list,'ID')
        renew_student_candidatelist(tomatch_subject,renewed_student_list)
        #手动输入已匹配6场的老师以删去
        teacher_to_remove = round2_input_teacher_toremove()
        #更新老师列表，写入json文件
        renewed_teacher_list = remove_matched(teacher_to_remove,teacher_list,'Initials')
        renew_teacher_list(tomatch_subject,renewed_teacher_list)



            
    
var = 1
while var == 1 :
    play_subjectlist()
    tomatch_subject = select_subject(subjects_list)
    if tomatch_subject == '':
        break
    else:
        while var == 1:
            student_list = open_student_candidatelist(tomatch_subject)
            teacher_list = open_teacher_list(tomatch_subject)
            if len(student_list) == 0:
                print('没有待匹配的学生啦') 
                break
            else:   # To-do:选择老师时可以再做一次条件判断，允许输入over结束
                round2_match_ver2(student_list,teacher_list,tomatch_subject)
