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

import os
import logging
import http.client
from urllib.error import HTTPError
from argparse import ArgumentParser
from datetime import datetime

try:
    from symplpay import *
    from symplpay.client import Client
except ImportError as e:
    print('Someone forgot to "PYTHONPATH=.;export PYTHONPATH" prior to running this script! Try again;)')
    sys.exit(1)

try:
    import bottle
except ImportError as e:
    print('The "bottle" package is unavailable on this system!')
    print('Please run "pip install bottle" and try starting the server again;)')
    sys.exit(1)

# -----------------------------------------------------------------------------
class Server(object):
    '''
    Composite Controller class.
    Handles incoming HTTP requests.
    '''
    def __init__(self, c, l, debug):
        '''
        Constructor
        :param c: REST API client object to delegate incoming API calls to.
        :param l: Logger instance.
        :param debug: Running in Production environment?
        :return: Instance of this class.
        '''
        self.c = c
        self.l = l
        self.debug = debug
        self.l.info('symplpay server initialized!')

    # --REST APIs--------------------------------------------------------------
    def compositeUsers(self, userId):
        '''
        Composes three separate REST calls:
            GET https://api.qa.fitpay.ninja/users/:userId
            GET https://api.qa.fitpay.ninja/users/:userId/devices
            GET https://api.qa.fitpay.ninja/users/:userId/creditCards

        into a single REST response:
            GET http://localhost:8080/compositeUsers/:userId

        :param userId: ID of the user we want to learn about
        :param creditCardState: limit credit cards to those matching this state.
        Note that this is *not* a Python parameter; instead it's yanked
        out of the request's query (bottle framework limitation)
        :param deviceState: limit devices to those matching this state.
        Note that this is *not* a Python parameter; instead it's yanked
        out of the request's query (bottle framework limitation)
        :return: Composite JSON response of the the REST calls. Example:

        '''
        creditCardState = bottle.request.query.get("creditCardState")
        deviceState = bottle.request.query.get("deviceState")
        self.l.debug(f'compositeUsers: {userId}, {creditCardState}, {deviceState}')
        try:
            ret_val = c.composite_users(userId, creditCardState, deviceState,
                                        bottle.request.url)
        except HTTPError as e:
            ret_val = bottle.HTTPResponse(status=e.code, 
                                          body={'error': 'general' if e.code not in http.client.responses else http.client.responses[e.code],
                                                'error_description': e.reason}
                                          )
        except Exception as e:
            # Should never happen, but just in case...
            ret_val = bottle.HTTPResponse(status=500, 
                                          body={'error': 'internal server error',
                                                'error_description': str(e)}
                                          )

        return ret_val

    # --HTML VIEWS-------------------------------------------------------------
    def main(self):
        '''
        Main HTML page for the webapp.
        :return:
        '''
        self.l.debug('Request for "main".')
        return bottle.template('main')

    def logs(self):
        '''
        All server logs. 
        Useful for debugging only.
        Would not let this page see the light of day in production w/o 
        an authentication-authorization protocols in place.
        :return:
        '''
        self.l.debug('Request for "logs".')
        if self.debug:
            return bottle.template('logs', log_buffer=self.l.pbh.buffer)
        else:
            return bottle.HTTPResponse(status=403, 
                                       body='Please use the "--debug" flag when starting this webapp to enable world-visible logs:(')

    def static(self, file_path):
        '''
        Used to serve up CSS/JS/etc. files.
        :param file_path: Server path to static files.
        :return: Static file.
        '''
        return bottle.static_file(file_path, root='static')

    def get_favicon(self):
        '''
        :return: Favicon file.
        '''
        return bottle.static_file('favicon.ico', root='static')

    
# --MAIN----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    now_str = datetime.utcnow().strftime(DATETIME_FORMAT)

    # -- Command-line args ---------------------------------------------------- 
    parser = ArgumentParser()
    parser.add_argument('--base_url',
                        help='Remote REST API server to delegate our own calls to.',
                        type=str,
                        default='https://api.qa.fitpay.ninja')
    parser.add_argument('--token_url',
                        help='Remote REST API server to grab our authentication token from',
                        type=str,
                        default='https://auth.qa.fitpay.ninja/oauth/token?grant_type=client_credentials')
    parser.add_argument("--client_id",
                        help="Remote REST API server client name",
                        type=str,
                        required=True)
    parser.add_argument("--client_secret",
                        help="Remote REST API server client password",
                        type=str,
                        required=True)
    parser.add_argument("--port",
                        help="TCP port to run this server from.",
                        type=int,
                        default=8080)
    parser.add_argument("--log_file",
                        help="Text log file location.",
                        type=str,
                        default=f'symplpay.{now_str}.log')
    parser.add_argument('--debug',
                        dest='debug',
                        default=False,
                        action='store_true',
                        help='Emit debug messages.')
    args = parser.parse_args()
    args.log_file = os.path.abspath(args.log_file)

    # We want file logs as well------------------------------------------------
    _fh = logging.FileHandler(args.log_file, mode='w')
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(lf)
    l.addHandler(_fh)
    l.info(f'Server logs available from {args.log_file} *or* http://localhost:{args.port}/logs')

    # -- Configure the web server ---------------------------------------------
    c = Client(args.client_id, args.client_secret, args.base_url, args.token_url, l)
    s = Server(c, l, args.debug)

    # Initialize routes
    bottle.get("/")(s.main)
    bottle.get("/logs")(s.logs)
    bottle.route('/static/:file_path#.+#')(s.static)
    bottle.get("/favicon.ico")(s.get_favicon)
    bottle.get('/compositeUsers/<userId>')(s.compositeUsers)

    # Start honoring requests!
    bottle.run(host='localhost', port=args.port, debug=args.debug, quiet=True)