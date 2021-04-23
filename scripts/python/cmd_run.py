"""
Для администрирования сервера. Выполнение команд операционной системы
В КОНТЕКСТЕ КОРНЯ ПРОЕКТА
"""

from subprocess import check_output, CalledProcessError, STDOUT, Popen, PIPE
from . import easy_scripts


def run(cmd, context=easy_scripts.PROJECT_GENERAL_FOLDER):
    """
    Команды операционной системы
    :param context:
    :param cmd:
    :return:
    """

    try:
        data_cmd = check_output(cmd, cwd=context.absolute(), shell=True, universal_newlines=True, stderr=STDOUT)
        status_cmd = 0

    except CalledProcessError as ex:

        data_cmd = ex.output
        status_cmd = ex.returncode

    if data_cmd[-1:] == '\n':
        data_cmd = data_cmd[:-1]

    data_cmd = data_cmd.encode(encoding='1251', errors='ignore')
    data_cmd = data_cmd.decode(encoding='IBM866', errors='ignore')

    return status_cmd, data_cmd


def run_with_answer(cmd, answer=b'y\r' * 100, context=easy_scripts.PROJECT_GENERAL_FOLDER):
    """
    Запуск команды с ответом

    :param cmd:
    :param answer:
    :param context:
    :return:
    """
    try:
        proc = Popen(cmd, cwd=context.absolute(), stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
        stdout, stderr = proc.communicate(input=answer, timeout=3)
        status, data = 0, stdout.decode()

    except Exception as exp:
        print('try run without answer')
        print(exp)
        status, data = run(cmd)

    return status, data
