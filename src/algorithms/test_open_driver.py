import time

from src.GLOBAL import GLOBAL
from src.driver.driver import BaseSeleniumDriver


def open_driver():
    new_driver = BaseSeleniumDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, headless=False,
                                    window_size=(400, 700))

    new_driver.create_instance()
    new_driver.get("https://youtube.com/")
    time.sleep(10)
    new_driver.quit()

