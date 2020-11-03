# (C) Copyright 1996- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import time

import schedule
from aviso_admin import logger, __version__
from aviso_admin.cleaner import Cleaner
from aviso_admin.compactor import Compactor
from aviso_admin.config import Config
from aviso_admin.monitoring.monitor import Monitor


def main():
    # load the configuration
    config = Config()
    logger.info(f"Running Aviso-admin v.{__version__}")
    logger.info(f"Configuration loaded: {config}")

    # instantiate the compactor and cleaner
    compactor = Compactor(config.compactor)
    cleaner = Cleaner(config.cleaner)

    # Every day at scheduled time run the compactor
    schedule.every().day.at(config.compactor["scheduled_time"]).do(compactor.run)

    # Every day at scheduled time run the cleaner
    schedule.every().day.at(config.cleaner["scheduled_time"]).do(cleaner.run)

    # Instantiate the monitor
    monitor = Monitor(config.monitor)
    # schedule the monitor
    schedule.every(config.monitor["frequency"]).minutes.do(monitor.run)

    # Loop so that the scheduling task keeps on running all time.
    while True:
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(30)


# when running directly from this file
if __name__ == "__main__":
    main()

