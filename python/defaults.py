"""
Функции установки дефолтов
"""


def default_dict(dict_v, key, value):
    """
    значение словаря по умолчанию - велосипед
    """
    res = dict_v.get(key)
    if res is None:
        res = value
    return res
