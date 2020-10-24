import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
import pickle

def get_html(url,driver):
    driver.get(url.format(url))
    return driver.page_source


def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find_all('a', class_='button btn-link btn-link-styled block-link')
    all_pages=[]
    for page in pages:
        page=page.get('href')
        all_pages.append(page)
    return all_pages

def main():
    url = "https://glorygoal.ru/p/10ecaa/"
    base_url = "https://glorygoal.ru"

    # total_pages = get_total_pages(get_html(url))
    driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver')
    url_case=set()
    def sub_main(url,base_url,driver,url_case):
        url_case_back=url_case.copy
        for pages in set(get_pages(get_html(url,driver))):
            if pages in ['/','/p/1eb1b3/','/p/138b2d/','/NaN/'] or len(pages)>12:
                continue
            print(pages)
            url_gen = base_url  + str(pages)
            url_case.add(url_gen)
            sub_main(url_gen, base_url, driver, url_case)
        if url_case_back==url_case:
            return False
    sub_main(url,base_url,driver,url_case)
    driver.quit()
    with open('list_to_csv.csv', 'w', newline='') as csv_file_link:
        csv_writer = csv.writer(csv_file_link)
        for item in list(url_case):
            csv_writer.writerow([item])


if __name__ == '__main__':
    main()

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

with open('data.pickle', 'rb') as f:
   data_new = pickle.load(f)

data_new=pd.DataFrame(data_new,columns=['Товар','Цена','Картинка'])
print(data_new)
data_new.to_csv("output.csv", index=False,encoding='utf-8')
