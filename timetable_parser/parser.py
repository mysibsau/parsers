from bs4 import BeautifulSoup
import requests
import re


class Parser:
    def __init__(self):
        self.timetable = {
            'timetable': {
                'week_1': {
                    'monday': [],
                    'tuesday': [],
                    'wednesday': [],
                    'thursday': [],
                    'friday': [],
                    'saturday': [],
                },
                'week_2': {
                    'monday': [],
                    'tuesday': [],
                    'wednesday': [],
                    'thursday': [],
                    'friday': [],
                    'saturday': [],
                }
            },
            'session': {}
        }


    def get_int_subgroup(self, string):
        '''Из строки возвращает целочисленный номер группы''' 
        for symbol in string:
            if symbol.isdigit():
                return int(symbol)


    def delete_repeats(self, subjects):
        '''Избавляет от дублирования наименований премдметов'''
        if subjects.count( subjects[0] ) == len(subjects):
            return [subjects[0]]
        return subjects


    def get_subgroup(self, sub_subject):
        '''Получение подгруппы'''
        subgroup = None

        if sub_subject.find('i', {'class': 'fa-paperclip'}) is not None:
            subgroup = self.get_int_subgroup(sub_subject.find_all('li')[-1].text)
        
        if sub_subject.find('li', {'class': 'num_pdgrp'}) is not None:
            subgroup = self.get_int_subgroup(sub_subject.find('li', {'class': 'num_pdgrp'}).text)
        
        return subgroup


    def parse_type_of_subject(self, name_subject):
        return name_subject[ name_subject.find('(') + 1 : name_subject.find(')') ]


    def parse_cabinet(self, cabinet):
        cabinet = cabinet.replace('корп. ', '')
        cabinet = cabinet.replace(' каб. ', '-')
        cabinet = cabinet.replace("\"", "")
        return cabinet


    def get_timetable_for_group(self, id):
        '''Получение расписания'''

        html = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/group/{id}'
        ).text

        soup = BeautifulSoup(html, 'html.parser')

        for numb_week in range(1, 3):
            days = self.timetable['timetable'][f'week_{numb_week}']
            for day in days.keys():

                # Проверка на выходной день
                try:
                    day_timetable_html = soup.select(f'#week_{numb_week}_tab > div.day.{day} > div.body')[0]
                except IndexError:
                    days[day].append({'weekend': 'Отдыхайте'})
                    continue

                div_line = day_timetable_html.find_all('div', {'class': 'line'})

                for line in div_line:
                    # Парсинг времени
                    time = re.sub(r"\s", "", line.find('div', {'class': 'hidden-xs'}).text)

                    # Получение предметов, которые стоят в одно время
                    div_row = line.find('div', {'class': 'row'})
                    subjects = div_row.find_all('div')
                    
                    teachers = []
                    name_subjects = []
                    type_subjects = []
                    subgroups = []
                    location_in_university = []
                    location_in_city = []

                    for sub_subject in subjects:
                        
                        # Получение названия предмета
                        name = sub_subject.find('span', {'class': 'name'}).text
                        name_subjects.append( name )

                        # Получение типа предмета
                        type_subject = self.parse_type_of_subject( sub_subject.find('span', {'class': 'name'}).parent.text )
                        type_subjects.append( type_subject )

                        # Получение преподов
                        teachers.append( sub_subject.find('a').text )

                        # Местоположение
                        location_in_university.append( self.parse_cabinet(sub_subject.find('a', {'href':'#'} ).text) )
                        location_in_city.append( sub_subject.find('a', {'href':'#'} )['title'] )

                        subgroups.append( self.get_subgroup(sub_subject) )
                    
                    # Добавление данных в структуру
                    days[day].append({
                        'time': time,
                        'name_subjects': self.delete_repeats(name_subjects),
                        'type_subjects': self.delete_repeats(type_subjects),
                        'teachers': teachers,
                        'subgroups': subgroups,
                        'location_in_university': self.delete_repeats(location_in_university),
                        'location_in_city': self.delete_repeats(location_in_city)
                    })
                
        return self.timetable
