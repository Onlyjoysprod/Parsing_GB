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


get_vacancy_info(vacancy_to_get)
result = pd.DataFrame(vacancy_data)
result.to_excel('./result.xlsx', sheet_name='Budgets', index=False)
