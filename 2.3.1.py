# Для выполнения этой практики взял практику 1.5.2, тк она имеет в моем решении много функций
import csv
import re
import prettytable
from math import floor
from prettytable import PrettyTable

class Job:
    """Класс для представления Работы.
    Attributes:
        dic (dict): Словарь
    """
    def __init__(self, dic: dict):

        """Инициализирует объект Job, получает данные из файла и записывает в словарь к нужному критерию вакансии.

        Args:

        name (str) - Название вакансии
        desc (str) - Описание вакансии
        skills (str) - Навыки для вакансии
        exp (str or int) - Опыт работы
        prem (str) - Проверка на премиум - вакансию
        emp (str) - Компания
        s_from (str or int or float) - Нижняя граница оклада
        s_to (str or int or float) - Верхняя граница оклада
        s_final (str or int or float) - Финальный оклад
        area (str) - Название региона
        time (int) - Дата публикации вакансии
        """
        self.dic = dic
        self.name = dic["name"]
        self.desc = dic["description"]
        self.skills = dic["key_skills"]
        self.exp = dic["experience_id"]
        self.prem = dic["premium"]
        self.emp = dic["employer_name"]
        self.s_from = dic["salary_from"]
        self.s_to = dic["salary_to"]
        self.s_final = dic["salary_final"]
        self.area = dic["area_name"]
        self.time = dic["published_at"]


    def tableF(self, val: str) -> str:
        """Получает на вход данные ячейки, и если количество ее символов больше 100, то функция оставляет первые 100 символов и ставит "...".
        :param val: (str) -данные одной ячейки
        :return: (str) - Обрезанные данные ячейки
        """
        return val if len(val) < 100 else val[:100] + "..."


    def listF(self):
        """Функция, позволяющая корректно использовать метод __init__
        :return: (str) Ключ словаря
        """
        c = self
        uni = [c.name, c.desc, c.skills, c.exp, c.prem, c.emp, c.s_final, c.area, c.time]
        return [c.tableF(val) for val in uni]

def csv_reader(file_name):
    """Функция чтения файла

    :param file_name: (str) Название файла
    :return: headers (list) - Список заголовков
     values (List) - Список значений ячеек одной вакансии
    """
    headers = []
    values = []
    with open(file_name, "r", encoding='utf-8-sig', newline='') as csv_file:
        reader = csv.reader(csv_file)
        try: headers = next(reader)
        except: go_to_exit("Пустой файл")
        values = [line for line in reader if not ("" in line or len(line) != len(headers))]
        if len(values) <= 0:
            go_to_exit("Нет данных")
        return headers, values

def csv_filter(reader, list_naming):
    """Функция фильтрации входных данных

    :param reader: (list) Список значений ячеек одной вакансии
    :param list_naming: Список заголовков
    :return: data (list) - Отфильтрованный список значений ячеек одной вакансии
    """
    data = []
    for vacan in reader:
        appx = dict(zip(list_naming, [cleaner(field) for field in vacan]))
        data.append(appx)
    return data

def print_vacancies(data_vacancies, dic_naming, colum, fro):
    """Функция вывода таблицы

    :param data_vacancies: (list) список, содержащий отфильтрованные и очищенные данные ячеек
    :param dic_naming: (dict) Переведенный список названий столбцов, которые будут выведены
    :param colum: (str) Названия столбцов, которые нужно выводить в таблице
    :param fro: (int) Порядковые номера вакансий - нумерация в пределах отфильтрованных данных
    """
    fro = fro + [len(data_vacancies)+1] if len(fro) == 1 else fro
    fro = [1, len(data_vacancies)+1] if len(fro) == 0 else fro
    fro = [int(val) for val in fro]
    exit_table = PrettyTable(align="l", hrules=prettytable.ALL)
    exit_table.field_names = dic_naming.values()
    exit_table.max_width = 20
    [exit_table.add_row([i+1] + data_vacancies[i]) for i in range(len(data_vacancies))]
    if len(data_vacancies) <= 0:
        go_to_exit("Ничего не найдено")
    else:
        print(exit_table.get_string(start=fro[0]-1, end=fro[1]-1, fields=colum))

def formatter(row):
    dict2 = {}
    row.update({"salary_final":None})
    for key, val in row.items():
        val = trying(val)
        try: val = keyfunD[key](val, dict2)
        except: None
        dict2[key] = val
    return Job(dict2)

#my functions

def numberF(num):
    """Вспомогательная функция форматирования данных оклада

    :param num: (int) Данные оклада
    :return: (str) Отформатированные данные оклада
    """
    number = floor(float(num))
    return '{:,}'.format(number).replace(",", " ")

def trying(val):
    """Функция перевода аббревиатуры валюты на русский язык

    :param val: (str) Аббревиатура валюты
    :return: (str) Название валюты на русском языке
    """
    try: val = toRuD[val]
    except: None
    return val

def moneyF(row):
    """Функция форматирования данных оклада

    :param row: (str) Ключ
    :return: (str) Выходные данные ячейки Оклад
    """
    start_sal = numberF(row["salary_from"])
    end_sal = numberF(row["salary_to"])
    salary_n = "Без вычета налогов" if row['salary_gross'] == "Да" else "С вычетом налогов"
    return f"{start_sal} - {end_sal} ({row['salary_currency']}) ({salary_n})"

def dateF(val):
    """Функция форматирования данных даты публикации

    :param val: (list) Дата публикации
    :return: (str) Выходные данные ячейки Дата публикации вакансии
    """
    valu = val.split("T")[0].split("-")
    return f"{valu[2]}.{valu[1]}.{valu[0]}"

def cleaner(val):
    """Функция очистки входных данных от html тегов и отступов

    :param val: (str) Входные данные одной ячейки
    :return: (str) Очищенные данные одной ячейки
    """
    newval = re.sub(r"\<[^>]*\>", '', val).strip()
    if newval.find("\n") > -1:
        newval = newval.replace("\r", "")
    else:
        newval = re.sub(r'\s+', ' ', newval)
    return newval

def go_to_exit(val):
    """Функция остановки программы

    :param val: (str) Сообщение при остановке программы
    """
    print(val)
    exit(0)

def checkerF(filter_key, filterD):
    """Функции проверки корректного ввода данных

    :param filter_key: (str) Ввоодимый параметр фильтрации
    :param filterD: (dict) Названия столбцов
    :return: (str) Ключ фильтрации
    """
    if filter_key == "":
        return []
    k = filter_key.split(": ")
    if len(k) <= 1:
        go_to_exit("Формат ввода некорректен")
    if k[0] not in filterD.keys():
        go_to_exit("Параметр поиска некорректен")
    k[0] = filterD[k[0]]
    k[1] = k[1].split(", ")
    return k

def salaryF(job: Job, keys):
    return int(keys[0]) >= int(job.s_from) and int(keys[0]) <= int(job.s_to)

def skillF(job: Job, skills):
    """Функция форматирования данных ячейки Навыки

    :param job: (str) Название вакансии
    :param skills: (str) Навыки вакансии
    :return: (str) Навыки вакансии, каждый навык на новой строке
    """
    vacsk = job.skills.split("\n")
    return all([s in vacsk for s in skills])

def filter(j,ru_en, key_vals):
    """Функция фильтрации и добавления данных вакансий в итоговый список

    :param j: (list) Данные вакансии
    :param ru_en: (dict) Названия столбцов
    :param key_vals: (str) Ключ фильтрации
    :return: (list)
    """
    data3 = []
    for job in j:
        if len(key_vals) >= 2:
            try:
                key1 = dict_check_key_function[key_vals[0]](job, key_vals[1])
            except:
                key1 = True if job.dic[key_vals[0]] == key_vals[1][0] else False
        else:
            key1 = True
        if key1: data3.append(job.listF())
    return data3

translate_nameD = {
    "№": "№",
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_final": "Оклад",
    "area_name": "Название региона",
    "published_at": "Дата публикации вакансии"}

toRuD = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "False": "Нет",
    "True": "Да",
    "FALSE": "Нет",
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"}

filterD = {
    "Навыки": "key_skills",
    "Оклад": "salary_final",
    "Дата публикации вакансии": "published_at",
    "Опыт работы": "experience_id",
    "Премиум-вакансия": "premium",
    "Идентификатор валюты оклада": "salary_currency",
    "Название": "name",
    "Название региона": "area_name",
    "Компания": "employer_name"}

keyfunD = {
    "salary_final": lambda *keys: moneyF(keys[1]),
    "published_at": lambda *keys: dateF(keys[0])}

dict_check_key_function = {
    "salary_final": salaryF, "key_skills": skillF}

headers, values = csv_reader(input())
filter_key = checkerF(input(), filterD)
list1 = csv_filter(values, headers)
job_list = [formatter(dic) for dic in list1]
final_list = filter(job_list, filterD, filter_key)
count_fro = input().split()
colum = input().split(", ")
colum = translate_nameD.values() if colum == [''] else ["№"] + colum
print_vacancies(final_list, translate_nameD, colum, count_fro)
