"""
Функции установки дефолтов
"""


def default_dict(dict_v, key, value):
    """
    Значение словаря по умолчанию
    """

    res = dict_v.get(key)
    if not res:
        res = value
    return res
