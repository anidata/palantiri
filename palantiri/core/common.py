# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from . import errors

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
