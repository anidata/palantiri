# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import threading
from pymongo import MongoClient

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
        "valdosta"
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

data_handler = datahandler.MongoDBDump("127.0.0.1", "27017", "crawler",
        "search", replset = "rs0")

eng = engine.TorEngine()
for area in areas:
    threads = []
    for site in sites:
        master = crawler.BackpageCrawler(site, [], data_handler, area,
                                         eng, 1, 1)

        threads.append(master)
        master.start()
    for t in threads:
        t.join()
