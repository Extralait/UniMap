import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
import pickle

# d=[]
# pars=[]
# with open('list_to_csv.csv', "r") as f_obj:
#     reader=csv.reader(f_obj)
#     for i in reader:
#         pars.append(str(i[0]).split(','))
#         print(str(i[0]).split(','))
#
#
# def get_html(url,driver):
#     driver.get(url.format(url))
#     return driver.page_source
#
# d=[]
#
# def get_page_data(html,pars):
#     try:
#         sope=BeautifulSoup(html,'lxml')
#         ads = sope.find('div',class_='row row-small').find_all('div',class_='col-xs-6 col-sm-4 item')
#         for ad in ads:
#             # print(ad)
#             title=ad.find('a',class_='product-container-outer').find('div',class_='product-container-text has-rtl').find('i').text.strip()
#             price = ad.find('a', class_='product-container-outer').find('div',class_='product-container-text has-rtl').find('b').get_text()
#             price = re.sub("\D", "",price)[:-2]
#             img = ad.find('a', class_='product-container-outer').find('div',class_='product-container picture-contain')['style']
#             pattern = "(?:\(['\"]?)(.*?)(?:['\"]?\))"
#             img = re.search(pattern, img).group(1)
#             full=[title, price, img]
#             full.extend(pars)
#             d.append(full)
#             print(full)
#     except AttributeError: return False
#
# driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver')
# for pars in pars:
#     print(pars[0])
#     get_page_data(get_html(pars[0],driver),pars[1:])
# driver.quit()
#
#
#
# with open('data.pickle', 'wb') as f:
#      pickle.dump(d, f)

with open('data.pickle', 'rb') as f:
   data_new = pickle.load(f)

new_data=[]
for row in data_new:
    new_str=';'.join(row)
    new_str=new_str.replace('"',"'")
    new_data.append(new_str)

with open('list_to_csv_final.csv', 'w', newline='') as csv_file_link:
    csv_writer = csv.writer(csv_file_link)
    for item in new_data:
        csv_writer.writerow([item])

#
# xls = pd.read_csv('list_to_csv_final.csv',encoding='utf-8')
# print(xls.head(50))
# xls.to_csv("output.csv", index=False,encoding='utf-8')