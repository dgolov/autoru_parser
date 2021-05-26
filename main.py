# -*- coding: utf-8 -*-
from settings import *
from utils import convert_entered_data_to_int
from parser import ParserCars
import csv
import sqlite3


def print_cars(cars_list):
    index = 0
    for item_car in cars_list:
        index += 1
        print(f"{index} - {item_car['title']}\t{item_car['year']} год\t{item_car['mileage']}\t{item_car['link']}"
              f"\t{item_car['price']}\t{item_car['city']}")


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


if __name__ == '__main__':
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    # Первый элемент в каждом массиве None - означает что выбор не имеет значения
    # При таком выборе поиск осуществляется по всем автомобилям и/или по всем моделям
    cars_list = [None]
    model_list = [None]

    sql_cars_result = cursor.execute("SELECT id, title, slug FROM cars")
    for result in sql_cars_result:
        # Помещаем id, title, slug в кортеж, кортеж в список
        cars_list.append((result[0], result[1], result[2]))
    for car in cars_list:
        if car:
            print(f'{car[0]} - {car[1]}')
        else:
            print(f'0 - Не имеет значения')

    car_index = convert_entered_data_to_int('Выберите марку автомобиля: ')
    car_tuple = cars_list[car_index]
    car_index, car_title, car_slug = car_tuple
    print(car_title)

    sql_model_result = cursor.execute(f"SELECT id, title, slug fROM models WHERE car = {car_index}")
    for result in sql_model_result:
        model_list.append((result[0], result[1], result[2]))

    i = 0
    for model in model_list:
        if model:
            print(f'{i} - {model[1]}')
        else:
            print(f'0 - Не имеет значения')
        i += 1

    model_index = convert_entered_data_to_int('Выберите серию: ')
    model_tuple = model_list[model_index]
    model_index, model_title, model_slug = model_tuple
    print(model_title)

    city = input('Введите город: ')

    url = generate_url(city, car_slug, model_slug)

    price_from = convert_entered_data_to_int('Цена от (в рублях): ')
    price_to = convert_entered_data_to_int('Цена до (в рублях): ')
    if price_from == 0:
        price_from = None
    if price_to == 0:
        price_to = None

    owners_count_index = convert_entered_data_to_int('Укажите кол-во владельцев: 0 - не имеет значения'
                                                     '\n1 - один владелец\n2 - Не более двух\n')
    if owners_count_index not in range(3):
        owners_count = OWNERS_COUNT_LIST[0]
    else:
        owners_count = OWNERS_COUNT_LIST[owners_count_index]

    km_age_to = convert_entered_data_to_int('Пробег до (в км): ')

    parser = ParserCars(
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
