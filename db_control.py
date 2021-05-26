from parser import ParserSlugs
from settings import *
from utils import convert_entered_data_to_int
import sqlite3
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


def get_models(car_id):
    for model in cursor.execute(f"SELECT id, title, car, slug FROM models WHERE car = {car_id}"):
        yield model


def update_db():
    parser = ParserSlugs()
    result_list = parser.run_parsing()
    for result in result_list:
        item_list = result.split('-')
        car_title = item_list[0]
        car_slug = item_list[1]
        models_list = item_list[2].split(',')
        car_id = update_cars(title=car_title, slug=car_slug)
        try:
            update_models(car_id, models_list)
        except IndexError:
            print('Ошибка добавления записи')
    db.commit()


def update_cars(title, slug):
    cursor.execute(f"SELECT id, title, slug FROM cars WHERE slug = '{slug}'")
    try:
        db_id, db_title, db_slug = cursor.fetchone()
        if db_title != title:
            cursor.execute(f"UPDATE cars SET title = '{title}' WHERE slug = '{slug}'")
            print(f"Запись {db_title} изменена на {title}")
            db.commit()
    except TypeError:
        cursor.execute(f"INSERT INTO cars (title, slug) VALUES (?, ?)", (title, slug,))
        print(f'Добавлена новая запись {title}')
        cursor.execute(f"SELECT id title, slug FROM cars WHERE slug = '{slug}'")
        db_id = cursor.fetchone()[0]
        db.commit()
    return db_id


def update_models(car_id, data_list):
    for model in data_list:
        model_list = model.split(':')
        title = model_list[0]
        slug = model_list[1]
        cursor.execute(f"SELECT title, slug FROM models WHERE slug = '{slug}'")
        try:
            db_title, db_slug = cursor.fetchone()
            if db_title != title:
                cursor.execute(f"UPDATE models SET title = '{title}' WHERE slug = '{slug}'")
                print(f"Запись {db_title} изменена на {title}")
                db.commit()
        except TypeError:
            cursor.execute(f"INSERT INTO models (title, car, slug) VALUES (?, ?, ?)", (title, car_id, slug,))
            print(f'Добавлена новая запись {title}')
            db.commit()


def delete_record(table, record_id):
    record_id = str(record_id)
    item = cursor.execute(f"SELECT id, title FROM {table} WHERE id = {record_id}")
    if len(item.fetchall()) > 0:
        cursor.execute(f"DELETE FROM {table} WHERE id = {record_id}")
        db.commit()
        print('Запись успешно удалена')
    else:
        print('Запись не найдена')


def show_tables():
    available_table = execute_sql_from_file('show_tables.sql')
    return available_table.fetchall()


def get_table_in_delete_menu():
    while True:
        print('Из какой таблицы удаляем?\n1 - cars\n2 - models\n0 - Выход в предыдущее меню')
        act = input('>>> ')
        if act == '1':
            return 'cars'
        elif act == '2':
            return 'models'
        elif act == '0':
            return
        else:
            print('Вы ввели некорректные данные')


def run():
    while True:
        print('\nВыберите действие')
        print('1 - Вывод таблицы марок автомобилей')
        print('2 - Вывод таблицы серий')
        print('3 - Обновление базы данных')
        print('4 - Удаление записей')
        print('0 - Выход из программы')
        act = input('>>> ')
        if act == '0':
            return
        elif act == '1':
            for value in get_cars():
                print(f'{value[0]} - {value[1]}')
        elif act == '2':
            car = input('Укажите марку автомобиля: ')
            cursor.execute(f"SELECT id, title FROM cars WHERE title = '{car}'")
            car_id = cursor.fetchone()
            for value in get_models(car_id[0]):
                print(f'{value[0]} - {car_id[1]} {value[1]}')
        elif act == '3':
            update_db()
        elif act == '4':
            table = get_table_in_delete_menu()
            if table == 'cars' or table == 'models':
                record_id = convert_entered_data_to_int('Введите id записи >> ')
                delete_record(table=table, record_id=record_id)
        else:
            print('Вы ввели некорректные данные')


if __name__ == '__main__':
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    execute_sql_from_file('create_cars.sql')
    execute_sql_from_file('create_models.sql')
    db.commit()
    print('Соединение с базой данных установлено!')
    run()
    print('Работа программы завершена')
