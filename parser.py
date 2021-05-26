import requests
from bs4 import BeautifulSoup
from settings import HOST, HEADERS


class Parser:
    def __init__(self, url):
        self.url = url
        self.html = None

    def get_html(self, params=None):
        try:
            html = requests.get(self.url, headers=HEADERS, params=params)
            html.encoding = 'utf-8'
            return html
        except requests.ConnectionError:
            return None


class ParserCars(Parser):
    """ Парсинг автомобилей с сайта auto.ru по заданным характеристикам """
    def __init__(self, url, price_from=None, price_to=None, owners_count=None, km_age_to=None, city=None):
        super(ParserCars, self).__init__(url=url)
        self.city = city
        self.cars_list = []
        self.params = {
            'owners_count_group': owners_count,
            'price_from': price_from,
            'price_to': price_to,
            'km_age_to': km_age_to
        }

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
        self.html = self.get_html(params=self.params)
        if self.html:
            if self.html.status_code == 200:
                print('Соединение установлено!')
                pages_count = self.get_pages_count()
                for page in range(1, pages_count + 1):
                    print(f'Парсинг страницы {page} из {pages_count}...')
                    self.html = self.get_html(params={
                        'page': page,
                        'owners_count_group': self.params['owners_count_group'],
                        'price_from': self.params['price_from'],
                        'price_to': self.params['price_to'],
                        'km_age_to': self.params['km_age_to']
                    })
                    self.get_content()
                return self.cars_list
            else:
                print(f'Ошибка соединения! Код - {self.html.status_code} :(')
        else:
            print("Ошибка Соединения! Нет подключения к интернету.")


class ParserSlugs(Parser):
    """
    Получает названия и компоненты ссылок на марки и серии автомобилей для занесения в базу данных
    и дальнейшего использования при генерации ссылки исходя из введенных параметров автомобиля
    """
    def __init__(self):
        super(ParserSlugs, self).__init__(url=HOST)
        self.params = None

    def get_models(self, car):
        """ Парсит страницу серии для определенной марки автомобиля
        :param car: -Название марки
        :return: - Список серий и компонентов для построения ссылки
                 разделенных ':' для удобства сплита
        """
        print(f'Парсинг страницы {car}')
        models_list = []
        self.html = self.get_html()
        soup = BeautifulSoup(self.html.text, 'html.parser')
        items_slugs = soup.find_all('a', class_='ListingPopularMMM-module__itemName')
        for item_slug in items_slugs:
            car = item_slug.get_text()
            slug = item_slug.get('href')
            models_list.append(f"{car}:{slug.split('/')[5]}")
        return models_list

    def get_cars(self):
        """
        Парсит главную страницу, вытаскивает названия каждой марки и ссылку на нее
        После чего проходит по каждой ссылке методом get_models
        Возвращает полученные данные в списке в формате:
        марка-ссылка на марку-серия1:ссылка на серию1, серия2 - ссылка на серию2 ... и тд
        Каждая марка запмсывается в новый элемент списка
        Разделители '-' ',' ':' применяются для удобства сплита
        """
        print('Парсинг главной страницы')
        data_list = []
        soup = BeautifulSoup(self.html.text, 'html.parser')
        items_slugs = soup.find_all('a', class_='IndexMarks__item')

        for item_slug in items_slugs:
            car = item_slug.find('div', 'IndexMarks__item-name').get_text()
            slug = item_slug.get('href')
            line_for_write = f"{car}-{slug.split('/')[4]}-"
            self.url = slug
            models_list = self.get_models(car=car)
            for model in models_list:
                line_for_write += f"{model},"

            data_list.append(line_for_write[:-1])
        return data_list

    def run_parsing(self):
        """
        :return: Данные для записи в БД или текстовый файл в виде списка строк
        """
        data_list = None
        print('Установка соединения...')
        self.html = self.get_html()
        if self.html:
            if self.html.status_code == 200:
                print('Соединение установлено!')
                data_list = self.get_cars()
                print('Парсинг завершен')
            else:
                print(f'Ошибка соединения! Код - {self.html.status_code} :(')
        else:
            print("Ошибка Соединения! Нет  подключения к интернету.")

        return data_list
