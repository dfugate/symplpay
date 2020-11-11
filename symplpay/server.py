# ----------------------------------------------------------------------------------------------------------------------
# Copyright (C) 2020 David Fugate dave.fugate@gmail.com
# ----------------------------------------------------------------------------------------------------------------------

import os
import logging
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
    def __init__(self, c, l):
        '''
        Constructor
        :param c: REST API client object to delegate incoming API calls to.
        :param l: Logger instance.
        :return: Instance of this class.
        '''
        self.c = c
        self.l = l
        self.l.info('symplpay server initialized!')

    # --REST APIs--------------------------------------------------------------
    def compositeUsers(self, userId):
        '''
        TODO better documentation
        Composes three separate REST calls:
            GET https://api.qa.fitpay.ninja/users/:userId
            GET https://api.qa.fitpay.ninja/users/:userId/devices
            GET https://api.qa.fitpay.ninja/users/:userId/creditCards

        into a single REST response:
            GET http://localhost:8080/compositeUsers/:userId
        '''
        ret_val = {}

        creditCardState = bottle.request.query.get("creditCardState")
        deviceState = bottle.request.query.get("deviceState")
        self.l.debug(f'compositeUsers: {userId}, {creditCardState}, {deviceState}')

        # userId
        ret_val['userId'] = userId
        ret_val = c.composite_users(userId, creditCardState, deviceState,
                                    bottle.request.url)

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
        return bottle.template('logs', log_buffer=self.l.pbh.buffer)

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
    parser.add_argument("--log",
                        help="Text log file location.",
                        type=str,
                        default=f'symplpay.{now_str}.log')
    parser.add_argument('--debug',
                        dest='debug',
                        default=False,
                        action='store_true',
                        help='Emit debug messages.')
    args = parser.parse_args()
    # Parameter normalization
    args.log = os.path.abspath(args.log)

    # -- Configure logging ----------------------------------------------------
    # TODO - move this to __init__.py
    l = logging.getLogger('symplpay')
    l.setLevel(logging.DEBUG)
    lf = logging.Formatter(LOG_FORMAT)
    
    lh = logging.StreamHandler(sys.stdout)
    lh.setFormatter(lf)
    l.addHandler(lh)

    fh = logging.FileHandler(args.log, mode='w')
    fh.setLevel(logging.INFO)
    fh.setFormatter(lf)
    l.addHandler(fh)

    # We need an in-memory logging handler to render the logs on an HTML page (easily at least).
    pbh = PersistentBufferingHandler(1000)
    pbh.setLevel(logging.DEBUG)
    l.addHandler(pbh)
    l.pbh = pbh
    
    l.info(f'Server logs available from {args.log} *or* http://localhost:{args.port}/logs')

    # -- Configure the web server ---------------------------------------------
    c = Client(args.client_id, args.client_secret, args.base_url, args.token_url, l)
    s = Server(c, l)

    # Initialize routes
    bottle.get("/")(s.main)
    bottle.get("/logs")(s.logs)
    bottle.route('/static/:file_path#.+#')(s.static)
    bottle.get("/favicon.ico")(s.get_favicon)

    bottle.get('/compositeUsers/<userId>')(s.compositeUsers)

    bottle.run(host='localhost', port=args.port, debug=args.debug, quiet=True)