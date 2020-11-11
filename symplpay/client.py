# ----------------------------------------------------------------------------------------------------------------------
# Copyright (C) 2020 David Fugate dave.fugate@gmail.com
# ----------------------------------------------------------------------------------------------------------------------

import sys
from time import sleep

try:
    from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
    from requests_oauthlib import OAuth2Session
except ImportError as e:
    print('The "requests_oauthlib" package is unavailable on this system!')
    print('Please run "pip install requests_oauthlib" and try starting the server again;)')
    sys.exit(1)

# -----------------------------------------------------------------------------
class Client(object):
    '''
    REST API client class.
    Issues outgoing HTTP requests, merging results into a single JSON result.
    '''
    def __init__(self, 
                 client_id, client_secret, base_url, token_url,
                 logger, 
                 max_retries=3, retry_sleep=1):
        '''
        Constructor
        :param client_id: REST API username for base_url
        :param client_secret: REST API password for base_url
        :param base_url: base URL of the REST services we'll consume
        :param token_url: URL used for token generator
        :param logger: Python logger
        :param max_retries: if we timeout or otherwise fail to invoke an API,
                            this is the maximum number of retry attempts we'll
                            make
        :param retry_sleep: time in seconds we sleep between retry attempts
        :return: Instance of this class.
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_url = token_url
        self.l = logger

        self.max_retries = max_retries
        self.retry_sleep = retry_sleep

        self.client = BackendApplicationClient(client_id=self.client_id)
        self.session = OAuth2Session(client=self.client)
        
        self.__assign_token()

    def composite_users(self, user_id, credit_card_state, device_state,
                        given_url, user_id_url='/users/%s'):
        '''
        '''
        ret_val = {
            '_links': {
                'self': {
                    'href': given_url
                    }
                }
        }

        # Normal parameters
        if credit_card_state is not None:
            credit_card_state = credit_card_state.upper().strip()
        if device_state is not None:
            device_state = device_state.upper().strip()

        user_id_url = f'{self.base_url}{user_id_url % user_id}'
        self.l.debug(f'User ID URL is {user_id_url}')

        user_json = self.__get_json(user_id_url)
        
        # In theory, we could just take what was passed as a parameter...
        # Could also be the case the API normalized the user ID somehow
        # though;)
        ret_val['userId'] = user_json['id']

        credit_cards_url = user_json['_links']['creditCards']['href']
        # TODO - don't kill the server. Use pagination instead
        credit_cards_json = self.__get_json(credit_cards_url)
        credit_cards = [ {'creditCardId': x['creditCardId'], 
                          'state': x['state'],
                          '_links': {'self': {'href': x['_links']['self']['href']}}} for x in credit_cards_json['results']
                          if credit_card_state is None or x['state'].upper().strip() == credit_card_state]

        ret_val['creditCards'] = {
            'limit': len(credit_cards),
            'offset': 0,
            'totalResults': len(credit_cards),
            'results': credit_cards
        }

        devices_url = user_json['_links']['devices']['href']
        # TODO - don't kill the server. Use pagination instead
        devices_json = self.__get_json(devices_url)
        devices = [ {'deviceId': x['deviceIdentifier'], 
                     'state': x['state'],
                     '_links': {'self': {'href': x['_links']['self']['href']}}} for x in devices_json['results']
                     if device_state is None or x['state'].upper().strip()==device_state]
        ret_val['devices'] = {
            'limit': len(devices),
            'offset': 0,
            'totalResults': len(devices),
            'results': devices
        }

        return ret_val

    def __assign_token(self):
        '''
        A long-running server may need to refresh it's token.
        '''
        self.l.debug('Fetching new token.')
        self.token = self.session.fetch_token(token_url=self.token_url,
                                              client_id=self.client_id,
                                              client_secret=self.client_secret)
        return self.token

    def __get_json(self, url):
        '''
        Given a URL, tries to pull a JSON result from it in a fault-tolerant manner.
        I.e., repeats the request up to a maximum number of retries, sleeping
        between attempts as to not cause a DoS. 
        '''
        for i in range(self.max_retries):
            try:
                response = self.session.get(url)
                if response.ok:
                    return response.json()
                else:
                    num_retries = self.max_retries - i - 1
                    if num_retries:
                        self.l.error(f'Bad response ({response.status_code}) from {url}! Retryring {num_retries} more times.')
                        sleep(self.retry_sleep)
            except TokenExpiredError as e:
                num_retries = self.max_retries - i - 1
                self.l.error(f'Token expired! Renewing...')
                self.__assign_token()

            if not num_retries:
                err_msg = f'Retry attempts exhausted for {url}!'
                self.l.error(err_msg)
                raise Exception(err_msg)


# --MAIN----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # This is just for testing purposes. Real usage is in symplpay.server.
    import sys
    import logging
    from argparse import ArgumentParser
    import json

    from symplpay import LOG_FORMAT

    l = logging.getLogger('client')
    l.setLevel(logging.DEBUG)
    lf = logging.Formatter(LOG_FORMAT)
    lh = logging.StreamHandler(sys.stdout)
    lh.setFormatter(lf)
    l.addHandler(lh)

    parser = ArgumentParser()
    parser.add_argument("--client_id",
                        help="Remote REST API client name",
                        type=str,
                        required=True)
    parser.add_argument("--client_secret",
                        help="Remote REST API client password",
                        type=str,
                        required=True)
    args = parser.parse_args()


    client = Client(args.client_id, args.client_secret,
                    'https://api.qa.fitpay.ninja', 'https://auth.qa.fitpay.ninja/oauth/token?grant_type=client_credentials', 
                    l)
    
    users_url = 'https://api.qa.fitpay.ninja/users?limit=10'
    users = client._Client__get_json(users_url)
    
    for u in users['results']:
        uid = u['id']
        composite_stuff = client.composite_users(uid, 
                                                None, 
                                                None, 
                                                "https://does.not.exist.com")
        print(json.dumps(composite_stuff, sort_keys=False, indent=2))
        print('-------------------------------')

    # quick filtering check
    uid_9 = users['results'][9]['id']
    composite9_stuff = client.composite_users(uid, None, None, "https://does.not.exist.com")
    uid9_cc_state = composite_stuff['creditCards']['results'][0]['state']
    uid9_d_state = composite_stuff['devices']['results'][0]['state']
    print(f'Unfiltered 9: {composite9_stuff["devices"]["totalResults"]} devices & {composite9_stuff["creditCards"]["totalResults"]} creditcards.')

    composite9_stuff = client.composite_users(uid, "nope", None, "https://does.not.exist.com")
    print(f'No credit card 9: {composite9_stuff["devices"]["totalResults"]} devices & {composite9_stuff["creditCards"]["totalResults"]} creditcards.')

    composite9_stuff = client.composite_users(uid, None, "nope", "https://does.not.exist.com")
    print(f'No devices 9: {composite9_stuff["devices"]["totalResults"]} devices & {composite9_stuff["creditCards"]["totalResults"]} creditcards.')

    composite9_stuff = client.composite_users(uid, uid9_cc_state.lower(), uid9_d_state.upper(), "https://does.not.exist.com")
    print(f'Different case 9: {composite9_stuff["devices"]["totalResults"]} devices & {composite9_stuff["creditCards"]["totalResults"]} creditcards.')
