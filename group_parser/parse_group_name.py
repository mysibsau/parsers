import requests
from bs4 import BeautifulSoup
import re
import json

groups = {}

def is_group(soup):
    element = soup.find('h3', {'class': 'text-center'})
    if element is not None:
        return element.text
    return False


def parse_name_group(string):
    string = re.sub(r"\s", "", string)
    string = ''.join(list(string)[1:])
    name_group = string[: string.find("\"")]
    return name_group


def get_name_groups_by_id():
    for id_group in range(0, 6000):
        # Получение страницы
        html = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/group/{id_group}'
        ).text

        soup = BeautifulSoup(html, 'html.parser')
        group = is_group(soup)

        # Проверка на существование группы
        if group is not False:
            groups.update({ parse_name_group(group) : id_group })

    return groups


def save_data_in_json(data):
    f = open('name_groups.json', 'w', encoding="utf-8")
    json.dump(data, f, ensure_ascii=False, indent=4)


save_data_in_json(get_name_groups_by_id())