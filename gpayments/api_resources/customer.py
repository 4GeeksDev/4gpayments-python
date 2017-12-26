from __future__ import absolute_import, division, print_function

import warnings

from gpayments import api_requestor, util
from gpayments.api_resources.charge import Charge
from gpayments.api_resources.abstract import CreateableAPIResource
from gpayments.api_resources.abstract import DeletableAPIResource
from gpayments.api_resources.abstract import UpdateableAPIResource
from gpayments.api_resources.abstract import ListableAPIResource

from gpayments.six.moves.urllib.parse import quote_plus


class Customer(CreateableAPIResource, UpdateableAPIResource,
               ListableAPIResource, DeletableAPIResource):
    OBJECT_NAME = 'customer'

    @classmethod
    def _build_instance_url(cls, sid):
        if not sid:
            return "/v1/accounts/customers/"
        base = "/v1/accounts/customer"
        sid = util.utf8(sid)
        extn = quote_plus(sid)
        if sid is not None:
            extn = extn + "/"
        return "%s/%s" % (base, extn)

    def instance_url(self):
        id = self.get('id') or self.get('key')
        return self._build_instance_url(id)

    @classmethod
    def class_url(cls):
        return "/v1/accounts/customers/"

    def charges(self, **params):
        params['customer'] = self.id
        charges = Charge.list(self.access_token, **params)
        return charges

    def update_subscription(self, idempotency_key=None, **params):
        warnings.warn(
            'The `update_subscription` method is deprecated. Instead, use the '
            '`subscriptions` resource on the customer object to update a '
            'subscription',
            DeprecationWarning)
        requestor = api_requestor.APIRequestor(self.api_key)
        url = self.instance_url() + '/subscription'
        headers = None
        response, api_key = requestor.request('post', url, params, headers)
        self.refresh_from({'subscription': response}, api_key, True)
        return self.subscription

    def cancel_subscription(self, idempotency_key=None, **params):
        warnings.warn(
            'The `cancel_subscription` method is deprecated. Instead, use the '
            '`subscriptions` resource on the customer object to cancel a '
            'subscription',
            DeprecationWarning)
        requestor = api_requestor.APIRequestor(self.api_key)
        url = self.instance_url() + '/subscription'
        headers = None
        response, api_key = requestor.request('delete', url, params, headers)
        self.refresh_from({'subscription': response}, api_key, True)
        return self.subscription
