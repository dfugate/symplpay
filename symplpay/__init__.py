# ----------------------------------------------------------------------------------------------------------------------
# Copyright (C) 2020 David Fugate dave.fugate@gmail.com
# ----------------------------------------------------------------------------------------------------------------------

import logging
import logging.handlers
import sys

# --SANITY CHECKS--------------------------------------------------------------
if sys.version_info.major != 3:
    print("This version of Python, {{sys.version}}, is not supported! Please install 3.x!")
    sys.exit(1)

# --GLOBALS--------------------------------------------------------------------
LOG_FORMAT = '%(asctime)-15s - %(levelname)-8s - %(message)s'
DATETIME_FORMAT = '%Y_%m_%d_%H_%M_%S_%f'


# --HELPER FUNCTIONS ----------------------------------------------------------
class PersistentBufferingHandler(logging.handlers.BufferingHandler):
    """
    Subclass of BufferingHandler which *never* throws logs away.
    """
    def flush(self):
        """
        Overridden
        :return: Nothing
        """
        pass
