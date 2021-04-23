"""
Руслан.
Прототип очистки мусора.
Потенциальная заявка на создание файла APP_RUN/CLEAR.py
"""

import glob
from __scripts.python.easy_scripts import PROJECT_GENERAL_FOLDER
from APP_RUN.GENERAL_CONFIG import GeneralConfig, FastApiConfig
from pathlib import Path
import shutil


def migration_clear():
    """
    Удаление файлов миграций
    :return:
    """

    if FastApiConfig in GeneralConfig.__bases__:
        delete_in_folder(FastApiConfig.DEFAULT_AERICH_MIGR_PATH, gitkeep=True)
        delete_file(PROJECT_GENERAL_FOLDER / "aerich.ini")
        delete_file(PROJECT_GENERAL_FOLDER / "APP_RUN" / "aerich.ini")

    # elif QuartApiConfig in GeneralConfig.__bases__:
    #     delete_in_folder(QuartApiConfig.ALEMBIC_CATALOG_ALEMBIC, gitkeep=True)
    #     delete_file(PROJECT_GENERAL_FOLDER / "APP_RUN" / "alembic.ini")


def delete_in_folder(path, gitkeep=False):
    files = glob.glob(str(path) + '\*')
    for f in files:
        if Path(f).is_file():
            Path(f).unlink()
        else:
            shutil.rmtree(f)
    if gitkeep:
        open(Path(path) / '.gitkeep', 'w').close()


def delete_file(path):
    if Path(path).exists() and Path(path).is_file():
        Path(path).unlink()
    else:
        print('Path remove already:', str(path))


if __name__ == '__main__':
    migration_clear()
