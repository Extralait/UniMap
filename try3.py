import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
import pickle

with open('data.pickle', 'rb') as f:
   data_new = pickle.load(f)

data_new=pd.DataFrame(data_new,columns=['Товар','Цена','Картинка'])
print(data_new)
data_new.to_csv("output.csv", index=False,encoding='utf-8')

