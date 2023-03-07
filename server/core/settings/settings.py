import os
from os.path import join

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

NEED_NEW_BASE = False

# Настройки локальной базы
LOCAL_BASE_HOST = '10.0.2.18'
LOCAL_BASE_NAME = 'academy'
LOCAL_BASE_USER_NAME = os.environ.get('LOCAL_BASE_USER_NAME')
LOCAL_BASE_USER_PASSWORD = os.environ.get('LOCAL_BASE_USER_PASSWORD')
LOCAL_BASE_DRIVER = 'mysql+asyncmy'

# Настройки сервера
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9000

