import requests
from random import randint


SEARCH_BROADCAST_URL = 'http://biblioteka.sibsau.ru/jirbis2/components/com_irbis/ajax_provider.php'


def get_random_req_id_client():
    return randint(1, 900000)


def get_books_from_library(key_words: str = 'программирование', physical: bool = True) -> str:
    if not physical:
        response = requests.get(
            f'http://biblioteka.sibsau.ru/jirbis2/components/com_irbis/ajax_provider.php?task=set_selected_bases&bl_id_array_selected%5B1%5D=3&bl_id_array_selected%5B11%5D=11&_=1615539096378'
        )

    req_id_client = get_random_req_id_client()

    requests.post(
        SEARCH_BROADCAST_URL,
        data={
            'fasets': '',
            'req_static': 1,
            'keywords': key_words,
            "task": 'search_broadcast',
            "first_number": 1,
            "req_id_client": req_id_client,
            "selected_search_flag": 0,
        },
    )
    SHOW_RESULTS_URL = f'http://biblioteka.sibsau.ru/jirbis2/components/com_irbis/ajax_provider.php?task=show_results&req_id_client={req_id_client}&first_number=1&recs_outputed=0&reqs_outputed=0&last_output_time=0&finish_flag=last&_=1615539096361'
    response = requests.get(SHOW_RESULTS_URL).json()

    return response['recs']


'''def get_books(key_word: str, physical: bool = True) -> list:
    html = get_books_from_library(key_word, physical)
    if physical:
        return parser.get_physical_books(html)
    return parser.get_digital_books(html)'''



if __name__ == '__main__':
    print(get_books_from_library('Программирование', True))
    # print(get_books_from_library('Программирование', False))