from bs4 import BeautifulSoup
import re
from getters import get_books_from_library


def get_book_quantities(soup):
    return len(soup.find_all('table', {'class': 'record'}))


def get_author_name(soup, num):
    return soup.find_all('div', {'class': 'bo_div'})[num].text
    #return soup.select('#bo_tab-2145830616 > div.bo_div > b:nth-child(3)')


def get_digital_books(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')


def get_physical_books(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    result = []

    for num in range(get_book_quantities(soup)):
        result.append({
            'author': get_author_name(soup, num),
        })

    return result


if __name__ == '__main__':
    for item in get_physical_books(get_books_from_library('программирование', True)):
        print(item)
