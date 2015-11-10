# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib.request
import urllib.error
import time
import selenium.webdriver
from stem import Signal
import stem.connection
import getpass

import stem.process
from stem.util import term

from . import errors
from . import common

class Engine(object):
    def __init__(self):
        return

    def get_page_source(self, url):
        raise errors.EngineError("get_page_source not implemented")

    def cleanup(self):
        return

    def clone(self):
        raise errors.EngineError("clone not implemented")

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"

class DefaultEngine(Engine):
    def __init__(self, data = None, headers = {'User-Agent': DEFAULT_USER_AGENT}):
        self.data = data
        self.headers = headers
        return

    def get_page_source(self, url):
        try:
            if url:
                req = urllib.request.Request(url, self.data, self.headers)
                return common.Website(url, str(urllib.request.urlopen(req).read()))
            else:
                return None
        except urllib.error.HTTPError as e:
            return None

    def clone(self):
        return DefaultEngine(self.data, self.headers)

class TorEngine(DefaultEngine):
    def __init__(self, pw = None, control = ("127.0.0.1", 9051), signal = Signal.NEWNYM,
            proxy_handler = urllib.request.ProxyHandler({"http": "127.0.0.1:8118"}),
            data = None, headers = { "User-Agent": DEFAULT_USER_AGENT }):
        if pw:
            self.pw = pw
        else:
            self.pw = getpass.getpass("Tor password: ")
        self.control = control
        self.signal = signal
        self.proxy_handler = proxy_handler
        proxy_opener = urllib.request.build_opener(self.proxy_handler)
        urllib.request.install_opener(proxy_opener)
        super(TorEngine, self).__init__(data, headers)

    def send_signal(self):
        conn = stem.connection.connect(
                control_port = self.control,
                password = self.pw
                )
        conn.signal(self.signal)
        conn.close()

    def get_page_source(self, url):
        try:
            if url:
                self.send_signal()
                req = urllib.request.Request(url, self.data, self.headers)
                res = urllib.request.urlopen(req)
                if res:
                    return common.Website(url, str(res.read()))
                else:
                    return None
            else:
                return None
        except urllib.error.HTTPError as e:
            time.sleep(2)
            return None

    def clone(self):
        return TorEngine(self.pw, self.control, self.signal, self.proxy_handler,
                self.data, self.headers)

class BaseSeleniumEngine(Engine):
    def __init__(self):
        self.driver = None
        return

    def get_source(self):
        return str(self.driver.page_source)

    def cleanup(self):
        self.driver.quit()
        return

    def setup(self):
        self.driver = selenium.webdriver.Firefox()
        return

    def load_page(self, url):
        self.driver.get(url)
        return

    def get_url(self):
        return self.driver.current_url

    def clone(self):
        return BaseSeleniumEngine()

class SeleniumEngine(BaseSeleniumEngine):
    def __init__(self):
        super(SeleniumEngine, self).__init__()
        super(SeleniumEngine, self).setup()
        return

    def get_page_source(self, url):
        if url:
            super(SeleniumEngine, self).load_page(url)
            return common.Website(
                    super(SeleniumEngine, self).get_url(),
                    super(SeleniumEngine, self).get_source()
                    )
        else:
            return None

    def cleanup(self):
        super(SeleniumEngine, self).cleanup()
        return

    def clone(self):
        return SeleniumEngine()


class TimedWait(BaseSeleniumEngine):
    def __init__(self, delay, parent = None):
        self.delay = delay
        if not parent:
            raise errors.EngineError("Selenium Decorator must wrap a Selenium Engine object")
        self.parent = parent
        return

    def get_page_source(self, url):
        if url:
            self.parent.get_page_source(url)
            time.sleep(self.delay)
            return common.Website(
                    self.parent.get_url(),
                    self.parent.get_source()
                    )
        else:
            return None

    def cleanup(self):
        self.parent.cleanup()
        return

    def clone(self):
        return TimedWait(self.delay, self.parent.clone())

    def get_source(self):
        return self.parent.get_source()

    def get_url(self):
        return self.parent.get_url()
