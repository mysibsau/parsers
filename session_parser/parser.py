from bs4 import BeautifulSoup
import requests
import re


class Parser:
    def __init__(self):
        self.session = []


    def get_session(self, group_id):
        for ind, day in enumerate(self.get_exam_days(group_id)):
            self.session.append({
                'date': self.get_exam_date(day, ind + 2),
                'time': self.get_exam_time(day, ind + 2),
                'discipline': self.get_name_exam(day, ind + 2),
                'type_discipline': self.get_type_discipline(day, ind + 2),
                'proffesor': self.get_proffesor(day, ind + 2),
                'location_in_university': self.get_location_in_university(day, ind + 2),
                'location_in_city': self.get_location_in_city(day, ind + 2)
            })
        return self.session


    def get_exam_days(self, id):
        response = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/group/{id}'
        ).text
        soup = BeautifulSoup(response, 'html.parser')
        return self.check_session(soup.select('#session_tab > div'))


    def get_exam_date(self, day, child_num):
        date = day.select(f'#session_tab > div:nth-child({child_num}) > div.header > div.name.text-center > div')[0].text
        return re.sub(r"\s", "", date)


    def get_exam_time(self, day, child_num):
        time = day.select(f'#session_tab > div:nth-child({child_num}) > div.body > div > div.time.text-center > div')[0].text
        return re.sub(r"\s", "", time)


    def get_proffesor(self, day, child_num):
        return day.select(f'#session_tab > div:nth-child({child_num}) > div.body > div > div.discipline > div > div > ul > li:nth-child(2) > a')[0].text


    def get_name_exam(self, day, child_num):
        return day.select(f'#session_tab > div:nth-child({child_num}) > div.body > div > div.discipline > div > div > ul > li:nth-child(1) > span')[0].text


    def get_location_in_university(self, day, child_num):
        university_location = day.select(f'#session_tab > div:nth-child({child_num}) > div.body > div > div.discipline > div > div > ul > li:nth-child(3) > a')[0].text
        return self.parse_cabinet(university_location)


    def get_location_in_city(self, day, child_num):
        return day.select(f'#session_tab > div:nth-child({child_num}) > div.body > div > div.discipline > div > div > ul > li:nth-child(3) > a')[0]['title']
    

    def get_type_discipline(self, day, child_num):
        type_disc = day.select(f'#session_tab > div:nth-child({child_num}) > div.body > div > div.discipline > div > div > ul > li:nth-child(1)')[0].text
        return self.parse_name_discipline(type_disc)
    

    def parse_cabinet(self, cabinet):
        cabinet = cabinet.replace('корп. ', '')
        cabinet = cabinet.replace(' каб. ', '-')
        cabinet = cabinet.replace('"', '')
        return cabinet
    

    def parse_name_discipline(self, name_discipline):
        type_discipline = name_discipline[ name_discipline.find('(') + 1 : name_discipline.find(')') ]
        if type_discipline not in ['Экзамен']:
            name_discipline = name_discipline.replace(f'({type_discipline})', '')
        return name_discipline[ name_discipline.find('(') + 1 : name_discipline.find(')') ]


    def check_session(self, soup):
        if soup[0].findChildren('h3'):
           self.session = None
           exit()
        return soup

