from lxml import html
from io import StringIO
from getters import get_books_from_library


def get_book_quantities(root):
    return len(root.cssselect('table.record'))


def get_author_name(root, num):
    if author := root.cssselect('div.bo_div')[num].cssselect('b')[1].text.strip():
        return author


def get_name_book(root, num):
    text = ' '.join([item.strip() for item in root.cssselect("div.bo_div")[num].xpath('./text()')]).strip()
    return text\
        .split('>> ')[-1]\
        .split('\xa0\xa0\xa0\xa0')[-1]\
        .split(':')[0]\
        .split('/')[0].strip()


def get_physical_books(content: str) -> list:
    # временная переменная, потом убрать
    # content = get_books_from_library()

    root = html.parse(StringIO(content)).getroot()
    result = []

    for num in range(get_book_quantities(root)):
        result.append({
            'author': get_author_name(root, num),
            'name': get_name_book(root, num),
        })

    return result


if __name__ == '__main__':
    content = get_books_from_library()
    for book in get_physical_books(content):
        for key, value in book.items():
            print(key, ':', value)
        print()
