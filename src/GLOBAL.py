import os
import sys
from enum import Enum

class GLOBAL:
    class PATH:
        APPLICATION_ROOT = f'{os.path.expanduser('~/Instagram_greetings_with_AI')}'
        SQLITE_DATABASE_PATH = f'{APPLICATION_ROOT}/accounts.db'
        LOGS = f'{APPLICATION_ROOT}/log.txt'
        BOT_LOGS_ROOT = f'{APPLICATION_ROOT}/botLogs'
        STATISTIC_PATH = f'{APPLICATION_ROOT}/botStatistic'
        BANLIST = f'{APPLICATION_ROOT}/banlist.txt'
        CHROMEDRIVER_PATH = f'{APPLICATION_ROOT}/chromedriver.exe'
        SETTINGS_PATH = f'{APPLICATION_ROOT}/settings.json'

        @classmethod 
        def get_resource(cls, relative_path: str):
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath("..")
            return os.path.join(base_path, relative_path)

        @classmethod
        def get_bot_log_path(cls, bot) -> str:
            return os.path.join(cls.BOT_LOGS_ROOT, f'{bot.name}.{bot.id}.txt')

        @classmethod
        def get_bot_statistic_path(cls, bot) -> str:
            return os.path.join(cls.STATISTIC_PATH, f'{bot.name}.{bot}.json')

    class BOT_MODE:
        DEFAULT = 'default'
        RECEIVER = 'receiver'
        DONOR = 'donor'