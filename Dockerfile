# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Use the latest python image from DockerHub (3.x)
FROM python:latest

# Install postgresql dev headers
RUN apt-get -y update \
    && apt-get install -y libpq-dev

# Copy local files into the palantiri directory
COPY . /palantiri/

# Make /palantiri our working directory
WORKDIR /palantiri

# Install dependencies 
RUN pip install .

# Execute test script
CMD ["/usr/local/bin/python", "setup.py", "test"]

