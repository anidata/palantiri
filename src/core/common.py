# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import threading

class SharedList(object):
    def __init__(self, lst = []):
        self.mutex = threading.Lock()
        self.lst = lst
        return

    def pop():
        self.mutex.acquire()
        return

    def append(self, val):
        self.mutex.acquire()
        try:
            self.lst.append(val)
            self.mutex.release()
            return True
        except:
            self.mutex.release()
            return False

    def extend(self, lst):
        self.mutex.acquire()
        ret_val = False
        try:
            self.lst.extend(lst)
            self.mutex.release()
            return True
        except:
            self.mutex.release()
            return False

class EngineError(Exception):
    def __init__(self, value):
        self.value = value
        return

    def __str__(self):
        return repr(self.value)

class Website(object):
    def __init__(self, url = None, source = None):
        self.url = url
        self.source = source
        return

    def set_source(self, source):
        self.source = source
        return

    def set_url(self, url):
        self.url = url
        return

    def __repr__(self):
        return "url: %s" % self.url
