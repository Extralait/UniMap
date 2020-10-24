import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
import pickle

d=[]
pars=[]
with open('list_to_csv.csv', "r") as f_obj:
    reader=csv.reader(f_obj)
    for i in reader:
        pars.append(i)


def get_html(url,driver):
    driver.get(url.format(url))
    return driver.page_source

d=[]

def get_page_data(html):
    try:
        sope=BeautifulSoup(html,'lxml')
        ads = sope.find('div',class_='row row-small').find_all('div',class_='col-xs-6 col-sm-4 item')
        for ad in ads:
            # print(ad)
            title=ad.find('a',class_='product-container-outer').find('div',class_='product-container-text has-rtl').find('i').text.strip()
            price = ad.find('a', class_='product-container-outer').find('div',class_='product-container-text has-rtl').find('b').get_text()
            price = re.sub("\D", "",price)[:-2]
            img = ad.find('a', class_='product-container-outer').find('div',class_='product-container picture-contain')['style']
            pattern = "(?:\(['\"]?)(.*?)(?:['\"]?\))"
            img = re.search(pattern, img).group(1)
            d.append([title, price, img])
            print([title, price, img])
    except AttributeError: return False

driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver')
for pars in pars:
    get_page_data(get_html(pars[0],driver))
driver.quit()


d=np.array(d)
with open('data.pickle', 'wb') as f:
     pickle.dump(d, f)




