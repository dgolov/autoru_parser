from config import *
import os


def execute_sql_from_file(file):
    path = os.path.join('sql', file)
    with open(path, 'r') as sql_file:
        script = sql_file.read()
        cursor.execute(script)
    return cursor


def get_cars():
    for car in cursor.execute("SELECT id, title, slug FROM cars"):
        yield car


def get_models():
    for model in cursor.execute("SELECT id, title, car, slug FROM models"):
        yield model


def add_car(data_dict=None):

    def create_car_record(title, slug):
        cursor.execute(f"SELECT title FROM cars WHERE title = '{title}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO cars (title, slug) VALUES (?, ?)", (title, slug,))
            db.commit()
            print('Добавлена новая запись!')
        else:
            print('Запись уже существует')

    if not data_dict:
        title = input('Укажите марку автомобиля: ')
        slug = input('Укажите название для составления ссылки на auto.ru: ')
        create_car_record(title, slug)
    else:
        for title, slug in data_dict.items():
            create_car_record(title, slug)


def add_model(data_dict=None):

    def create_model_record(title, car_id, slug):
        cursor.execute(f"SELECT title FROM models WHERE title = {title}")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO models (title, car, slug) VALUES (?, ?, ?)", (title, car_id, slug,))
            db.commit()
            print('Добавлена новая запись!')
        else:
            print('Запись уже существует')

    if not data_dict:
        car = input('Укажите марку автомобиля: ')
        title = input('Укажите серию: ')
        slug = input('Укажите название для составления ссылки на auto.ru: ')
        db_object = cursor.execute(f"SELECT id, title FROM cars WHERE title = '{car}'")
        car_id = db_object.fetchall()
        create_model_record(title, car_id[0][0], slug)
    else:
        pass


def show_tables():
    cursor = execute_sql_from_file('show_tables.sql')
    available_table = (cursor.fetchall())
    return available_table


def get_add_menu(func, data):
    while True:
        print('Добавить данные\n1 - из словаря\n2 - вручную\n0 - Выход в предыдущее меню')
        act = input('>>> ')
        if act == '1':
            func(data)
        elif act == '2':
            func()
        elif act == '0':
            return
        else:
            print('Вы ввели некорректные данные')


def run():
    while True:
        print('\nВыберите действие')
        print('1 - Добавить марку автомобиля')
        print('2 - Добавить серию автомобиля')
        print('3 - Вывод таблицы автомобилей')
        print('4 - Вывод таблицы серий')
        print('0 - Выход из программы')
        act = input('>>> ')
        if act == 0:
            return
        elif act == '1':
            get_add_menu(add_car, CARS_DICT)
        elif act == '2':
            get_add_menu(add_model, MODELS_DICT)
        elif act == '3':
            for value in get_cars():
                print(value)
        elif act == '4':
            for value in get_models():
                print(value)
        else:
            print('Вы ввели некорректные данные')


if __name__ == '__main__':
    db = sqlite3.connect('config.db')
    cursor = db.cursor()
    execute_sql_from_file('create_cars.sql')
    execute_sql_from_file('create_models.sql')
    db.commit()
    print('Соединение с базой данных установлено!')
    run()
