# -*- coding: utf-8 -*-
from parser import Parser


HOST = 'https://auto.ru/'
URL = 'https://auto.ru/cars/bmw/3er/all/'

# Кол-во владельцев: [Не имеет значения, один, не более двух]
OWNERS_COUNT_LIST = [None, 'ONE', 'LESS_THAN_TWO']
CITIES_DICT = {
    'Санкт Петербург': 'sankt-peterburg/',
    'Москва': 'moskva/',
    'Нижний Новгород': 'nizhniy_novgorod/',
    'Екатеринбург': 'ekaterinburg/',
    'Казань': 'kazan/',
    'Владивосток': 'vladivostok/',
    'Новосибирск': 'novosibirsk/',
    'Краснодар': 'krasnodar/',
    'Уфа': 'ufa/',
}


def print_cars(cars_list):
    print(f'Всего найдено {len(cars_list)} автомобилей')
    i = 0
    for car in cars_list:
        i += 1
        print(f"{i} - {car['title']}\t{car['year']} год\t{car['mileage']}\t{car['link']}"
              f"\t{car['price']}\t{car['city']}")


if __name__ == '__main__':

    city = input('Введите город: ')
    if city:
        url = HOST + CITIES_DICT[city] + '/cars/bmw/3er/all/'
    else:
        url = HOST + 'cars/bmw/3er/all/'

    price_from = int(input('Цена от (в рублях): '))
    price_to = int(input('Цена до (в рублях): '))

    owners_count_index = int(input('Укажите кол-во владельцев:\n'
                                   '0 - не имеет значения\n1 - один владелец\n2 - Не более двух\n'))
    if owners_count_index not in range(3):
        owners_count = OWNERS_COUNT_LIST[0]
    else:
        owners_count = OWNERS_COUNT_LIST[owners_count_index]

    km_age_to = int(input('Пробег до (в км): '))

    parser = Parser(
        url=url,
        price_from=price_from,
        price_to=price_to,
        city=city,
        owners_count=owners_count,
        km_age_to=km_age_to
    )
    result = parser.run_parsing()
    print_cars(cars_list=result)
