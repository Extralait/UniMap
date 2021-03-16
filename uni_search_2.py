from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import pickle
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait


def get_html(url, driver,on_click=False):
    sleep(1)
    driver.get(url.format(url))
    if on_click==True:
        elements=driver.find_elements_by_link_text('Показать больше данных')
        for elem in elements:
            elem.click()
        html = driver.page_source
    else:
        WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        html=driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('title').get_text()=='429 Too Many Requests':
        return get_html(url, driver)
    else:
        return html


def get_uni_town_links(html):
    link_container = []
    soup = BeautifulSoup(html, 'lxml')
    town_sections = soup.find_all('section')[1:]
    for section in town_sections:
        region = section.find('b').get_text()
        towns = section.find_all('a')
        for town in towns:
            town_name = town.get_text()
            town_link = town.get('href')
            link_container.append([region, town_name, town_link])
    return link_container


def get_uni_links(html):
    link_container = []
    soup = BeautifulSoup(html, 'lxml')
    unis = soup.find_all('p', class_='unit-name')
    for uni in unis:
        link = uni.find('a').get('href')
        title = uni.find('a').get_text()
        link_container.append((link, title))
    return link_container


def button_check_and_get_link(html,sub_link):
    soup = BeautifulSoup(html, 'lxml')
    try:
        button = soup.find_all('a', class_='btn center-block')
        print(button)
    except AttributeError:
        return (False,)
    if len(button) == 1 and button[0].get_text() == 'Назад':
        return (False,)
    elif len(button) == 2:
        return True,sub_link  + button[-1].get('href')
    elif len(button) == 1 and button[0].get_text() == 'Далее':
        return True, sub_link + button[0].get('href')

    else:
        return (False,)

def get_contacts_and_quantity(html):
    soup = BeautifulSoup(html, 'lxml')
    contacts_container=soup.select_one('#general').find('div',class_="row contacts")
    try:
        site=contacts_container.select_one('p.myIcon.leftIcon.site a').get('href')
    except AttributeError:site=''
    try:
        e_mail=contacts_container.select_one('p.myIcon.leftIcon.email').get_text()
    except AttributeError:e_mail=''
    try:
        number=contacts_container.select_one('div.phone a').get('href')[4:]
    except AttributeError:number=''
    try:
        quantity=soup.select_one('tbody tr:nth-child(6) td:nth-child(2)').get_text()
    except AttributeError:quantity=''
    try:
        common_information=soup.select_one('#general p:nth-child(2)').get_text()
    except AttributeError:common_information=''
    try:
        middle_score=soup.select_one('tbody tr:nth-child(3) td:nth-child(2)').get_text()
        if middle_score=='-':
            middle_score=''
    except AttributeError:middle_score=''
    return (number,site,e_mail,quantity,middle_score,common_information)

all_uni=[]

def main():
    url = "https://vuz.edunetwork.ru/cities"
    base_url = "https://vuz.edunetwork.ru"
    option = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
    option.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver',options=option)
    town_container = [['Москва', 'Москва', '/77/?']] + [['Санкт-Петербург', 'Санкт-Петербург',
                                                       '/78/?']] + get_uni_town_links(get_html(url, driver))

    for region, town, town_link in town_container:
        town_url = base_url + town_link
        button_check = (True, town_url)
        html_town=get_html(town_url,driver)
        while button_check[0] == True:
            unis = get_uni_links(html_town)
            button_check = button_check_and_get_link(html_town,town_link[:-1])
            if button_check[0] == True:
                town_url = base_url + button_check[1]
                html_town = get_html(town_url, driver)
            for uni_link, uni_name in unis:
                uni_url = base_url + uni_link + '#'
                number,site,e_mail,quantity,middle_score,common_information=get_contacts_and_quantity(get_html(uni_url, driver,True))
                all_uni.append([region, town,uni_name,number,site,e_mail,quantity,middle_score,common_information])

    with open('pickle/uni_base_2.pickle', 'wb') as f:
         pickle.dump(all_uni, f)
    driver.quit()


if __name__ == '__main__':
    main()

with open('pickle/uni_base_2.pickle', 'rb') as f:
   data_new = pickle.load(f)

data_new=pd.DataFrame(data_new,columns=['Регион','Город','Вуз','Номер','Сайт','Почта','Студенты','Средний балл','Общая информация'])
data_new=data_new.applymap(lambda x:'' if x=='—' else x)

with open('pickle/uni_base_2.pickle', 'wb') as f:
   pickle.dump(data_new, f)
