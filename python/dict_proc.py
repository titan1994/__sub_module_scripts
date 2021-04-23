"""
Работа со словарями
"""

from dictdiffer import diff


def recombine_dict(old, new, change=True, add=True, remove=False):
    """
    Перекомпановка данных словаря новыми значениями.
    Все словари в итоге становятся одинаковыми old == new

    + change заменяет значения новыми
    + add добавляет новые пары ключ-значение
    + remove удаляет ключи

    Операция когда все три истина - это бред, точнее можно просто приравнять словари
    """
    if not isinstance(old, dict):
        old = {}

    if not isinstance(new, dict):
        new = {}

    processing_keys = []
    result_diff = get_dict_difference(old=old, new=new)

    if change and add and remove:
        old = new
        processing_keys = old.keys()
        return result_diff

    if not change and result_diff.get('change'):
        result_diff.pop('change')

    if not add and result_diff.get('add'):
        result_diff.pop('add')

    if not remove and result_diff.get('remove'):
        result_diff.pop('remove')

    for action, data in result_diff.items():
        if action == 'change' and change:
            for key, ch_dat in data.items():
                old[key] = ch_dat[old[key]]
                processing_keys.append(key)

        elif action == 'add' and add:
            for key, value in data.items():
                old[key] = value
                processing_keys.append(key)

        elif action == 'remove' and remove:
            for key, _ in data.items():
                old.pop(key)
                processing_keys.append(key)
    new = old
    return result_diff, processing_keys


def get_dict_difference(old, new):
    """
    Получить различия в словарях в формате:

    {
        "change": {
            "2": {
                "chicken": "chicken1"
            },
            "3": {
                "dog": "dog1"
            }
        },
        "add": {
            "77": "roll",
            "88": "back"
        },
        "remove": {
            "5": "ttt",
            "999": 222
        }
    }
    """
    diff_dict = {}

    if isinstance(old, dict):
        old_compare = old
    else:
        old_compare = {}

    if isinstance(new, dict):
        new_compare = new
    else:
        new_compare = {}

    for action, key, data in diff(first=old_compare, second=new_compare):
        dict_res = diff_dict.get(action)
        if dict_res is None:
            dict_res = {}

        if action == 'change':
            val_old, val_new = data

            if isinstance(key, str):
                key_save = key
            else:
                key_save = key[0]

            dict_res[key_save] = {val_old: val_new}
        else:
            for last_data in data:
                key_cur, val = last_data
                if key:
                    # Добавления в подуровни фиксировать как изменения
                    key_save = f'{key}.{key_cur}'
                    dict_change_res = diff_dict.get('change')
                    if dict_change_res is None:
                        dict_change_res = {}
                    dict_change_res[key_save] = val
                else:
                    key_save = key_cur
                    dict_res[key_save] = val

        diff_dict[action] = dict_res
    return diff_dict


# Пилотные тесты

# if __name__ == '__main__':
#     from json import dump as jsd
#
#     dict1 = {1: 'donkey', 2: 'chicken', 3: 'dog', 5: 'ttt', 999: 222}
#     dict2 = {1: 'donkey', 2: 'chicken1', 3: 'dog1', 77: 'roll', 88: 'back'}
#
#     report, _ = recombine_dict(old=dict1, new=dict2)
#
#     with open('diff.json', 'w', encoding='utf-8') as fb:
#         jsd(report, fb, ensure_ascii=False, indent=4)
#
#     with open('dict1.json', 'w', encoding='utf-8') as fb:
#         jsd(dict1, fb, ensure_ascii=False, indent=4)
#

