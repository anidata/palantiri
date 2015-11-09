# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess

arr_areas = [
        #"albanyga",
        #"athensga",
        "atlanta",
        #"augusta",
        #"brunswick",
        #"columbusga",
        #"macon",
        #"nwga",
        #"savannah",
        #"statesboro",
        #"valdosta"
        ]

arr_sites = [
        "FemaleEscorts",
        "BodyRubs",
        "Strippers",
        "Domination",
        "TranssexualEscorts",
        "MaleEscorts",
        "Datelines",
        "AdultJobs",
        ]

areas = ",".join(arr_areas)
sites = ",".join(arr_sites)

subprocess.call(["python", "search.py", "-b", sites, "--areas", areas, "--nthreads", "4"])
