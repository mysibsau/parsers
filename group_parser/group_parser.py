import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import re
import json


class GroupParser:
    def __init__(self):
        self.groups = []


    def get_name_group(self, soup: BeautifulSoup):
        element = soup.find('h3', {'class': 'text-center'})
        if element:
            return element.text


    def parse_name_group(self, string: str) -> str:
        return string.split('"')[1]


    def get_group_by_id(self, id_group: int):
        html = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/group/{id_group}'
        ).text

        soup = BeautifulSoup(html, 'html.parser')
        group = self.get_name_group(soup)

        # Проверка на существование группы
        if group:
            return [id_group, self.parse_name_group(group)]


    def set_groups(self):
        '''Формирует словарь типа "название_группы": "id_группы"'''

        id_list = list(range(6000))
        pool = ThreadPool(16)
        
        # Формируем словарь
        for group in pool.map(self.get_group_by_id, id_list):
            if group:
                self.groups.append(group)
        
        pool.close()


    def save_data_in_json(self):
        with open('name_groups.csv', 'w', encoding="utf-8") as f:
            for i in self.groups:
                f.write(f'{i[0]};{i[1]}\n')
