from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import pickle


from selenium.webdriver.support.ui import WebDriverWait

def get_html(url,driver):
    driver.get(url.format(url))
    WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    return driver.page_source

def get_uni_category_links(html):
    link_container=[]
    soup = BeautifulSoup(html, 'lxml')
    category_links = soup.find_all('a', class_='lintspecmenu')[1:]
    for link in category_links:
        link_container.append((link.get('href'),link.find('div', class_='specspec').get_text()))
    return link_container

def get_uni_links(html):
    link_container=[]
    soup = BeautifulSoup(html, 'lxml')
    unis=soup.find_all('div',class_='col-md-12 itemVuz')
    for uni in unis:
        # print(uni)
        # print(uni.find('div', class_='itemVuzTitle'))
        link=uni.find('a').get('href')
        title=uni.find('a').find('div').get_text().replace('\n','').replace('                        ','').replace('    ','')
        # print([title])
        # print(link,title)
        link_container.append((link,title))
    # print(link_container)
    return link_container


def button_check_and_get_link(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(len(html))
    # print(soup)
    try:
        button = soup.find('div',class_='pagpag').find('ul', class_='pagination').find_all('span', class_='material-icons')
        # button = soup.find_all('span', class_='material-icons')
    except AttributeError: return (False,)
    # print(button)
    if len(button)==1 and button[0].get_text()=='keyboard_arrow_left':
        return (False,)
    elif len(button)==2 or (len(button)==1 and button[0].get_text())=='keyboard_arrow_right':
        all_buttons=soup.find('ul',class_='pagination').find_all('a')
        # print('/vuz'+all_buttons[-1].get('href'))

        return True,'/vuz'+all_buttons[-1].get('href')
    else:
        # print(button)
        # print('че ха хуета, я не понял?')
        return (False,)


def get_uni_place(html):
    soup = BeautifulSoup(html, 'lxml')
    place = soup.find('div', class_='col-lg-6 col-md-6 col-xs-12 col-sm-6').find_all_next('div')[5].get_text()
    email = soup.find('div', class_='col-lg-6 col-md-6 col-xs-12 col-sm-6').find_all_next('div')[8].get_text()
    number = soup.find('div', class_='col-lg-6 col-md-6 col-xs-12 col-sm-6').find_all_next('div')[2].get_text()
    site = soup.find('div', class_='col-lg-6 col-md-6 col-xs-12 col-sm-6').find_all_next('div')[9].get_text()
    # print(site)
    if 'http' in site:
        while site[:4]!='http':

            site=site[1:]
        site=site[:-1]
    else:
        site = site[:-1]
        site.replace(' ','').replace('Сайт','')

    return place,email,number,site

all_uni=[]

def main():
    url = "https://vuzopedia.ru/vuz/"
    base_url = "https://vuzopedia.ru"
    driver = webdriver.Chrome('C:\\Users\\Валера\\Desktop\\chromedriver')

    all_category=get_uni_category_links(get_html(url,driver))
    for category in all_category:
        category_name=category[1]
        url_gen = base_url + category[0]
        html_category=get_html(url_gen,driver)
        button_check=(True,category[0])
        while button_check[0]==True:
            print(url_gen)
            unis = get_uni_links(html_category)
            button_check = button_check_and_get_link(html_category)
            if button_check[0]==True:
                url_gen = base_url + button_check[1]
                html_category = get_html(url_gen, driver)
            # print(unis)
            for uni in unis:
                title = uni[1]
                url_gen_uni = base_url + uni[0]
                # print(1,end='')
                html_uni = get_html(url_gen_uni, driver)
                # print(1, end='')
                place,email,number,site = get_uni_place(html_uni)
                # print(1, end='')
                all_uni.append([category_name,title,place,email,number,site])
                print([category_name,title,place,email,number,site])

    with open('pickle/data.pickle', 'wb') as f:
         pickle.dump(all_uni, f)
    driver.quit()

if __name__ == '__main__':
    main()

with open('pickle/data.pickle', 'rb') as f:
   data_new = pickle.load(f)

data_new=pd.DataFrame(data_new,columns=['Категория','Вуз','Адрес','e-mail','Телефон','Сайт'])
# print(data_new)
data_new['Категории']=data_new.groupby(by=['Вуз'])['Категория'].transform(lambda x: ','.join(x.values))
del data_new['Категория']
data_new=data_new.sort_values('Вуз')
data_new=data_new.drop_duplicates()
data_new=data_new.reset_index()
del data_new['index']
print(data_new)

with open('pickle/data_final.pickle', 'wb') as f:
   pickle.dump(data_new, f)