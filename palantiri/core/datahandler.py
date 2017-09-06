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
import getpass
import re
import json
import threading

import psycopg2

from .common import SharedList

_version = 1

class DataHandler(threading.Thread):
    def __init__(self, batch_size=100, timeout=4000, name="DataHandler"):
        super(DataHandler, self).__init__(name=name)
        self.to_dump = SharedList([])
        self.insert_evt = threading.Event()
        self.stop_evt = threading.Event()
        self.batch_size = batch_size
        self.timeout = timeout

    def cleanup(self):
        self.stop_evt.set()
        self.insert_evt.set()

    def add_page(self, page):
        self.to_dump.append(
            (page.url, page.source, page.access_datetime,
             page.response_code, json.dumps(dict(page.headers)))
        )
        if len(self.to_dump) > self.batch_size:
            self.insert_evt.set()

    def check_insert(self):
        to_insert = self.to_dump.drain()
        if len(to_insert):
            self.dump(to_insert)

    def run(self):
        while not self.stop_evt.is_set():
            self.insert_evt.wait(self.timeout)
            self.check_insert()
            self.insert_evt.clear()
        self.check_insert()

class PostgreSQLDump(DataHandler):
    def __init__(self, host, dbname, user = None, pwd = None):
        super(PostgreSQLDump, self).__init__(name="Postgres Dumper")
        self.db = dbname
        self.host = host
        if user:
            self.user = user
        else:
            self.user = raw_input("PostgreSQL User: ")
        if pwd:
            self.pwd = pwd
        else:
            self.pwd = getpass.getpass("PostgreSQL Password: ")

        self.conn = psycopg2.connect(
                "dbname='{}' user='{}' host='{}' password='{}'".format(
                    self.db, self.user, self.host, self.pwd
                    )
                )

    def __repr__(self):
        return "PostgreSQLDump({}, {})".format(host, db)

    def dump(self, to_insert):
        cur = self.conn.cursor()
        cur.executemany(("INSERT INTO page(url, content, datescraped, status_code, headers) "
                         "VALUES (%s, %s, %s, %s, %s) "
                         "ON CONFLICT (url) DO NOTHING;"),
                        to_insert)
        cur.close()
        self.conn.commit()

    def find_by_id(self, _id, attempt = 0):
        try:
            cur = self.conn.cursor()
            cur.execute(
            """SELECT id FROM page WHERE url = '{}'""".format(_id)
                )
            return cur.fetchone() is not None
        except (psycopg2.IntegrityError, psycopg2.InternalError):
            if attempt < 5:
                return self.find_by_id(_id, attempt + 1)
            return None
