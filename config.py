import sqlite3


HOST = 'https://auto.ru/'

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

CARS = [None, 'vaz', 'alfa_romeo', 'audi', 'bmw', 'chery', 'chevrolet', 'citroen', 'daewoo', 'ford', 'geely', 'honda',
        'hyundai', 'infiniti', 'kia', 'land_rover', 'lexus', 'lifan', 'mazda', 'mercedes', 'mitsubishi', 'nissan',
        'opel', 'peugeot', 'porsche', 'renault', 'skoda', 'ssang_yong', 'subaru', 'suzuki', 'toyota', 'volkswagen',
        'volvo', 'gaz', 'zaz', 'uaz']

CARS_DICT = {
    'Не имеет значения': None,
    'ВАЗ': 'vaz',
    'Alfa Romeo': 'alfa_romeo',
    'Audi': 'audi',
    'BMW': 'bmw',
    'Chery': 'chery',
    'Chevrolet': 'chevrolet',
    'Citroen': 'citroen',
    'Daewoo': 'daewoo',
    'Ford': 'ford',
    'Geely': 'geely',
    'Honda': 'honda',
    'Hyundai': 'hyundai',
    'Infiniti': 'infiniti',
    'Kia': 'kia',
    'Land Rover': 'land_rover',
    'Lexus': 'lexus',
    'Lifan': 'lifan',
    'Mazda': 'mazda',
    'Mercedes Benz': 'mercedes',
    'Mitsubishi': 'mitsubishi',
    'Nissan': 'nissan',
    'Opel': 'opel',
    'Peugeot': 'peugeot',
    'Porsche': 'porsche',
    'Renault': 'renault',
    'Skoda': 'skoda',
    'Ssang Yong': 'ssang_yong',
    'Subaru': 'subaru',
    'Suzuki': 'suzuki',
    'Toyota': 'toyota',
    'Volkswagen': 'volkswagen',
    'Volvo': 'volvo',
    'ГАЗ': 'gaz',
    'ЗАЗ': 'zaz',
    'УАЗ': 'uaz',
}

MODELS_DICT = {
    'vaz': [None, ''],
    'alfa_romeo': [None, ''],
    'audi': [None, ''],
    'bmw': [None, '1er', '3er', '5er', '6er', '7er', 'x1',  'x3',  'x4',  'x5',  'x6',  'x7'],
    'chery': [None, ''],
    'chevrolet': [None, ''],
    'citroen': [None, ''],
    'daewoo': [None, ''],
    'ford': [None, ''],
    'geely': [None, ''],
    'honda': [None, ''],
    'hyundai': [None, ''],
    'infiniti': [None, ''],
    'kia': [None, ''],
    'land_rover': [None, ''],
    'lexus': [None, ''],
    'lifan': [None, ''],
    'mazda': [None, ''],
    'mercedes': [None, ''],
    'mitsubishi': [None, ''],
    'nissan': [None, ''],
    'opel': [None, ''],
    'peugeot': [None, ''],
    'porsche': [None, ''],
    'renault': [None, ''],
    'skoda': [None, ''],
    'ssang_yong': [None, ''],
    'subaru': [None, ''],
    'suzuki': [None, ''],
    'toyota': [None, ''],
    'volkswagen': [None, ''],
    'volvo': [None, ''],
    'gaz': [None, ''],
    'zaz': [None, ''],
    'uaz': [None, ''],
}
