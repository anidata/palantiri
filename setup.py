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

from setuptools import setup, Extension, find_packages

# TODO: Added package requirements
test_requirements = [
    "nose",
    "nose-watch"
]

setup(
    name="palantiri",
    version="0.0.1",
    description="Crawler to find data on adds involving human trafficking",
    author="Anidata",
    author_email="info@anidata.org",
    license="BSD",
    packages=find_packages(),
    install_requires=["beautifulsoup4==4.4.1",
                      "pymongo==3.2",
                      "selenium==2.49.2",
                      "stem==1.4.0",
                      "psycopg2==2.6.1",
                      "lxml",
                      "anidata-rasp==0.0.1"],
    dependency_links=[
        "https://github.com/anidata/rasp/tarball/master#egg=anidata-rasp-0.0.1",
    ],
    test_requires=test_requirements,
    extras_require={
        'tests': test_requirements,
    }
)
