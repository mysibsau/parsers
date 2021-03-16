from lxml import html
from io import StringIO
from getters import get_books_from_library


def get_book_quantities(root):
    return len(root.cssselect('table.record'))


def get_author_name(root, num):
    # return soup.find_all('table', {'class': 'record'})
    # return soup.find_all('tr')
    
    return root.select('div.bo_div')[num].text


def get_physical_books(html: str) -> list:
    # временная переменная, потом убрать
    # content = get_books_from_library()

    root = html.parse(StringIO(content)).getroot()
    result = []

    for num in range(get_book_quantities):
        result.append({
            'author': get_author_name(root, num),
        })

    return result


if __name__ == '__main__':
    content = open('test.html').read()
    print(get_physical_books(content))
