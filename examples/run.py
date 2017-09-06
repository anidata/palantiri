import getpass
import time
import logging
logging.basicConfig(level=logging.DEBUG)

from palantiri.core import crawler, datahandler

areas = [
        # "albanyga",
        # "athensga",
        "atlanta",
        # "augusta",
        # "brunswick",
        # "columbusga",
        # "macon",
        # "nwga",
        # "savannah",
        # "statesboro",
        # "valdosta",
        # "birmingham",
        # "nashville",
        # "panamacity",
        # "myrtlebeach",
        # "memphis",
        # "miami",
        # "tampa"
        ]

sites = [
        # "FemaleEscorts",
        # "BodyRubs",
        # "Strippers",
        # "Domination",
        # "TranssexualEscorts",
        # "MaleEscorts",
        # "Datelines",
        # "AdultJobs",
        "TheraputicMassage",
        "WomenSeekMen",
        "MenSeekWomen",
        "MenSeekMen",
        "WomenSeekWomen",
        ]

user = input("PostgreSQL Username: ")
pwd = getpass.getpass("PostgreSQL Password: ")
page_wait_time = 1

def first_finished(threads):
    for i in range(0, len(threads)):
        if not threads[i].isAlive():
            return i
    return None

for area in areas:
    print(area)
    threads = []
    for site in sites:
        if len(threads) > 4:
            idx = first_finished(threads)
            if idx:
                del threads[idx]
            else:
                time.sleep(1)
                continue

        data_handler = datahandler.PostgreSQLDump("postgres", "crawler",
                                                  user=user, pwd=pwd)
        master = crawler.BackpageContinuousCrawler(site, [], data_handler, area,
                                                   max_threads=2, delay=5)

        threads.append(master)
        master.start()

    for t in threads:
        t.join()
