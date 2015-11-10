# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import re

from pymongo import MongoClient
import pymongo.errors

__document_version__ = "0.1"

class ContactFilter(object):
    def __init__(self, parent = None):
        self.parent = parent
        return

    def process(self, message):
        phones = re.findall("\d{3}[-/]\d{3}[-/]\d{4}|\d{10}", message.source)
        emails = re.findall("[\w._-]+\@[\w_-]+\.\w+", message.source)
        today = datetime.datetime.now()
        res = {
                "_id": message.url,
                "v": __document_version__,
                "source": message.source,
                "contact": {
                    "emails": emails,
                    "phones": phones
                    },
                "dateRange": {
                    "first": today,
                    "last": today,
                }
                }
        if self.parent:
            res = self.parent.process(message)
        contact = {}
        contact["emails"] = emails
        contact["phones"] = phones
        res["contact"] = contact
        return res

class BackPageUrlParser(object):
    def __init__(self, parent = None):
        self.parent = parent
        return

    def process(self, message):
        parsed = re.findall("http://(\w+).backpage.com/(\w+)/", message.url)
        today = datetime.datetime.now()
        res = {
                "_id": message.url,
                "v": __document_version__,
                "source": message.source,
                "dateRange": {
                    "first": today,
                    "last": today,
                }
                }
        if self.parent:
            res = self.parent.process(message)
        location = {}
        location["area"] = "" if len(parsed) < 1 else parsed[0][0]
        location["subdirectory"] = "" if len(parsed) < 1 else parsed[0][1]
        location["site"] = "backpage"
        res["siteInfo"] = location
        return res

class MongoDBDump(object):
    def __init__(self, host, port, dbname, colname,
            processor = ContactFilter(BackPageUrlParser())):
        url = "".join([
            "mongodb://",
            host,
            ":",
            port,
            "/"
            ])
        self.conn = MongoClient(url)
        self.col = self.conn[dbname][colname]
        self.processor = processor

    def dump(self, message):
        try:
            curr = self.col.find({"_id": {"$eq": message.url}}).limit(1)
            # document already exists
            if curr.count() > 0:
                # update the last day the page was indexed
                cur = self.col.update_one(
                        { "_id": message.url },
                        { "$set": { "dateRange.last": datetime.datetime.now() } },
                        upsert = True
                        )
            # if we don't already have the website insert the website
            else:
                cur = self.col.insert_one(self.processor.process(message))
        except pymongo.errors.DuplicateKeyError:
            pass
