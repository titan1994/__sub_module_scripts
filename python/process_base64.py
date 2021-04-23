"""
Кодирование и декодирование base64
"""

from base64 import b64encode, b64decode


def data_to_base64_to_str(data):
    """
    Кодирование байт в base64 и возврат нормализованной строки для JSON
    :param data:
    :return:
    """

    return base64_str_file_normalize(str(b64encode(data)))


def data_from_str_base64_to_bytes(data):
    """
    Кодирование JSON строки содержащей base64 в набор байт/двоичных данных
    :param data:
    :return:
    """

    if isinstance(data, str):
        return b64decode(base64_str_file_normalize(data).encode())
    else:
        return data


def base64_str_file_normalize(data):
    """
    Предполагаем что на вход строка, которая начинается с буквы b
    :param data:
    :return:
    """

    if isinstance(data, str) and data.startswith('b'):
        return data[2:-1]

    return data