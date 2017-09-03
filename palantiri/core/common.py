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

import threading
from . import errors

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

    def drain(self):
        self.mutex.acquire()
        try:
            local_cpy = self.lst[:]
            self.lst.clear()
            self.mutex.release()
            return local_cpy
        except:
            if self.mutex.locked():
                self.mutex.release()
            return None

