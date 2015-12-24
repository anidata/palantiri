# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
from distutils.core import setup, Command

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

# TODO: Added package requirements
setup(
        name="palantiri",
        version="0.0.1",
        description="Crawler to find data on adds involving human trafficking",
        author="Daniel Robertson",
        author_email="danlrobertson89@gmail.com",
        license="MPL 2.0",
        packages=["palantiri", "palantiri.core"],
        package_dir={'palantiri': 'src'},
        cmdclass = {'test': PackageTest}
        )
