from selenium import webdriver
import pickle

with open('pickle/uni_base_2.pickle', 'rb') as f:
   data_new = pickle.load(f)

data_new['Адрес']=data_new['Регион']+' '+data_new['Город']+' '+data_new['Вуз']
print(data_new['Адрес'])

data_new['Url'] = ['https://www.google.com/maps/search/' + i for i in data_new['Адрес']]

Url_With_Coordinates = []

option = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
option.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome("C:\\Users\\Валера\\Desktop\\chromedriver", options=option)

for url in data_new['Url']:
    driver.get(url)
    Url_With_Coordinates.append(driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
driver.close()

# with open('csv_files/Url_With_Coordinates.csv', 'r') as f:
#     reader = csv.reader(f, delimiter=',')
#     for i in reader:
#         Url_With_Coordinates = i
#         break

data_new['Url_With_Coordinates'] = Url_With_Coordinates
data_new = data_new[data_new.Url_With_Coordinates.str.contains('&zoom=')].copy()

data_new['lat'] = [ url.split('?center=')[1].split('&zoom=')[0].split('%2C')[0] for url in data_new['Url_With_Coordinates'] ]
data_new['long'] = [url.split('?center=')[1].split('&zoom=')[0].split('%2C')[1] for url in data_new['Url_With_Coordinates'] ]

with open('pickle/data_uni_2_final.pickle', 'wb') as f:
   pickle.dump(data_new, f)

with open('pickle/data_uni_2_final.pickle', 'rb') as f:
   data_new = pickle.load(f)

print(data_new)

data_new.to_csv("csv_files/output_uni_2_final.csv",
          sep = ";")