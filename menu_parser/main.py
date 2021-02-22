from bs4 import BeautifulSoup
import requests


def get_menu_quantities(soup):
    '''Получение общего количества меню'''
    return len(soup.find_all('a', {'data-toggle': 'pill'}))


def get_name_room(soup, menu_num):
    return soup.select(f'#wrapwrap>main>div:nth-child(2)>div>ul>li:nth-child({menu_num+1})>a')[0].text


def get_sub_menu(soup, menu_num):
    '''Получение меню конкретной столовой'''
    return soup.find_all('div', {'class':'tab-pane'})[menu_num]


def get_tr_in_table(sub_menu):
    '''Получение всех строк из таблицы меню конкретной столовой'''
    return sub_menu.find_all('tr')[1:]


def get_name_dish(tr):
    return tr.find_all('td')[0].text


def get_weight(tr):
    return tr.find_all('td')[1].text


def get_price(tr):
    return float(tr.find_all('td')[2].text)


def get_type_name(tr):
    return tr.find('th').text.strip()


def menu_is_empty(soup):
    return len(soup.find_all('a', {'data-toggle': 'pill'})) == 0


def get_all_menu(html_file):
    soup = BeautifulSoup(open(html_file), 'html.parser')

    if menu_is_empty(soup):
        yield {'error': 'menu is empty'}

    for menu_num in range(get_menu_quantities(soup)):
        type_dish = None
        for tr in get_tr_in_table(get_sub_menu(soup, menu_num)):

            if tr.attrs.get('class') == ['active']:
                type_dish = get_type_name(tr)
            else:
                yield {
                    'type': type_dish,
                    'name': get_name_dish(tr),
                    'weight': get_weight(tr),
                    'price': get_price(tr),
                    'room': get_name_room(soup, menu_num)
                }


if __name__ == '__main__':
    for dish in get_all_menu('menu_all_1.html'):
        for key, value in dish.items():
            print(key, ":", value)
        print()
        print()
