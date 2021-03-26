import requests
from random import randint


BASE_URL = 'http://biblioteka.sibsau.ru'


def get_random_req_id_client() -> int:
    return randint(1, 900000)


def get_books_from_library(key_words: str, physical: bool = True) -> str:
    if not physical:
        requests.get(
            BASE_URL + '/jirbis2/components/com_irbis/ajax_provider.php',
            params={
                'task': 'set_selected_bases',
                'bl_id_array_selected[1]': 3,
                'bl_id_array_selected[11]': 11,
            }
        )

    req_id_client = get_random_req_id_client()

    requests.post(
        BASE_URL + '/jirbis2/components/com_irbis/ajax_provider.php',
        data={
            'fasets': '',
            'req_static': 1,
            'keywords': key_words,
            'task': 'search_broadcast',
            'first_number': 1,
            'req_id_client': req_id_client,
            'selected_search_flag': 0,
        },
    )

    response = requests.get(
        BASE_URL + '/jirbis2/components/com_irbis/ajax_provider.php',
        params={
            'task': 'show_results',
            'req_id_client': req_id_client,
            'first_number': 1,
            'recs_outputed': 0,
            'reqs_outputed': 0,
            'last_output_time': 0,
            'finish_flag': 'last'
        }
    )

    if response.status_code == 200:
        return delete_bo_lighting_tag(response.json()['recs'])


def delete_bo_lighting_tag(html: str) -> str:
    return html.replace("<span class=\"bo_lighting\">", '')


def get_book_holders(url_part: str) -> str:
    headers = {
        'Accept': "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.2.636315675.1608545000; f_search_mode=STEASY; JSESS3=7ecc3798b86b9b879eef0360f4e63a7b; cltid=1529; trcusr=155; e7b861d63c4aad58e88ad02684ae99d0=9c3ae27386f8e67fdda04ce675048c56; js_vsid=4917",
        "Host": "biblioteka.sibsau.ru",
        "Referer": "http://biblioteka.sibsau.ru/jirbis2/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests.get(url=BASE_URL+url_part, headers=headers)
    if response.status_code == 200:
        return response.text


'''def get_books(key_word: str, physical: bool = True) -> list:
    html = get_books_from_library(key_word, physical)
    if physical:
        return parser.get_physical_books(html)
    return parser.get_digital_books(html)'''


if __name__ == '__main__':
    print(get_books_from_library(key_words='Ефремов', physical=True))
    # print(get_books_from_library('Программирование', False))