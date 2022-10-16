#!/usr/local/bin/python3
from datetime import datetime, timedelta
import random
import itertools


# OBJECT NEED TO RETURN
"""
{
start: '2022-07-29',
end: '2022-07-29',
title: 'Postagem no Facebook',
content: '<i class="v-icon material-icons">facebook</i>',
class: 'facebook'
}
"""


def generate_random_cal():
    WEEK_DAYS = {
        '5': 'Sexta-Feira',
        '6': 'Sábado',
        '0': 'Domingo',
        '1': 'Segunda-Feira',
        '2': 'Terça-Feira',
        '3': 'Quarta-Feira',
        '4': 'Quinta-Feira'
    }

    DICT_MODEL = {
        "facebook": {
            "title": 'Postagem no Facebook',
            "content": '<i class="fab fa-facebook"></i>',
            "class": 'facebook'
        },
        "instagram": {
            "title": 'Postagem no Instagram',
            "content": '<i class="fab fa-instagram"></i>',
            "class": 'instagram'
        },
        "youtube": {
            "title": 'Video no Youtube',
            "content": '<i class="fab fa-youtube"></i>',
            "class": 'youtube'
        },
        "email": {
            "title": 'Email para...',
            "content": '<i class="fas fa-envelope"></i>',
            "class": 'email'
        },
    }
    #-----KEYS OFF MIDIAS-----#
    key_dict_midia = [x for x in DICT_MODEL.keys()]
    print('Chaves das Mídias:')
    print(key_dict_midia)
    print('\n')
    for k, v in DICT_MODEL.items():
        print(f'{k}: {v}')
    """
    print(DICT_MODEL['facebook'])
    print(DICT_MODEL[key_dict_midia[0]])
    print(DICT_MODEL['email'])
    """

    # RANDOM POSTS FOR EACH DAY

    def get_random_posts(final):
        return random.randint(2, final)

    # RANDOM POSTS FOR EACH DAY

    def mix_all_days(days, numbers):
        new_list = [days for i in range(0, numbers)]
        return new_list

    # DEFINE VARS TO USE IN FUNCTIONS
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    dead_line = 15
    last_date = timedelta(days=dead_line)
    last_date = (now + last_date).strftime("%d/%m/%Y")
    print('Amanhã: ')
    print(tomorrow.strftime("%d/%m/%Y"))
    print('Last Date: ')
    print(last_date)

    #-----STARTING LOGIC ALEATORY-----#

    #-----DATE LIST OF NEXT 15 DAYS-----#

    list_date = [((tomorrow + timedelta(days=i)).strftime("%Y-%m-%d"))
                 for i in range(dead_line)]
    print('\n')

    final_list = []
    for i in list_date:
        days = mix_all_days(i, get_random_posts(4))
        final_list.append(days)
    final_list = list(itertools.chain.from_iterable(final_list))
    print('\n')

    list_date = [({'date': day, 'dateweek': ((datetime.strptime(day, "%Y-%m-%d")).strftime("%w"))})
                 for day in final_list]

    for i in list_date:
        midia = key_dict_midia[random.randint(0, 3)]
        i['calevents'] = DICT_MODEL[midia]

    final_result = []
    for i in list_date:
        new_dict = {}
        date_cal = i['date']
        new_dict['class'] = i['calevents']['class']
        new_dict['content'] = i['calevents']['content']
        new_dict['title'] = i['calevents']['title']
        new_dict['end'] = date_cal
        new_dict['start'] = date_cal
        final_result.append(new_dict)

    return final_result


if __name__ == '__main__':
    resultado = generate_random_cal()
    for i in resultado:
        print(i)
