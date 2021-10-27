# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия. ### По желанию можно добавить ещё параметры вакансии
# (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pymongo import MongoClient

vacancy_data = {'name': [], 'salary': [], 'link': [], 'site': []}
vacancy_to_get = 'Python'


def get_vacancy_hh(vacancy):
    link = 'https://hh.ru/search/vacancy'
    params = {'text': vacancy, 'search_field': 'name', 'items_on_page': '100', 'page': ''}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}

    html_response = requests.get(link, params=params, headers=headers)
    parsed_html = bs(html_response.text, 'html.parser')

    all_vacancy = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}) \
        .find_all('div', {'class': 'vacancy-serp-item'})

    for el in all_vacancy:
        # get name
        vacancy_data['name'].append(el.find('a').getText())
        # get salary
        try:
            vacancy_data['salary'].append(el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText())
        except AttributeError:
            vacancy_data['salary'].append('None')
        # get link
        vacancy_data['link'].append(el.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href'))
        vacancy_data['site'].append('hh.ru')


def get_vacancy_info(vacancy):
    get_vacancy_hh(vacancy)
    return vacancy_data


# get_vacancy_info(vacancy_to_get)


# result = pd.DataFrame(vacancy_data)
# result.to_excel('./result.xlsx', sheet_name='Budgets', index=False)
# ------------------------------------------------------------------------------------------------------------

# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.

client = MongoClient("mongodb+srv://Onlyjoy:roxxan94@testcluster.fas5o.mongodb.net/TestCluster?retryWrites=true&w=majority")
db = client.hh_db
jobs = db.jobs

get_vacancy_info(vacancy_to_get)


def add_to_db(data):
    for i in range(len(data['name'])):
        job_tup = {}
        for key, item in data.items():
            job_tup[key] = item[i]
        id = jobs.insert_one(job_tup).inserted_id
        print(id)

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# ----
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.


def update_db(old_data, new_data):
    for i in range(len(old_data['name'])):
        for key, item in old_data.items():
            old_values = {}
            new_values = {}

            old_values[key] = item[i]
            new_values['$set'] = {key: new_data[key][i]}
            jobs.update_one(old_values, new_values)


# добавляем данные в базу
# add_to_db(vacancy_data)

# обновляем данные
update_db(vacancy_data, get_vacancy_info(vacancy_to_get))
