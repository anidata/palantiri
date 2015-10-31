# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib.request
import time
import selenium.webdriver

from . import errors
from . import common

class Engine(object):
    def get_page_source(self, url):
        raise errors.EngineError("get_page_source not implemented")

    def cleanup(self):
        return

class DefaultEngine(Engine):
    def __init__(self, data = None, headers = {}, origin_req_host = None,
            unverifyable = False, method = None):
        self.data = data
        self.headers = headers
        self.origin_req_host = None
        self.unverifyable = False
        self.method = None
        return

    def get_page_source(self, url):
        req = urllib.request.Request( url, self.data, self.headers,
                self.origin_req_host, self.unverifyable, self.method)
        return common.Website(url, urllib.request.urlopen(req).read())

class BaseSeleniumEngine(Engine):
    def __init__(self):
        self.driver = None
        return

    def setup(self):
        self.driver = selenium.webdriver.Firefox()
        return

    def load_page(self, url):
        self.driver.get(url)
        return

    def get_url(self):
        return self.driver.current_url

    def get_source(self):
        return self.driver.page_source

    def cleanup(self):
        self.driver.quit()
        return

class SeleniumEngine(BaseSeleniumEngine):
    def __init__(self):
        super(SeleniumEngine, self).setup()
        return

    def get_page_source(self, url):
        super(SeleniumEngine, self).load_page(url)
        return common.Website(
                super(SeleniumEngine, self).get_url(),
                super(SeleniumEngine, self).get_source()
                )


class TimedWait(BaseSeleniumEngine):
    def __init__(self, delay, parent = None):
        self.delay = delay
        if not parent:
            raise errors.EngineError("Selenium Decorator must wrap a Selenium Engine object")
        self.parent = parent
        return

    def get_source(self):
        return self.parent.get_source()

    def get_url(self):
        return self.parent.get_url()

    def get_page_source(self, url):
        self.parent.get_page_source(url)
        time.sleep(self.delay)
        return common.Website(
                self.parent.get_url(),
                self.parent.get_source()
                )
