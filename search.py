# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import re
from pymongo import MongoClient

from palantiri.core import engine
from palantiri.core import crawler

options = {
        # MongoDB Options
        "port": "27017",
        "host": "127.0.0.1",
        "db": "crawler",
        "collection": "search",
        # Crawler Options
        "engine": engine.DefaultEngine,
        "nthreads": 10,
        "ndelay": 1,
        "terms": None,
        "crawler": None,
        "sites": [],
        "area": "atlanta"
        }

option_descriptions = {
        "port": "\tPort MongoDB will use",
        "host": "\tHost MongoDB will use",
        "db"  : "\tMongoDB database used",
        "collection": "Database collection used",
        "engine": "URL fetching \"engine\" used",
        "nthreads": "Maximum number of green threads spawned",
        "terms": "\tComma separated list of search terms",
        "area": "\tLocation to be searched"
        }

def get_help():
    message = "Usage:\tpython search.py -[cgb] <sites> <optional arguments>\n\tE.g. python palantiri.py -b Foo,Bar --terms foo,bar\nOptional Arguments:"
    for key in option_descriptions:
        message += "\n\t"
        message += "".join(["--", key, "\t", option_descriptions[key]])
    print(message)

def parse_needed(argv, options):
    if len(argv) > 2 and re.search("-\w+", argv[1]):
        options["sites"] = argv[2].split(",")
        if re.search("g", argv[1]):
            print("Google search not yet implemented")
            sys.exit(1)
        elif re.search("c", argv[1]):
            print("Craigslist search not yet implemented")
            sys.exit(1)
        elif re.search("b", argv[1]):
            print("Backpage Search")
            options["crawler"] = crawler.BackpageCrawler
        else:
            print("Could not parse user input")
            sys.exit(1)
    else:
        print("Could not parse user input")
        sys.exit(1)

def parse_optional(argv, options):
    i = 0
    while i < (len(argv) - 1):
        opt = argv[i].replace("--", "")
        if opt in options:
            options[opt] = argv[i + 1]
        else:
            print("Could not parse user input: " + argv[i])
        i += 2
    if i < len(argv):
        print("Could not parse user input: " + argv[i])
        sys.exit(1)

if __name__ == "__main__":
    argv = sys.argv
    # check for --help
    if "--help" in argv:
        get_help()
        sys.exit(0)

    if len(argv) < 3:
        print("Usage:\tpython search.py -[cgb] <sites> <optional arguments>\n\tE.g. python palantiri.py -b Restaurants,Roommates --terms foo,bar\n\tuse --help for more information")
        sys.exit(1)
    else:
        parse_needed(argv, options)
        if len(argv) > 3:
            parse_optional(argv[3:], options)
            url = "".join([
                "mongodb://",
                options["host"],
                ":",
                options["port"],
                "/"
                ])
            print("Connecting to: %s" % url)
            conn = MongoClient(url)
            col = conn[options["db"]][options["collection"]]

            for site in options["sites"]:
                master = options["crawler"](
                        sites,
                        options["terms"].split(",") if options["terms"] else [],
                        col,
                        options["area"],
                        options["engine"](),
                        int(options["nthreads"]),
                        int(options["ndelay"])
                        )
                master.start()
