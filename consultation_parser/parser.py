from bs4 import BeautifulSoup
import requests
import re


class ParseConsultation:
    def __init__(self):
        self.consultation = {
            'week_1': [],
            'week_2': []
        }


    def get_days(self, numb_week, id):
        response = requests.get(
            f'https://timetable.pallada.sibsau.ru/timetable/professor/{id}'
        ).text
        soup = BeautifulSoup(response, 'html.parser')

        if not self.is_consultation(soup):
            return None

        return soup.select(f'#cs_week_{numb_week}_tab > div.day')


    def get_consultation(self, id):
        for numb_week in range(1, 3):
            week = self.consultation[f'week_{numb_week}']

            days = self.get_days(numb_week, id)
            if days is None:
                return None

            for day in days:
                week.append({
                    'day': self.get_consult_day(day),
                    'time': self.get_consult_time(day),
                    'location_in_university': self.get_location_in_university(day),
                    'location_in_city': self.get_location_in_city(day)
                })
        
        
        return self.consultation


    def get_consult_day(self, day):
        name_day = day.find('div', {'class': 'name'}).find('div').text
        return re.sub(r"\s", "", name_day)


    def get_consult_time(self, day):
        time = re.sub(r"\s", "", day.find('div', {'class': 'visible-xs'}).text)
        if not len(time) > 5:
            return time
        return time[:5] + ' - ' + time[5:]


    def get_location_in_university(self, day):
        return self.parse_cabinet(day.find('a', {'href': '#'}).text)


    def get_location_in_city(self, day):
        return day.find('a', {'href': '#'})['title']


    def parse_cabinet(self, cabinet):
        cabinet = cabinet.replace('корп. ', '')
        cabinet = cabinet.replace(' каб. ', '-')
        cabinet = cabinet.replace('"', '')
        return cabinet


    def is_consultation(self, soup):
        if soup.find('h3', {'class': ''}):
           return None
        return True

