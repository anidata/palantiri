# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
from distutils.core import setup, Command, Extension

class PackageTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call(["python", "-m", "unittest", "discover",
            "-s", "./tests", "-p", "test_*.py"])
        raise SystemExit(errno)

util_module = Extension(name = "util", sources = ["src/ext/util.c"])

setup(
        name="palantiri",
        version="0.0.1",
        description="Crawler to find data on adds involving human trafficking",
        author="Daniel Robertson",
        author_email="danlrobertson89@gmail.com",
        license="MPL 2.0",
        ext_package = "palantiri",
        ext_modules = [util_module],
        packages=["palantiri", "palantiri.core"],
        package_dir={'palantiri': 'src'},
        cmdclass = {'test': PackageTest},
        install_requires=["beautifulsoup4 == 4.4.1",
                          "pymongo == 3.2",
                          "selenium == 2.49.2",
                          "stem == 1.4.0",
                          "psycopg2 == 2.6.1"]
        )
