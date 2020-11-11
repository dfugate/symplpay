# -----------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2020 David Fugate
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
# -----------------------------------------------------------------------------

import logging
import logging.handlers
import sys

# --SANITY CHECKS--------------------------------------------------------------
if sys.version_info.major != 3:
    print("This version of Python, {{sys.version}}, is not supported! Please install 3.x!")
    sys.exit(1)

# --CLASSES--------------------------------------------------------------------
class PersistentBufferingHandler(logging.handlers.BufferingHandler):
    '''
    Subclass of BufferingHandler which *never* throws logs away.
    '''
    def flush(self):
        '''
        Overridden
        :return: Nothing
        '''
        pass

# --GLOBALS--------------------------------------------------------------------
LOG_FORMAT = '%(asctime)-15s - %(levelname)-8s - %(message)s'
DATETIME_FORMAT = '%Y_%m_%d_%H_%M_%S_%f'

# Setup a global logger and log formatter
l = logging.getLogger('symplpay')
l.setLevel(logging.DEBUG)
lf = logging.Formatter(LOG_FORMAT)
_lh = logging.StreamHandler(sys.stdout)
_lh.setFormatter(lf)
l.addHandler(_lh)
# In-memory log handler to render logs on an HTML page
_pbh = PersistentBufferingHandler(1000)
_pbh.setLevel(logging.DEBUG)
l.addHandler(_pbh)
l.pbh = _pbh

# --HELPER FUNCTIONS ----------------------------------------------------------
