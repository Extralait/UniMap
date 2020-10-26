import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
import pickle

xls = []

with open('list_to_csv_final_final.csv', "r",encoding='utf-8') as f_obj:
    reader=csv.reader(f_obj)
    for i in reader:
        new_row=str(i[0]).split(';')
        for i,el in enumerate(new_row):
            if el == '':
                del(new_row[i])
        xls.append(new_row)

last_sort_1=0
last_sort_2 =0
last_sort_3 = 0
last_sort_4 =0
last_sort_5 = 0
new_xls=[]
start_ex_id=10000000000
start_parent_id=10000000000
first=True
for row in xls:
    if first ==True:
        first=False
        continue
    try:
        sort_1 = row[5]
    except IndexError: sort_1=''
    try:
        sort_2 = row[6]
    except IndexError: sort_2=''
    try:
        sort_3 = row[7]
    except IndexError: sort_3=''
    try:
        sort_4 = row[8]
    except IndexError: sort_4=''
    try:
        sort_5 = row[9]
    except IndexError: sort_5=''

    if sort_1 and sort_1 !=last_sort_1:
        new_xls.append([start_ex_id,'',sort_1])
        start_ex_id+=1
        last_sort_1=sort_1
    if sort_2 and sort_2 !=last_sort_2:
        new_xls.append([start_ex_id,start_parent_id,sort_2])
        start_ex_id+=1
        start_parent_id+=1
        last_sort_2 = sort_2
    if sort_3 and sort_3 !=last_sort_3:
        new_xls.append([start_ex_id,start_parent_id,sort_3])
        start_ex_id+=1
        start_parent_id+=1
        last_sort_3 = sort_3
    if sort_4 and sort_4 !=last_sort_4:
        new_xls.append([start_ex_id,start_parent_id,sort_4])
        start_ex_id+=1
        start_parent_id+=1
        last_sort_4 = sort_4
    if sort_5 and sort_5 !=last_sort_5:
        new_xls.append([start_ex_id,start_parent_id,sort_5])
        start_ex_id+=1
        start_parent_id+=1
        last_sort_5 = sort_5
    new_xls.append([start_ex_id,start_parent_id,row[2],row[3],row[4]])
    start_ex_id += 1

new_data=[]

for row in new_xls:
    row = [*map(str,row)]
    new_str=','.join(row)
    new_data.append(new_str)

with open('nu_posmotrim.csv', 'w', newline='') as csv_file_link:
    csv_writer = csv.writer(csv_file_link)
    for item in new_data:
        csv_writer.writerow([item])
