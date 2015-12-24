# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import getpass
from pymongo import MongoClient
import time

from src.core import engine
from src.core import crawler
from src.core import datahandler

areas = [
        "albanyga",
        "athensga",
        "atlanta",
        "augusta",
        "brunswick",
        "columbusga",
        "macon",
        "nwga",
        "savannah",
        "statesboro",
        "valdosta",
        "birmingham",
        "nashville",
        "panamacity",
        "myrtlebeach",
        "memphis",
        "miami",
        "tampa"
        ]

sites = [
        "FemaleEscorts",
        "BodyRubs",
        "Strippers",
        "Domination",
        "TranssexualEscorts",
        "MaleEscorts",
        "Datelines",
        "AdultJobs",
        ]

user = input("Username: ")
pwd = getpass.getpass("MongoDB Password: ")
data_handler = datahandler.MongoDBDump("danrobertson.org", "27017", "crawler", "search",
        user = user, pwd = pwd) 
eng = engine.TorEngine()

def first_finished(threads):
    for i in range(0, len(threads)):
        if not threads[i].isAlive():
            return i
    return None

for area in areas:
    threads = []
    for site in sites:
        if len(threads) > 4:
            idx = first_finished(threads)
            if idx:
                del threads[idx]
            else:
                time.sleep(1)
                continue

        master = crawler.BackpageCrawler(site, [], data_handler, area,
                                         eng, 6, 1)

        threads.append(master)
        master.start()

    for t in threads:
        t.join()
