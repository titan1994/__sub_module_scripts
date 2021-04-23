"""
Шаблонизатор
"""

from jinja2 import Environment, FileSystemLoader, BaseLoader
from os import makedirs
from pathlib import Path
import re


def jinja_render_to_file(src, dst, render, pattern_folder=None):
    """
    Рендер ниндзи из файла в файл по словарю
    """
    str_render = jinja_render_to_str(src=src, render=render, pattern_folder=pattern_folder)

    try:
        # Нидзя теперь умный - ниндзя сначала создаст все каталоги
        makedirs(Path(dst).parent)
    except FileExistsError:
        pass

    with open(dst, 'w', encoding='utf-8') as file:
        file.write(str_render)


def jinja_render_to_str(src, render, pattern_folder=None, smart_replace=False):
    """
    Рендер ниндзи из файла в строку по словарю
    Теперь с наследованием и импортом (extends/include)
    """

    if pattern_folder:
        env = Environment(loader=FileSystemLoader(Path(pattern_folder).absolute()))
    else:
        env = Environment(loader=FileSystemLoader(Path(src).parent.absolute()))

    template = env.get_template(Path(src).name)
    str_render = template.render(**render)

    if smart_replace:
        str_render = jinja_smart_replace(str_input=str_render)

    return str_render


def jinja_render_str_to_str(str_pattern, render, pattern_folder=None, smart_replace=False):
    """
    Рендер по строке. Строка в строку по словарю.
    Теперь с наследованием и импортом (extends/include)
    """

    if pattern_folder:
        env = Environment(loader=FileSystemLoader(Path(pattern_folder).absolute()))
    else:
        env = Environment(loader=BaseLoader)

    template = env.from_string(str_pattern)
    str_render = template.render(**render)
    if smart_replace:
        str_render = jinja_smart_replace(str_input=str_render)

    return str_render


def jinja_smart_replace(str_input):
    """
    Замена лишних пустот
    """
    return re.sub(r'[\r\n]+', '\r\n', str_input)
