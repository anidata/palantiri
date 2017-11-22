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

import getpass
import time

from rasp import TorEngine
from palantiri.core import crawler
from palantiri.core import datahandler


user = "dbadmin" #input("PostgreSQL Username: ")
pwd = "1234" #getpass.getpass("PostgreSQL Password: ")
data_handler = datahandler.PostgreSQLDump("localhost", "crawler",
        user = user, pwd = pwd)

site = "swapfinder.com" #input("website: ")

sites = [site]

def first_finished(threads):
    for i in range(0, len(threads)):
        if not threads[i].isAlive():
            return i
    return None

threads = []
for site in sites:
    if len(threads) > 4:
        idx = first_finished(threads)
        if idx:
            del threads[idx]
        else:
            time.sleep(1)
            continue

    master = crawler.WebsiteCrawler(site, [], data_handler)

    threads.append(master)
    master.start()

for t in threads:
    t.join()
