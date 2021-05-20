# -*- coding: utf-8 -*-
from config import *
from parser import Parser
import csv
import sqlite3
import os


def print_cars(cars_list):
    i = 0
    for car in cars_list:
        i += 1
        print(f"{i} - {car['title']}\t{car['year']} год\t{car['mileage']}\t{car['link']}"
              f"\t{car['price']}\t{car['city']}")


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Автомобиль', 'Ссылка', 'Цена', 'Год выпуска', 'Пробег', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['year'], item['mileage'], item['city']])


def generate_url(city, car, model):
    if city and car and model:
        url = HOST + CITIES_DICT[city] + 'cars/' + car + '/' + model + '/all/'
    elif city and car and not model:
        url = HOST + CITIES_DICT[city] + 'cars/' + car + '/all/'
    elif city and not car and not model:
        url = HOST + CITIES_DICT[city] + 'cars/all/'
    elif not city and car and model:
        url = HOST + 'cars/' + car + '/' + model + '/all/'
    elif not city and car and not model:
        url = HOST + 'cars/' + car + '/all/'
    else:
        url = HOST + 'cars/all/'
    return url


def get_entered_data(message_to_input):
    try:
        response = int(input(message_to_input))
    except ValueError:
        response = 0
    return response


if __name__ == '__main__':
    i = 0
    for car in CARS_DICT:
        if car:
            print(f'{i} - {car}')
        else:
            print(f'{i} - Не имеет значения')
        i += 1

    car_index = get_entered_data('Выберите марку автомобиля: ')
    car = CARS[car_index]
    print(car)

    i = 0
    for model in MODELS_DICT[car]:
        if model:
            print(f'{i} - {model}')
        else:
            print(f'{i} - Не имеет значения')
        i += 1

    model_index = get_entered_data('Выберите серию: ')
    model = MODELS_DICT[car][model_index]

    city = input('Введите город: ')

    url = generate_url(city, car, model)

    price_from = get_entered_data('Цена от (в рублях): ')
    price_to = get_entered_data('Цена до (в рублях): ')
    if price_from == 0:
        price_from = None
    if price_to == 0:
        price_to = None

    owners_count_index = get_entered_data('Укажите кол-во владельцев: 0 - не имеет значения'
                                          '\n1 - один владелец\n2 - Не более двух\n')
    if owners_count_index not in range(3):
        owners_count = OWNERS_COUNT_LIST[0]
    else:
        owners_count = OWNERS_COUNT_LIST[owners_count_index]

    km_age_to = get_entered_data('Пробег до (в км): ')

    parser = Parser(
        url=url,
        price_from=price_from,
        price_to=price_to,
        city=city,
        owners_count=owners_count,
        km_age_to=km_age_to
    )
    result_list = parser.run_parsing()
    if result_list:
        print(f'Всего найдено {len(result_list)} автомобилей')
        save_file(result_list, 'cars.csv')
        # print_cars(cars_list=result_list)
    else:
        print('По заданным характеристикам результат не найден...')
