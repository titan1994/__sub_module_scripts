"""
Инспектирование модулей, поиск имен, пакетов.
Задание пути для файла относительно корня проекта.

Запуск питона питоном. НЕ ПЕРЕМЕЩАТЬ, чтобы не сломать path_general_folder
Hello World
"""

from pathlib import Path
from inspect import getmembers, isclass
from pkgutil import iter_modules
from importlib import import_module
from os import system as system
from sys import executable as __python_path


def get_module_system(name):
    """
    Получить указанный модуль

    :param name: __name__
    :return:
    """
    from sys import modules
    return modules[name]


def get_path_parent_module(name):
    """
    Получить путь к родительской папке, где лежит модуль
    :param name:
    :return:
    """

    model_path = [scan[1] for scan in getmembers(get_module_system(name)) if scan[0] == '__file__']
    return Path(model_path[0]).parent


def path_file_name_module(name, *args):
    """
    Возвращает объект-путь к файлу относительно директории указанного скрипта
    :param args: Папка, файл, расширение, всё вместе или отдельно, вобщем как удобно
    :return: Path
    """
    pro_folder = get_path_parent_module(name)
    for name in args:
        pro_folder = pro_folder / name

    return pro_folder


PROJECT_GENERAL_FOLDER = path_file_name_module(__name__).parent.parent  # На тоненького


def path_general_folder(alt_folder=''):
    """
    Возвращает путь к основной папке текущего проекта, для проектов с виртуальным окружением
    Заточено под пайчарм. Есть возможность переопределить имя корневой папки всех проектов, задав
    alt_folder
    """

    if alt_folder == '':
        gen_fold_name = PROJECT_GENERAL_FOLDER  # На тоненького
    else:
        gen_fold_name = alt_folder

    py_path = str(Path().cwd())
    path_global_folder = Path(gen_fold_name)
    name_global_folder = path_global_folder.name

    if name_global_folder in py_path:
        # Проект был создан в виртуальном окружении

        parent_path, find_pass = py_path.split(name_global_folder)
        return Path(parent_path) / path_global_folder / Path(find_pass).parts[1]

    # Проект глобальный - вернуть окружение скрипта
    return Path().cwd()


def path_file(*args):
    """
    Возвращает объект-путь к файлу, который находится в проекте
    :param args: Папка, файл, расширение, всё вместе или отдельно, вобщем как удобно
    :return: Path
    """
    pro_folder = path_general_folder()
    for name in args:
        pro_folder = pro_folder / name

    return pro_folder


def get_module_path(module):
    """
    Путь к модулю, который был импортирован. Распространяется и на пакеты
    :param module:
    :return:
    """
    model_path = [scan[1] for scan in getmembers(module) if scan[0] == '__path__']
    return model_path[0]._path[0]


def get_module_name(module):
    """
    Имя модуля, который был импортирован. Распространяется и на пакеты
    :param module:
    :return:
    """
    model_path = [scan[1] for scan in getmembers(module) if scan[0] == '__name__']
    return model_path[0]


def get_module_from_pack(pack):
    """
    Все имена пакетов модуля
    :param pack:
    :return:
    """
    path_pack = [get_module_path(pack)]

    module_list = []
    for (_, name, _) in iter_modules(path_pack):
        module_list.append(name)

    return module_list


def get_all_class_from_pack(imported_pack):
    """
    Список всех классов модулей внутри пакета в виде объектов
    :param imported_pack:
    :return:
    """
    list_of_class = []
    for name in get_module_from_pack(imported_pack):
        mod = import_module('.' + name, get_module_name(imported_pack))
        class_models = (m[1] for m in getmembers(mod, isclass) if m[1].__module__ == mod.__name__)
        for class_obj in class_models:
            list_of_class.append(class_obj)

    return list_of_class


def get_all_class_from_pack_dict(imported_pack):
    """
    Список всех классов модулей внутри пакета в виде объектов
    :param imported_pack:
    :return:
    """
    dict_of_class = {}
    for name in get_module_from_pack(imported_pack):
        mod = import_module('.' + name, get_module_name(imported_pack))
        class_models = (m[1] for m in getmembers(mod, isclass) if m[1].__module__ == mod.__name__)
        for class_obj in class_models:
            dict_of_class[class_obj.__name__] = class_obj

    return dict_of_class


def get_python_pass():
    """
    Путь к питону
    """

    return __python_path


def run_python_file(python_file, params=''):
    """
    Запуск питона питоном
    Args:
        python_file:
        params:
    """
    python_pass = get_python_pass()

    file_run_pass = '{} {} {}'.format(Path(python_pass), Path(python_file), params)
    try:
        result_run = system(file_run_pass)
        return result_run

    except Exception as info:
        print(file_run_pass)
        print(info)
        return None
