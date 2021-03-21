from lxml import html
from io import StringIO
from getters import get_books_from_library, get_book_holders
import re
import time
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool


def get_book_quantities(root: html.HtmlElement) -> int:
    return len(root.cssselect('table.record'))


def get_author_name(root: html.HtmlElement, num: int) -> str:
    if author := root.cssselect('div.bo_div')[num].cssselect('b')[1].text.strip():
        return author


def get_text(root: html.HtmlElement, num: int) -> str:
    return ' '.join([item.strip() for item in root.cssselect("div.bo_div")[num].xpath('./text()')]).strip()


def get_name_book(root: html.HtmlElement, num: int) -> str:
    return get_text(root, num)\
        .split('>> ')[-1]\
        .split('\xa0\xa0\xa0\xa0')[-1]\
        .split(':')[0]\
        .split('/')[0].strip()


def get_place_and_count(root: html.HtmlElement, num: int) -> tuple:
    '''Получение места хранения книги и их количество'''
    url_part = root.cssselect("div.bo_tabs")[num].xpath('./ul/li[2]/a')[0].get('href')
    content = get_book_holders(url_part)
    if not content:
        return None, None
    table = html.parse(StringIO(content)).getroot()
    place = table.cssselect("td.ex_full_name_cell")[0].text.strip()
    count = table.cssselect("td.ex_number_cell")[0].text.strip()
    return place.split('(')[-1][:-1].split(':')[0], int(count.strip())


def get_link(root: html.HtmlElement, num: int) -> str:
    '''Получение ссылки на полный текст'''
    text = get_text(root, num).strip()
    if protocol := re.findall(r"(http|https):", text)[0]:
        return protocol + text.split(protocol)[-1].split('(дата обращения')[0].strip()


def get_physical_books(content: str) -> list:
    root = html.parse(StringIO(content)).getroot()
    result = []

    pool = ThreadPool()

    books_count = range(get_book_quantities(root))
    books_storage = pool.map(partial(get_place_and_count, root), books_count)

    for num in books_count:
        author = get_author_name(root, num)
        name = get_name_book(root, num)
        place, count = books_storage[num]

        if not all((author, name, place, count)):
            continue

        result.append({
            'author': author,
            'name': name,
            'place': place,
            'count': count,
        })

    return result


def get_digital_books(content: str) -> list:
    root = html.parse(StringIO(content)).getroot()
    result = []

    for num in range(get_book_quantities(root)):
        author = get_author_name(root, num)
        name = get_name_book(root, num)
        url = get_link(root, num)

        if not all((author, name, url)):
            continue

        result.append({
            'author': author,
            'name': name,
            'url': url,
        })

    return result


if __name__ == '__main__':
    start_time = time.time()
    content = get_books_from_library(key_words='программирование', physical=True)
    
    for book in get_physical_books(content):
        for key, value in book.items():
            print(key, ':', value)
        print()
    end_time = time.time()
    print(f'TIME: {end_time-start_time}')
