import re
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions

import logging

from src.proxy import ProxyABC, Proxy, EmptyProxy
from src.proxy.connector import ProxyConnectorExtension
from src.utils.bot.scrollers import VerticalScroller
from src.utils.selenium import driver_processes

from src.exceptions.driver import TryAgainPageError, BrowserClosedError

"""
This module contains the BaseSeleniumDriver class, which is an extension of the Chrome class from the
undetected-chromedriver package.

This class is designed to be used with the Chrome web browser and provides additional functionality beyond what is
available in the undetected-chromedriver package.

The main purpose of this class is to provide a way to interact with the Chrome browser in a way that is not detectable
by web services that try to detect and block automation scripts.

The class provides methods for navigating to a URL, clicking on an element, submitting a form, and getting the page
source.

The class also provides methods for waiting for certain conditions to be met, such as waiting for an element to be
visible or waiting for a page to finish loading.

The class also provides methods for handling common issues that arise when interacting with web pages, such as
handling pop-up windows and handling pages that try to detect and block automation scripts.

The class is designed to be easy to use and provides a simple and intuitive API for interacting with the Chrome browser.
"""

class BaseSeleniumDriver(uc.Chrome):
    """
    Connects to chrome executable as debugger to control it.
    Has methods for effective control chrome for parsing tweeter.
    """

    def __init__(
            self,
            executable_path: str,
            proxy: ProxyABC = EmptyProxy,  # here is can be EmptyProxy or valid Proxy
            user_agent: str = '',
            headless=True,
            window_size=(400, 700),
            logger=None,
    ):
        self.executable_path = executable_path
        self.proxy = proxy
        self.user_agent = user_agent
        self.headless = headless
        self.window_size = window_size
        self.logger = logger or logging.getLogger(__name__)

        self.vertical_scroller = VerticalScroller(self)
        self.instance_exist = False

    def create_instance(self):
        try:
            self.__create_instance()
        except selenium.common.exceptions.WebDriverException as error:
            if 'supports chrome version' in str(error).lower():
                versions_msg_part = str(error)[str(error).lower().find('supports chrome version'):]
                versions = [match.group() for match in re.finditer(r'[\d.]+', versions_msg_part)]
                if len(versions) > 1:
                    supports_version, current_version = versions[:2]
                    raise TryAgainPageError(f"Your Chrome version is: {current_version}<br>"
                                            f"Please install Chrome {supports_version} for stable operation.")
                else:
                    raise TryAgainPageError("An error has occurred, likely related to your Chrome version.")
        except TypeError as error:
            if 'binary location must be a string' in str(error).lower():
                raise TryAgainPageError("Failed to find Chrome on your PC. Please install Chrome.")

    def __create_instance(self):
        self.logger.debug("Creating driver instance..")
        if self.instance_exist:
            return self.logger.warning("The instance of this driver already created! "
                                       "Can't create new, before quit() from existing")

        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--disable-blink-features=BlockCredentialedSubresources')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-media")
        options.add_argument('--no-sandbox')
        options.add_argument("--mute-audio")
        options.add_argument("--lang=en")

        if self.headless:
            options.add_argument('--headless')

        if self.user_agent not in ['']:
            options.add_argument(f'user-agent={self.user_agent}')

        if isinstance(self.proxy, Proxy):
            proxy_connector = ProxyConnectorExtension(self.proxy)
            options.add_argument(f'--load-extension={proxy_connector.get_extension_dir()}')

        service = Service(self.executable_path)

        super().__init__(
            options=options,
            service=service,
        )

        self.set_page_load_timeout(60)
        self.set_window_size(*self.window_size)
        self.instance_exist = True

        # hide undetected_chromedriver`s console window
        driver_processes.hide_drivers_command_prompt()

    def get(self, url: str):
        """
        Gets page with passing "Try again" page.

        Raises:
             - TryAgainPageError when can't pass "Try Again"  page.
        """
        self.logger.info('Selenium get page')
        super().get(url)
        try:
            for _ in range(10):
                WebDriverWait(self, 7).until(
                    EC.visibility_of_element_located((By.XPATH, '//span[text()="Try again"]'))
                )
                self.refresh()

            raise TryAgainPageError("There were 10 unsuccessful attempts to pass through the 'Try Again'  page, "
                                    "unable to reach the final page.")
        except:
            pass

    def quit(self):
        self.logger.info('Selenium quit')
        self.instance_exist = False
        try:
            super().quit()
        except Exception as e:
            pass

    def wait_for_window(self, timeout=30):
        """
        Waits for the browser window to remain open for a certain period.
        Raises a BrowserClosedError if the window is closed unexpectedly.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if not self.window_handles:
                    raise BrowserClosedError("The browser window was closed unexpectedly.")
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error while checking if the window is open: {e}")
                raise

            time.sleep(1)
