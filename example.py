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
