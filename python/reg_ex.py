"""
Полезные трюки с регулярками
"""

from re import compile as re_compile


def comb_file_name(name):
    """
    Причёсываем имя файла регулярным выражением
    """
    pattern = re_compile('[^\w+\d+]')
    res = pattern.sub(string=name, repl='')
    return res
