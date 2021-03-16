import pickle

from folium import GeoJsonTooltip, GeoJsonPopup
from folium.plugins import MarkerCluster
import folium
import json
import pandas as pd
import pprint
import geojson

with open('pickle/data_final_2.pickle', 'rb') as f:
    data_new = pickle.load(f)

data_new_json = pd.read_csv('csv_files/output_uni_2_final.csv', encoding='utf-8 ', sep=';')
data_new_2 = data_new_json.copy()
category_list = ['Авиационные', 'Аграрные', 'Архитектурные', 'Биологические', 'ФСБ', 'Военные', 'Вузы культуры',
                 'Гуманитарные', 'Дизайна', 'Информационные', 'Географические', 'Экономические', 'МВД', 'Медицинские',
                 'МЧС', 'Педагогические', 'Сервиса', 'Спортивные', 'Строительные', 'Технические', 'Нефтяные',
                 'Психологические', 'Транспортные', 'Пищевые', 'Юридические', 'Все']
color_list = ['lightred', 'red', 'cadetblue', 'black', 'darkpurple', 'pink', 'beige', 'gray', 'darkblue', 'orange',
              'lightblue', 'lightgreen', 'lightgray', 'darkgreen', 'darkred', 'purple', 'cadetblue', 'blue', 'green',
              'lightred', 'red', 'cadetblue', 'black', 'darkpurple', 'pink', 'beige']
color_list_mark = ['#ff8a7c', '#cf3c29', '#416674', '#2f2f2f', '#593869', '#ff8de9', '#ffc88d', '#565656', '#00629d',
                   '#ed922e',
                   '#86d9ff', '#b8f471', '#a3a3a3', '#718123', '#9f3235', '#cc50b4', '#416675', '#37a6d8', '#6eaa25',
                   '#ff8a7c', '#cf3c29', '#416674', '#2f2f2f', '#593869', '#ff8de9', '#ffc88d']

m = folium.Map(location=[55.7522200, 37.6155600], zoom_start=8, tiles=None)
folium.TileLayer('openstreetmap', name='Карта вузов').add_to(m)




tooltip = GeoJsonTooltip(
    fields=['name', 'name:ru'],
    aliases=['Регион', 'Количество студентов'],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

students_dict = {}
school_dict_1 = {}
data_new_json = data_new_json.fillna(0)

data_new_json['Студенты'] = data_new_json['Студенты'].apply(lambda x: 0 if x == '' else x)
data_new_json['Студенты'] = data_new_json['Студенты'].apply(lambda x: int(x))

data_new_json = data_new_json.groupby(by='Регион')['Студенты'].sum()
region_to_stat = data_new_json.index
students_quantity = data_new_json.to_list()

data_new_school = pd.read_csv('csv_files/shkoly_po_regionam.csv', encoding='utf-8 ', sep=';')
region_school = data_new_school['Регион'].to_list()
students_school = data_new_school['Количество учащихся'].to_list()
for i in range(len(region_school)):
    reg_now = region_school[i]
    school_dict_1[reg_now] = students_school[i]

for i in range(len(region_to_stat)):
    reg_now = region_to_stat[i]
    # if len(region_to_stat[i].split(' ')) > 1 and region_to_stat[i].split(' ')[1] == 'Республика':
    #     reg_now = ' '.join(reversed(region_to_stat[i].split(' ')))
    students_dict[reg_now] = students_quantity[i]
# 'name', 'name:ru', 'boundary', 'admin_level'
with open('geojson/admin_level_41.geojson', encoding='utf-8') as f:
    data = geojson.load(f)
    k = 1
    columns = pd.DataFrame(columns=['Регион', 'Количество студентов'])
    for j, features in enumerate(data['features']):
        if k == 1:
            k += 1
            continue
        if features['properties']['name:ru'] in ['Севастополь','Республика Крым',
                                                 'Ненецкий автономный округ', 'Ямало-Ненецкий автономный округ']:
            columns.loc[j - 1] = [features['properties']['name:ru'], 0]
            features['properties']['boundary'] = 0
            continue
        if features['properties']['name:ru'] in ['Москва', 'Санкт-Петербург']:
            columns.loc[j - 1] = [features['properties']['name:ru'], 150000]
            features['properties']['boundary'] = int(students_dict[features['properties']['name:ru']])
            continue

        columns.loc[j - 1] = [features['properties']['name:ru'], int(students_dict[features['properties']['name:ru']])]
        features['properties']['boundary'] = int(students_dict[features['properties']['name:ru']])

with open("geojson/admin_level_42.geojson", "w", encoding="utf-8") as file:
    json.dump(data, file)

pprint.pp(school_dict_1)
with open('geojson/admin_level_42.geojson', encoding='utf-8') as f:
    data = geojson.load(f)
    k = 1
    columns_chool_1 = pd.DataFrame(columns=['Регион', 'Количество школьников'])
    for j, features in enumerate(data['features']):
        if k == 1:
            k += 1
            continue
        if features['properties']['name:ru'] in ['Республика Крым' ]:
            columns_chool_1.loc[j - 1] = [features['properties']['name:ru'], 0]
            features['properties']['admin_level'] = 0
            continue
        if features['properties']['name:ru'] in ['Краснодарский край', 'Москва', 'Московская область']:
            columns_chool_1.loc[j - 1] = [features['properties']['name:ru'], 500000]
            features['properties']['admin_level'] = int(school_dict_1[features['properties']['name:ru']])
            continue

        columns_chool_1.loc[j - 1] = [features['properties']['name:ru'],
                                      int(school_dict_1[features['properties']['name:ru']])]
        features['properties']['admin_level'] = int(school_dict_1[features['properties']['name:ru']])

with open("geojson/admin_level_43.geojson", "w", encoding="utf-8") as file:
    json.dump(data, file)

popup = GeoJsonPopup(
    fields=['name:ru', 'boundary', 'admin_level'],
    aliases=['Регион', "Количество студентов", 'Количество школьников'],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

columns['Количество школьников'] = columns_chool_1['Количество школьников']
columns_chool_1['Количество студентов'] = columns['Количество студентов']
Cho = folium.Choropleth(json.load(open('geojson/admin_level_42.geojson', encoding='utf-8')),
                        name='Количество студентов в регионах',
                        data=columns,
                        style_function=lambda feature: {
                            'fillColor': 'rgba(0,0,0,0)',
                            'color': 'black',
                            'weight': 0.2,
                        },
                        tooltip=tooltip,
                        columns=['Регион', 'Количество студентов'],
                        key_on='feature.properties.name:ru',
                        fill_color='BuPu',
                        popup=popup,
                        show=False
                        ).add_to(m)

popup1 = GeoJsonPopup(
    fields=['name:ru', 'boundary', 'admin_level'],
    aliases=['Регион', "Количество студентов", 'Количество школьников'],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)
print(columns_chool_1)

Cho1 = folium.Choropleth(json.load(open('geojson/admin_level_43.geojson', encoding='utf-8')),
                         name='Количество школьников в регионах',
                         data=columns_chool_1,
                         style_function=lambda feature: {
                             'fillColor': 'rgba(0,0,0,0)',
                             'color': 'black',
                             'weight': 0.2,
                         },
                         tooltip=tooltip,
                         columns=['Регион', 'Количество школьников'],
                         key_on='feature.properties.name:ru',
                         fill_color='YlGn',
                         popup=popup1,
                         show=False
                         ).add_to(m)

Geo1 = folium.GeoJson(json.load(open('geojson/admin_level_43.geojson', encoding='utf-8')),
                      popup=popup1,
                      style_function=lambda feature: {
                          'fillColor': 'rgba(0,0,0,0)',
                          'color': 'black',
                          'weight': 0.5,
                      },
                      control=False,
                      overlay=True
                      ).add_to(m)

fg_ll = folium.FeatureGroup('Все университеты').add_to(m)
fg0 = folium.FeatureGroup(name='Университеты по категориям',control=False ).add_to(m)

i = range(26)
for i, category, color, color_mark in zip(i, category_list, color_list, color_list_mark):

    icon_create_function = '''
    function (cluster) {
        var childCount = cluster.getChildCount();
        return new L.DivIcon({ html: '<style type="text/css">'''
    icon_create_function += f'.my_new_icon_{i}'
    icon_create_function += '{display:flex;justify-content:center;'
    icon_create_function += f'border: grey solid 2px;background-color:{color_mark};'
    icon_create_function += '''border-radius:25px;align-items:center;}</style><div style="color: white"><span>' + childCount + '</span></div>', className: '''
    icon_create_function += f'"my_new_icon_{i}"'
    icon_create_function += ''', iconSize: new L.Point(30, 30) });
        }'''

    if category == 'Все':
        continue
    else:
        fg = folium.plugins.FeatureGroupSubGroup(fg0, f'{category}', show=False).add_to(m)
    title = data_new['Вуз']
    place = data_new['Адрес']
    e_mail = data_new['e-mail']
    number = data_new['Телефон']
    site = data_new['Сайт']
    categorys = data_new['Категории'].apply(lambda x: x.split(','))
    lat = data_new['lat']
    long = data_new['long']

    marker_cluster = MarkerCluster(icon_create_function=icon_create_function).add_to(fg)

    for title, place, e_mail, number, site, lat, long, categorys in zip(title, place, e_mail, number, site, lat, long,
                                                                        categorys):

        html = '''
        <style type="text/css">
            .popup_my{
                display:flex;
                max-width:100%;
                flex-direction:column

            }
        </style>

        '''
        html += f'<div class="popup_my"><h4>{title}</h4>\n' \
                f'<p>{place}</p> \n' \
                f'<a href="{e_mail}" target="_blank">{e_mail}</a> \n' \
                f'<p>{number}</p> \n' \
                f'<a href="{site}" target="_blank">{site}</a></div> \n'
        iframe = folium.IFrame(html=html, width=200, height=300)
        popup = folium.Popup(iframe, max_width=200)

        if category in categorys:
            folium.Marker(location=[lat, long], radius=9, popup=popup,
                          icon=folium.Icon(color=f'{color}'), fill_opacity=1, tooltip=f'{category}: {title}').add_to(
                marker_cluster)
        elif category == 'Все':
            folium.Marker(location=[lat, long], radius=9, popup=popup,
                          icon=folium.Icon(color=f'{color}'), fill_opacity=1, tooltip=f'{category}: {title}').add_to(
                marker_cluster)

color_mark = '#cf3c29'
color = 'red'
i = 26
icon_create_function = '''
function (cluster) {
    var childCount = cluster.getChildCount();
    return new L.DivIcon({ html: '<style type="text/css">'''
icon_create_function += f'.my_new_icon_{i}'
icon_create_function += '{display:flex;justify-content:center;'
icon_create_function += f'border: grey solid 2px;background-color:{color_mark};'
icon_create_function += '''border-radius:25px;align-items:center;}</style><div style="color: white"><span style="font-size:12px;">' + childCount + '</span></div>', className: '''
icon_create_function += f'"my_new_icon_{i}"'
icon_create_function += ''', iconSize: new L.Point(30, 30) });
    }'''



title = data_new_2['Вуз']
place = data_new_2['Адрес']
e_mail = data_new_2['Почта']
number = data_new_2['Номер']
site = data_new_2['Сайт']
quantity = data_new_2['Студенты']
middle = data_new_2['Средний балл']
lat = data_new_2['lat']
long = data_new_2['long']

marker_cluster = MarkerCluster(icon_create_function=icon_create_function,).add_to(fg_ll)

for title, place, e_mail, number, site, quantity, middle, lat, long, in zip(title, place, e_mail, number, site,
                                                                            quantity, middle, lat, long,
                                                                            ):
    html = '''
    <style type="text/css">
        .popup_my{
            display:flex;
            max-width:100%;
            flex-direction:column

        }
    </style>
    '''
    try:
        quantity = int(quantity)
    except ValueError:
        pass
    quantity = str(quantity)
    if quantity == 'nan':
        quantity = '-'

    try:
        number = int(number)
    except ValueError:
        pass
    number = str(number)
    if number == 'nan':
        number = '-'

    try:
        middle = int(middle)
    except ValueError:
        pass
    middle = str(middle)
    if middle == 'nan':
        middle = '-'

    html = '''
            <style type="text/css">
                .popup_my{
                    display:flex;
                    max-width:100%;
                    flex-direction:column
                }
                .str{
                    margin-top: 4px;
                    margin-bottom: 4px;
                }
            </style>'''

    html += f'<div class="popup_my"><h4>{title}</h4>\n' \
            f'<div class="str">Кол-во студентов: {quantity}</div> \n' \
            f'<div class="str">Ср.балл ЕГЭ: {middle}</div> \n' \
            f'<div class="str">e-mail: <a>{e_mail}</a></div> \n' \
            f'<div class="str">Тел:<a >{number}</a></div> \n' \
            f'<div class="str">Сайт:<a href="{site}" target="_blank">{site}</a></div> \n' \
            f'</div> \n'
    iframe = folium.IFrame(html=html, width=200, height=300)
    popup = folium.Popup(iframe, max_width=200)

    folium.Marker(location=[lat, long], radius=9, popup=popup,tooltip=f'{title}',
                  icon=folium.Icon(color=f'{color}'), fill_opacity=1).add_to(
        marker_cluster)
folium.plugins.MeasureControl().add_to(m)
folium.LayerControl().add_to(m)
folium.plugins.LocateControl().add_to(m)

m.save('map_1.html')
