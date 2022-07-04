import requests
from bs4 import BeautifulSoup as BS

import csv

def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def get_data(html):
    soup = BS(html,'lxml')
    catalog = soup.find('div', class_='amw-card-list__items-wrapper amw-card-list__items-wrapper--desktop')
    healths = catalog.find_all('div', class_='amw-card-list__info')
    h = []
    for health in healths:
        try:
            title = health.find('div', class_="amw-card-list__title amw-editor-text").text.strip()
        except:
            title = 'Health'

        try:
            description = health.find('div', class_="amw-card-list__description amw-editor-text").text.strip()
        except:
            description = 'https://thumbor.forbes.com/thumbor/fit-in/1200x0/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5d35eacaf1176b0008974b54%2F0x0.jpg%3FcropX1%3D790%26cropX2%3D5350%26cropY1%3D784%26cropY2%3D3349'
      
        data = {
            'title': title,
            'description': description,
               }    
         
        h.append(data)
    return h
     

def main():
    url = 'https://www.amway.ru/sovety/poleznye-sovety-dlya-zdorovya'
    html = get_html(url)
    r = get_data(html)
    return r
