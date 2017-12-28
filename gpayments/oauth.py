from __future__ import absolute_import, division, print_function

from gpayments import api_requestor, connect_api_base, error, util
from gpayments.six.moves.urllib.parse import urlencode


class OAuth(object):

    @staticmethod
    def _set_client_id(params):
        if 'client_id' in params:
            return
        # @TODO Change according to 4Geeks
        from gpayments import client_id
        if client_id:
            params['client_id'] = client_id
            return

        raise error.AuthenticationError(
            'No client_id provided. (HINT: set your client_id using '
            '"gpayments.client_id = <CLIENT-ID>"). You can find your client_ids '
            'in your Gpayments dashboard at '
            'https://dashboard.payments.4geeks.io/profile/')

    @staticmethod
    def _set_client_secret(params):
        if 'client_secret' in params:
            return
        # @TODO Change according to 4Geeks
        from gpayments import client_secret
        if client_secret:
            params['client_secret'] = client_secret
            return

        raise error.AuthenticationError(
            'No client_id provided. (HINT: set your client_id using '
            '"gpayments.client_id = <CLIENT-ID>"). You can find your client_ids '
            'in your Gpayments dashboard at '
            'https://dashboard.payments.4geeks.io/profile/')


    @staticmethod
    def authorize_url(**params):
        path = '/authentication/authorize'
        OAuth._set_client_id(params)
        if 'response_type' not in params:
            params['response_type'] = 'code'
        query = urlencode(list(api_requestor._api_encode(params)))
        url = connect_api_base + path + '?' + query
        return url

    @staticmethod
    def auth(**params):
        import gpayments
        return OAuth.token(client_id=gpayments.client_id, client_secret=gpayments.client_secret)

    @staticmethod
    def token(**params):
        requestor = api_requestor.APIRequestor(api_base=connect_api_base)
        params['grant_type'] = 'client_credentials'
        response, access_token = requestor.request(
            'post', '/authentication/token/', params, None)
        return response

    @staticmethod
    def deauthorize(**params):
        requestor = api_requestor.APIRequestor(api_base=connect_api_base)
        OAuth._set_client_id(params)
        response, access_token = requestor.request(
            'post', '/authentication/deauthorize', params, None)
        return response
