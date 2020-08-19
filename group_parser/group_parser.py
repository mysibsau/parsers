import requests
from bs4 import BeautifulSoup
import re
import json


class GroupParser:
    def __init__(self):
        self.groups = {}


    def get_group(self, soup):
        element = soup.find('h3', {'class': 'text-center'})
        if element is not None:
            return element.text
        return False


    def parse_name_group(self, string):
        string = re.sub(r"\s", "", string)
        string = ''.join(list(string)[1:])
        name_group = string[: string.find("\"")]
        return name_group


    def get_name_groups_by_id(self, id_group):
        # Получение страницы
        html = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/group/{id_group}'
        ).text

        soup = BeautifulSoup(html, 'html.parser')
        group = self.get_group(soup)

        # Проверка на существование группы
        if group is not False:
            self.groups.update({ self.parse_name_group(group) : id_group })


    def save_data_in_json(self):
        f = open('name_groups.json', 'w', encoding="utf-8")
        json.dump(self.groups, f, ensure_ascii=False, indent=4)
        f.close()
