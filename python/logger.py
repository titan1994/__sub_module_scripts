import shutil
from pathlib import Path
import logging
import os

FORMAT, DATE_FORMAT = "%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
LOG_DIR, LOG_NAME = "logs", "log.log"


log = logging.getLogger('Logger')


def _create_log_dir():
    path_to_log_dir = os.path.abspath(LOG_DIR)
    Path(path_to_log_dir).mkdir(parents=True, exist_ok=True)
    shutil.rmtree(path_to_log_dir)
    os.mkdir(path_to_log_dir)
    log_file = open(os.path.abspath(os.path.join(LOG_DIR, LOG_NAME)), 'tw')
    log_file.close()


def _setup_file_handler():
    _create_log_dir()
    formatter = logging.Formatter(FORMAT, datefmt=DATE_FORMAT)
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, LOG_NAME), encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)


def _setup_console_handler():
    console_formatter = logging.Formatter("%(log_color)s %(message)s", datefmt=DATE_FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    log.addHandler(console_handler)


def _setup_logstash_handler(host, port):
    from logstash_async.handler import AsynchronousLogstashHandler
    async_handler = AsynchronousLogstashHandler(host, port, database_path=None)
    log.addHandler(async_handler)


# example init logger
def setup_logger():
    _setup_console_handler()
    _setup_file_handler()
    _setup_logstash_handler(host='localhost', port=5000)
