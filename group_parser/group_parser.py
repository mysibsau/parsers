import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re
import json


class GroupParser:
    def __init__(self):
        self.groups = {}


    def get_name_group(self, soup):
        element = soup.find('h3', {'class': 'text-center'})
        if element is not None:
            return element.text
        return False


    def parse_name_group(self, string):
        string = re.sub(r"\s", "", string)
        string = ''.join(list(string)[1:])
        name_group = string[: string.find("\"")]
        return name_group


    def get_group_by_id(self, id_group):
        '''Возвращает словарь из одного элемента типа "название_группы": "id_группы"'''

        html = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/group/{id_group}'
        ).text

        soup = BeautifulSoup(html, 'html.parser')
        group = self.get_name_group(soup)

        # Проверка на существование группы
        if group is not False:
            return { self.parse_name_group(group) : id_group }


    def set_groups(self):
        '''Формирует словарь типа "название_группы": "id_группы"'''

        # Диапазон id групп
        id_list = list( range(6000) )

        # Устанавливаем пул из 100 процессов - это оптимальное на моём комплюхтере
        pool = Pool(processes=100)
        
        # Формируем словарь
        for group in pool.map(self.get_group_by_id, id_list):
            if group is not None:
                self.groups.update( group )
        
        pool.close()


    def save_data_in_json(self):
        '''Сохраняет группы в json'''

        f = open('name_groups.json', 'w', encoding="utf-8")
        json.dump(self.groups, f, ensure_ascii=False, indent=4)
        f.close()
