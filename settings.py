HOST = 'https://auto.ru/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
    'Accept': '*/*'
}

# Кол-во владельцев: [Не имеет значения, один, не более двух]
OWNERS_COUNT_LIST = [None, 'ONE', 'LESS_THAN_TWO']

DB_NAME = 'cars_data.db'

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
