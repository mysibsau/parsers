import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import re
import json


class ProfessorParser:
    def __init__(self):
        self.professors = []


    def get_name_professor(self, soup):
        element = soup.find('h3', {'class': 'text-center'})
        if element:
            return element.text


    def parse_name_professor(self, string):
        string = re.sub(r"\s", "", string).split('-')[0]
        symbols = [string[string.find('.') - 2], string[string.find('.') - 1]]
        return string.replace(''.join(symbols), ' '.join(symbols))


    def get_professor_by_id(self, professor_id):
        html = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/professor/{professor_id}'
        ).text

        soup = BeautifulSoup(html, 'html.parser')
        professor_name = self.get_name_professor(soup)

        # Проверка на существование группы
        if professor_name:
            return [professor_id, self.parse_name_professor(professor_name)]


    def set_professors(self):
        '''Формирует словарь типа "название_группы": "id_группы"'''

        id_list = list(range(6000))
        pool = ThreadPool(16)
        
        # Формируем словарь
        for professor in pool.map(self.get_professor_by_id, id_list):
            if professor:
                self.professors.append(professor)
        
        pool.close()


    def save_data_in_csv(self):
        with open('name_professors.csv', 'w', encoding="utf-8") as f:
            for i in self.professors:
                f.write(f'{i[0]};{i[1]}\n')
