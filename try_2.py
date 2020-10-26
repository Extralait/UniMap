import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
import pickle

# def get_html(url,driver):
#     driver.get(url.format(url))
#     return driver.page_source
#
#
# def get_pages(html):
#     soup = BeautifulSoup(html, 'lxml')
#
#     pages = soup.find_all('a', class_='button btn-link btn-link-styled block-link')
#     all_pages=[]
#     for page in pages:
#         link=page.find('div',class_='btn-link-title').get_text()
#         link = re.sub(r'[^А-Яа-я ]', '', link)
#         page=page.get('href')
#         all_pages.append((page,link))
#
#     return all_pages
#
# def main():
#     url = "https://glorygoal.ru/p/10ecaa/"
#     base_url = "https://glorygoal.ru"
#
#     # total_pages = get_total_pages(get_html(url))
#     driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver')
#     url_case=set()
#     def sub_main(url,base_url,driver,url_case,link_list):
#         url_case_back=url_case.copy
#         for pages, link in set(get_pages(get_html(url,driver))):
#             local_link_list=link_list.copy()
#             local_link_list.append(link)
#             if pages in ['/','/p/1eb1b3/','/p/138b2d/','/NaN/'] or len(pages)>12:
#                 continue
#             # print(pages)
#             url_gen = base_url  + str(pages)
#             if len(local_link_list)>2:
#                 local_link_list=local_link_list[1:]
#             local_link_list.insert(0, url_gen)
#             print(local_link_list)
#             url_case.add(tuple(local_link_list))
#             sub_main(url_gen, base_url, driver, url_case,local_link_list)
#         if url_case_back==url_case:
#             return False
#     sub_main(url,base_url,driver,url_case,link_list=[])
#     driver.quit()
#     with open('data.pickle', 'wb') as f:
#          pickle.dump(url_case, f)
    # with open('list_to_csv.csv', 'w', newline='') as csv_file_link:
    #     csv_writer = csv.writer(csv_file_link)
    #     for item in [*map(list,list(url_case))]:
    #         csv_writer.writerow([item])


# if __name__ == '__main__':
#     main()

# d=[]
# pars=[]
# with open('list_to_csv.csv', "r") as f_obj:
#     reader=csv.reader(f_obj)
#     for i in reader:
#         pars.append(i)


# def get_html(url,driver):
#     driver.get(url.format(url))
#     return driver.page_source
#
# d=[]
#
# def get_page_data(html):
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
#             d.append([title, price, img])
#             print([title, price, img])
#     except AttributeError: return False
#
# driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver')
# for pars in pars:
#     get_page_data(get_html(pars[0],driver))
# driver.quit()
#
#
# d=np.array(d)
# with open('data.pickle', 'wb') as f:
#      pickle.dump(d, f)
#
# with open('data.pickle', 'rb') as f:
#    data_new = pickle.load(f)
#
# data_new=pd.DataFrame(data_new,columns=['Товар','Цена','Картинка'])
# print(data_new)
# data_new.to_csv("output.csv", index=False,encoding='utf-8')


with open('data.pickle', 'rb') as f:
   data_new = pickle.load(f)

new_data=[]
for row in data_new:
    new_str=','.join(row)
    new_data.append(new_str)



with open('list_to_csv.csv', 'w', newline='') as csv_file_link:
    csv_writer = csv.writer(csv_file_link)
    for item in new_data:
        csv_writer.writerow([item])