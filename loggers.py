import logging
from pathlib import Path

BASE_PATH_LOGGER = Path("test_logs")
BASE_PATH_INFO = BASE_PATH_LOGGER / "info.log"
fmt_std = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s" # Standard

# Formatting in the logs produced
"""

fmt_1 = "%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s" # More detailed
fmt_2 = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s" # Standard
logging.basicConfig(
    level=logging.INFO,
    format=fmt_1 # Changed the format to this standard
)
logging.info("Info")

"""

# Doing this the console logs disapper - in production we need both.
"""

logging.basicConfig(
    filename=BASE_PATH_INFO, # Stores at this filename location
    level=logging.INFO, # stores info
    format=fmt_std # 
)
logging.info("TRAIN-TEST SPLIT : 8:2 ")
logging.info("MODEL : OVERFITTING")
logging.info("Experiments : Finished")
"""

# TO use logs in both : console and files
"""

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
file = logging.FileHandler("app.log")
logger.addHandler(console)
logger.addHandler(file)

"""

# Also in practice we are never to use the root logger 
# better :  Because it also gives us relative file path if in a big folder ; Better to debug

""" 
logger = logging.getLogger(__name__)
logger.info(...)
"""

# Suppose if our system deals with a lot of traffic - then what to do ?
"""
# We can use techniques called rotating where we do not save all logs but some depending upon the type of rotation.
ROTATION USING NO : We explicily set the number of logs to keep ; for example backup = 5 means upto 5 logs for that file.
ROTATION USING TIME :  We explitly set a date till which that log stays and then gets deleted.
"""

