import os
import shutil
import string
import random

import logging
from . import Proxy

"""
ProxyConnectorExtension is a class that generates a temporary folder with a
Chrome extension that can be used to connect to a proxy server.

The class takes a :class:`Proxy` object as parameter and generates a temporary
folder with the following structure:

.. code-block:: bash

    extension_dir/
        manifest.json
        background.js

The manifest.json file contains the basic information about the extension,
while the background.js file contains the code that will be executed in the
background to set the proxy configuration.

The class provides the following methods:

- :meth:`get_extension_dir`: returns the path of the temporary folder
- :meth:`remove_extension_dir`: removes the temporary folder
- :meth:`__del__`: removes the temporary folder when the instance is deleted

The class is designed to be used as a context manager, so you can use it in a
with statement to ensure that the temporary folder is removed when you are
done with it.

Example:

.. code-block:: python

    with ProxyConnectorExtension(proxy) as ext_dir:
        # Do something with the extension
        pass
"""

logger = logging.getLogger(__name__)


class ProxyConnectorExtension:
    def __init__(self, proxy: Proxy):
        logger.info("ProxyConnectorExtension init")
        from src.GLOBAL import GLOBAL

        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        logger.info(f"unique_id: {unique_id}")
        extension_file_dir = os.path.abspath(
            os.path.join(GLOBAL.PATH.APPLICATION_ROOT, 'proxy_extensions')
        )
        logger.info(f"extension_file_dir: {extension_file_dir}")
        self.__ext_dir = os.path.join(extension_file_dir, f'{unique_id}-proxy-connector')
        logger.info(f"self.__ext_dir: {self.__ext_dir}")

        if not isinstance(proxy, Proxy):
            logger.error("Proxy must be instance of twitter.Proxy, not {}".format(type(proxy)))
            return

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"76.0.0"
        }
        """
        logger.info(f"manifest_json initialized")

        background_js = """
        let config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy.host, proxy.port, proxy.username, proxy.userpass)
        logger.info(f"background_js initialized")

        """
        Check is everything correct with the self.__zip_path
        """
        os.makedirs(self.__ext_dir)
        logger.info("self.__ext_dir created")

        with (open(os.path.join(self.__ext_dir, 'manifest.json'), 'w') as m_fs,
              open(os.path.join(self.__ext_dir, 'background.js'), 'w') as b_fs):
            logger.info("manifest.json and background.js created")
            m_fs.write(manifest_json)
            logger.info("manifest.json written")
            b_fs.write(background_js)
            logger.info("background.js written")

    def get_extension_dir(self):
        logger.info("extension dir")
        return self.__ext_dir

    def remove_extension_dir(self):
        logger.info("remove extension dir")
        try:
            shutil.rmtree(self.__ext_dir)
        except Exception as ex:
            logger.warning(f"Failed to remove extension dir: {ex}")

    def __del__(self):
        """
        Remove the extension dir if instance was deleted
        """
        self.remove_extension_dir()
