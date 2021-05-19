import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
    'Accept': '*/*'
}


class Parser:
    """ Парсинг сайта auto.ru по заданным характеристикам """
    def __init__(self, url, price_from=None, price_to=None, owners_count=None, km_age_to=None, city=None):
        self.url = url
        self.owners_count = owners_count
        self.price_from = price_from
        self.price_to = price_to
        self.km_age_to = km_age_to
        self.city = city
        self.html = None
        self.cars_list = []

    @staticmethod
    def get_html(url, params):
        try:
            html = requests.get(url, headers=HEADERS, params=params)
            html.encoding = 'utf-8'
            return html
        except requests.ConnectionError:
            return None

    def get_pages_count(self):
        soup = BeautifulSoup(self.html.text, 'html.parser')
        pagination = soup.find_all('a', class_='ListingPagination-module__page')
        if pagination:
            return int(pagination[-1].get_text())
        else:
            return 1

    def get_content(self):
        soup = BeautifulSoup(self.html.text, 'html.parser')
        items_cards = soup.find_all('div', class_='ListingItem-module__main')

        for item_card in items_cards:
            try:
                price = item_card.find('div', class_='ListingItemPrice-module__content').get_text()
            except AttributeError:
                price = 'Цена не указана'
            try:
                city = item_card.find('span', class_='MetroListPlace__regionName').get_text()
                if self.city and self.city != str(city):
                    continue
            except AttributeError:
                # Если не указан город, значит автомобиль уже продан, отображать его нет смысла
                continue
            self.cars_list.append({
                'title': item_card.find('a', class_='ListingItemTitle-module__link').get_text(),
                'link': item_card.find('a', class_='Link ListingItemTitle-module__link').get('href'),
                'price': price,
                'year': item_card.find('div', class_='ListingItem-module__year').get_text(),
                'mileage': item_card.find('div', class_='ListingItem-module__kmAge').get_text(),
                'city': city
            })

    def run_parsing(self):
        print('Установка соединения...')
        self.html = self.get_html(url=self.url, params={
            'owners_count_group': self.owners_count,
            'price_from': self.price_from,
            'price_to': self.price_to,
            'km_age_to': self.km_age_to
        })
        if self.html:
            if self.html.status_code == 200:
                print('Соединение установлено!')
                pages_count = self.get_pages_count()
                for page in range(1, pages_count + 1):
                    print(f'Парсинг страницы {page} из {pages_count}...')
                    self.html = self.get_html(url=self.url, params={
                        'page': page,
                        'owners_count_group': self.owners_count,
                        'price_from': self.price_from,
                        'price_to': self.price_to,
                        'km_age_to': self.km_age_to
                    })
                    self.get_content()
                return self.cars_list
            else:
                print(f'Ошибка соединения! Код - {self.html.status_code} :(')
        else:
            print("Ошибка Соединения! Нет  подключения к интернету.")
