# Copyright (c) 2017 Anidata
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import logging
import random
import re
import threading
import time
from copy import copy
import urllib.parse
from bs4 import BeautifulSoup
from rasp import DefaultEngine

from . import errors
from .common import SharedList

class EngineWrapper(threading.Thread):
    def __init__(self, parent, group = None, name = None,
            args = (), kwargs = None):
        super(EngineWrapper, self).__init__(group = group, name = name,
                args = args, kwargs = kwargs)
        self.parent = parent
        self.eng = copy(parent.eng)
        self.to_visit = parent.to_visit
        self.stop = parent.stop
        self.delay = parent.delay

    def run(self):
        while self.to_visit or not self.stop.is_set():
            # There are more sites to visit
            if self.to_visit:
                url = self.to_visit.pop()
                site = self.eng.get_page_source(url)
                if url and site:
                    self.parent.notify(site)
            # The parent needs more time to generate more sites.
            # Wait the set delay
                time.sleep(self.delay)
            else:
                time.sleep(self.delay)
        return

class SearchCrawler(threading.Thread):
    def __init__(self, kwds = [], dbhandler = None, eng = DefaultEngine(),
            max_threads = 10, delay = 1, group = None, name = None,
            args = (), kwargs = None):
        super(SearchCrawler, self).__init__(group = group, name = name,
                args = args, kwargs = kwargs)
        self.max_threads = max_threads
        self.eng = eng
        self.dbhandler = dbhandler
        self.stop = threading.Event()
        self.to_visit = SharedList([])
        self.delay = delay
        self.kwds = kwds
        self.children = []
        return

    def next_page(self, soup):
        raise MasterError("next_page has not been implemented for this class")

    def get_listings(self, soup):
        raise MasterError("get_listings has not been implemented for this class")

    def notify(self, message):
        if getattr(message, "url", None):
            logging.info("Dumping %s" % str(message.url))
            self.dbhandler.add_page(message)
            return True
        else:
            return False

    def start_threads(self):
        self.dbhandler.start()
        for x in range(0, self.max_threads):
            t = EngineWrapper(self)
            self.children.append(t)
            t.start()
        logging.info("Started %d threads" % self.max_threads)

    def run(self):
        raise MasterError("get_listings has not been implemented for this class")

class BackpageCrawler(SearchCrawler):
    def __init__(self, site, kwds = [], dbhandler = None, area = "atlanta",
            eng = DefaultEngine(), max_threads = 10, delay = 1):
        self.baseurl = "".join(["http://", area, ".backpage.com/", site, "/"])
        if kwds:
            keywords = " ".join(kwds)
            self.url = "?".join([self.baseurl, keywords])
        else:
            self.url = self.baseurl
        super(BackpageCrawler, self).__init__(kwds, dbhandler, eng, max_threads, delay)

    def next_page(self, soup):
        links = soup.find_all("a", href=True)
        for link in links:
            innerHTML = link.decode_contents(formatter = "html")
            if innerHTML == "Next":
                return link["href"]
        return None

    def get_listings(self, soup):
        links = soup.find_all("a", href=True)
        valid = []
        for link in links:
            # remove some non-ad links
            if link.has_attr("class"):
                continue

            href = str(urllib.parse.urljoin(self.baseurl, link["href"]))
            # remove urls that are not on the same site
            if not re.search(self.baseurl, href):
                continue

            b_isindb = self.dbhandler.find_by_id(href)
            if not href in self.to_visit and not b_isindb:
                valid.append(href)
            if len(valid) > 100:
                self.to_visit.extend(valid)
                valid.clear()

        self.to_visit.extend(valid)
        return

    def run(self):
        self.start_threads()
        time.sleep(self.delay)
        url = self.url

        while url:
            site = self.eng.get_page_source(url)
            if site:
                soup = BeautifulSoup(site.source, "lxml")
                self.get_listings(soup)
                url = self.next_page(soup)
            else:
                url = None

        self.stop.set()
        for t in self.children:
            t.join()
        self.dbhandler.join()

class BackpageContinuousCrawler(BackpageCrawler):

    """Continously running version of BackpageCrawler class"""

    def __init__(self, site, kwds = None, dbhandler = None, area =
                 "atlanta", eng = DefaultEngine(), max_threads = 2,
                 delay = 5):
        """TODO: to be defined1.

        :site: TODO
        :kwds: TODO
        :dbhandler: TODO
        :area: TODO
        :eng: TODO

        """
        BackpageCrawler.__init__(self, site, kwds, dbhandler, area, eng, max_threads,
                                 delay)
        self._avg_delay = delay

    @property
    def delay(self):
        return 0.5 * self._avg_delay + random.random() * self._avg_delay

    @delay.setter
    def delay(self, value):
        self._avg_delay = value

    def get_listings(self, soup):
        links = soup.find_all("a", href=True)
        valid = []
        for link in links:
            # remove some non-ad links
            if link.has_attr("class"):
                continue

            href = str(urllib.parse.urljoin(self.baseurl, link["href"]))
            # remove urls that are not on the same site
            if not re.search(self.baseurl, href):
                continue

            res = self.dbhandler.find_by_id(href)
            if not href in self.to_visit and not res:
                valid.append(href)

        self.to_visit.extend(valid)
        return valid

    def run(self):
        self.start_threads()
        time.sleep(self.delay)
        url = self.url
        new_listing_cnt = 0

        # TODO: These should be configurable, not hard coded
        self.max_retry = 3
        retry = 0

        old_listing_cnt = -1
        while url and new_listing_cnt != old_listing_cnt:
            logging.info("Fetching %s" % url)
            site = self.eng.get_page_source(url)
            if site:
                soup = BeautifulSoup(site.source, "lxml")
                valid_listings = self.get_listings(soup)
                new_listing_cnt += len(valid_listings)

                url = self.next_page(soup)
            else:
                if old_listing_cnt == new_listing_cnt:
                    retry += 1
                else:
                    retry = 0

                old_listing_cnt = new_listing_cnt
                if retry <= self.max_retry:
                    url = self.url
                    retry_delay = 10 * self.delay
                    logging.info("Waiting %d seconds to retry" % retry_delay)
                    time.sleep(retry_delay)
                else:
                    logging.info("Tried %d times without new results" % retry)
                    url = None

        self.stop.set()
        for t in self.children:
            t.join()

