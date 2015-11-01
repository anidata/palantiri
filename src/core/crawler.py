# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import threading
import urllib.parse
import re
import datetime
from bs4 import BeautifulSoup

from . import errors
from . import common
from . import engine

# Technically I've read that many operations are thread-safe on Python's
# list implementation, so this may not be necessary, but I think I'd rather
# err on the side of caution at least for now
class SharedList(object):
    def __init__(self, lst):
        self.mutex = threading.Lock()
        self.lst = lst
        return

    def __contains__(self, val):
        return val in self.lst

    def __iter__(self):
        return self.lst.__iter__()

    def pop(self):
        self.mutex.acquire()
        try:
            val = self.lst.pop()
            self.mutex.release()
            return val
        except:
            if self.mutex.locked():
                self.mutex.release()
            return None

    def append(self, val):
        self.mutex.acquire()
        try:
            self.lst.append(val)
            self.mutex.release()
            return True
        except:
            if self.mutex.locked():
                self.mutex.release()
            return None

    def __len__(self):
        return len(self.lst)

    def extend(self, lst):
        self.mutex.acquire()
        try:
            self.lst.extend(lst)
            self.mutex.release()
            return True
        except:
            if self.mutex.locked():
                self.mutex.release()
            return True

class EngineWrapper(threading.Thread):
    def __init__(self, parent, group=None, target=None, name=None,
            args=(), kwargs=None, verbose=None):
        super(EngineWrapper, self).__init__()
        self.parent = parent
        self.eng = parent.eng.clone()
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
                    threading.Thread(target=self.parent.notify(site))
            # The parent needs more time to generate more sites.
            # Wait the set delay
            else:
                time.sleep(self.delay)
        return

class SearchCrawler(object):
    def __init__(self, kwds = [], col = None, eng = engine.DefaultEngine(),
            max_threads = 10, delay = 1):
        self.max_threads = max_threads
        self.eng = eng
        self.col = col
        self.stop = threading.Event()
        self.history = SharedList([])
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
        try:
            self.history.append(message)

            curr = self.col.find({"_id": {"$eq": message.url}}).limit(1)

            dt = datetime.datetime.now()
            # keep granularity at day
            today = datetime.datetime(dt.year, dt.month, dt.day)
            # document already exists
            if curr.count() > 0:
                # update the last day the page was indexed
                cur = self.col.update_one(
                        { "_id": message.url },
                        { "$set": { "dateRange.last": today } }
                        )
            # if we don't already have the website insert the website
            else:
                cur = self.col.insert_one({
                    "_id": message.url,
                    "source": message.source,
                    "dateRange": {
                        "first": today,
                        "last": today,
                    }
                    })
            return True
        except:
            #if self.mutex.locked():
                #self.mutex.release()
            return False

    def start_threads(self):
        for x in range(0, self.max_threads):
            t = EngineWrapper(self)
            self.children.append(t)
            t.start()

    def start(self):
        raise MasterError("get_listings has not been implemented for this class")

class BackpageCrawler(SearchCrawler):
    def __init__(self, site, kwds = [], col = None, area = "atlanta",
            eng = engine.DefaultEngine(), max_threads = 10, delay = 1):
        self.baseurl = "".join(["http://", area, ".backpage.com/", site, "/"])
        if kwds:
            keywords = " ".join(kwds)
            self.url = "?".join([self.baseurl, keywords])
        else:
            self.url = self.baseurl
        super(BackpageCrawler, self).__init__(kwds, col, eng, max_threads, delay)

    def next_page(self, soup):
        links = soup.find_all("a", href=True)
        for link in links:
            if link.content == "Next":
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

            if not href in self.to_visit and not href in self.history:
                valid.append(href)

        self.to_visit.extend(valid)
        return

    def start(self):
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

class CraigslistCrawler(SearchCrawler):
    def __init__(self, site, kwds = [], col = None, area = "atlanta",
            eng = engine.DefaultEngine(), max_threads = 10, delay = 1):
        self.baseurl = "".join(["http://", area, ".craigslist.com/search/", site, "/"])
        if kwds:
            keywords = "+".join(kwds)
            self.url = "?query=".join([self.baseurl, keywords])
        else:
            self.url = self.baseurl
        super(BackpageCrawler, self).__init__(kwds, col, eng, max_threads, delay)
