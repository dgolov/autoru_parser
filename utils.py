from parser import ParserSlugs


def convert_entered_data_to_int(message_to_input):
    """ Конвертирует вводимое число в integer
        В случае ошибки обрабатывает исключение и возвращает 0
    :param message_to_input: - число в текстовом формате
    :return: - Integer
    """
    try:
        response = int(input(message_to_input))
    except ValueError:
        response = 0
    return response


def write_cars_to_file(cars_list):
    """ Запись спарсенных данных (марок и серий) в текстовый файл
    :param cars_list: - список строк полученных в результате парсинга
    """
    with open('cars.txt', 'w') as file:
        file.write('')  # Удаление данных из файла перед новой записью

    with open('cars.txt', 'a') as file:
        for line_for_write in cars_list:
            file.write(line_for_write + '\n')


if __name__ == '__main__':
    parser = ParserSlugs()
    data_list = parser.run_parsing()
    if data_list:
        write_cars_to_file(cars_list=data_list)
