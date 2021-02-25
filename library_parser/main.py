from bs4 import BeautifulSoup
import re


def get_book_quantities(soup):
    """Получение книг на странице"""
    return len(soup.find_all('input', {'name': "MFN"}))


def get_parent(soup):
    return soup.find_all('input', {'name': "MFN"})[0].parent.parent.text


def get_text(soup, num):
    """Получение текста под названием книги"""
    return soup.find_all('input', {'name': "MFN"})[num].parent.parent.text


def get_name_book(soup, num):
    return get_text(soup, num)\
        .split('/')[0]\
        .split('\xa0\xa0\xa0\xa0')[-1]\
        .split(': пер')[0]\
        .split('[Электронный ресурс]')[0]\
        .split('[Electronic resource]')[0]\
        .split(':')[0].strip()


def get_link(soup, num):
    if link := soup.find_all('input', {'name': "MFN"})[num].parent.parent.find_all('a', {'target': '_blank'}):
        return link[0]['href']
    else:
        return None


def get_author_name(soup, num):
    if name := soup.find_all('input', {'name': "MFN"})[num].parent.parent.find_all('a', {'class':"term_hyper"}):
        return name[0].text
    elif name := soup.find_all('input', {'name': "MFN"})[num].parent.parent.select('b:nth-child(5)'):
        return name[0].text
    else:
        return None


def get_place(soup, num):
    tickets = {
        'УА': 'Л 208',
        'СЭА': 'Л 203',
        'НА': 'Л 204',
        'ХА': 'Л 208',
        'ХР': 'Л 208'
    }
    place = soup.find_all('input', {'name': "MFN"})[num].parent.parent.text\
            .split('Имеются экземпляры в отделах: ')[-1]\
            .split(')')[0]\
            .split('(')[0]

    return tickets.get(place, None)


def get_count(soup, num):
    try:
        count = int(
            soup.find_all('input', {'name': "MFN"})[num].parent.parent.text\
                .split('Имеются экземпляры в отделах: ')[-1]\
                .split(')')[0]\
                .split('(')[-1]
        )
    except ValueError:
        return 0
    return count


def get_all_books(html_file):
    soup = BeautifulSoup(open(html_file, encoding='cp1251'), 'html.parser')
    for num in range(get_book_quantities(soup)):
        yield {
            'author': get_author_name(soup, num),
            'name': get_name_book(soup, num),
            'url': get_link(soup, num),
            'place': get_place(soup, num),
            'count': get_count(soup, num)
        }


if __name__ == '__main__':
    for book in get_all_books('IZDV.html'):
        for key, value in book.items():
            print(key, ":", value)
        print()
