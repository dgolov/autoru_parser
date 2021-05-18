# -*- coding: utf-8 -*-
# Парсинг сайта auto.ru по заданным характеристикам с выводом результата в таблицу
import requests
from bs4 import BeautifulSoup


URL = 'https://auto.ru/cars/bmw/3er/all/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
    'Accept': '*/*'
}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    response.encoding = 'utf-8'
    return response


def get_content(html):
    cars = []
    soup = BeautifulSoup(html, 'html.parser')
    items_cards = soup.find_all('div', class_='ListingItem-module__main')

    for item_card in items_cards:
        try:
            price = item_card.find('div', class_='ListingItemPrice-module__content').get_text()
        except AttributeError:
            price = 'Цена не указана'
        try:
            city = item_card.find('span', class_='MetroListPlace__regionName').get_text()
        except AttributeError:
            # Если не указан город, значит автомобиль уже продан, отображать его нет смысла
            continue
        cars.append({
            'title': item_card.find('a', class_='ListingItemTitle-module__link').get_text(),
            'link': item_card.find('a', class_='Link ListingItemTitle-module__link').get('href'),
            'price': price,
            'year': item_card.find('div', class_='ListingItem-module__year').get_text(),
            'mileage': item_card.find('div', class_='ListingItem-module__kmAge').get_text(),
            'city': city
        })
    return cars


def print_cars(cars):
    print(f'Всего найдено {len(cars)} автомобилей')
    i = 0
    for car in cars:
        i += 1
        print(f"{i} - {car['title']}\t{car['year']} год\t{car['mileage']}\t{car['link']}"
              f"\t{car['price']}\t{car['city']}")


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html=html.text)
        print_cars(cars=cars)
    else:
        print('Error!')


if __name__ == '__main__':
    parse()
