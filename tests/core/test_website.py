# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from palantiri.core.common import Website

import unittest

class TestStringMethods(unittest.TestCase):
      def test_website(self):
          site = Website("url", "content")
          self.assertEqual(site.url, "url")
          self.assertEqual(site.source, "content")

if __name__ == "__main__":
    unittest.main()
