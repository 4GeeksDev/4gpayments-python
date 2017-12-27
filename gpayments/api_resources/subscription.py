from __future__ import absolute_import, division, print_function

import warnings

from gpayments import api_requestor, util
from gpayments.api_resources.charge import Charge
from gpayments.api_resources.abstract import CreateableAPIResource
from gpayments.api_resources.abstract import DeletableAPIResource
from gpayments.api_resources.abstract import ListableAPIResource

from gpayments.six.moves.urllib.parse import quote_plus


class Subscription(CreateableAPIResource,
           ListableAPIResource, DeletableAPIResource):
    OBJECT_NAME = 'subscription'

    @classmethod
    def _build_instance_url(cls, sid):
        if not sid:
            return "/v1/plans/subscriptions/"
        base = cls.class_url()
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
        return "/v1/plans/subscription"

    @classmethod
    def list(cls, access_token=None,
             **params):
        requestor = api_requestor.APIRequestor(access_token,
                                               api_base=cls.api_base())
        url = cls.class_url() + "s/"
        response, access_token = requestor.request('get', url, params)
        gpayments_object = util.convert_to_gpayments_object(response, access_token)
        return gpayments_object

    def delete(self, **params):
        base = '/v1/plans/un-subscribe'
        sid = self.get('subscription_id')
        sid = util.utf8(sid)
        extn = quote_plus(sid)
        if sid is not None:
            extn = extn + "/"
        url = "%s/%s" % (base, extn)

        self.refresh_from(self.request('delete', url, params))
        return self


    @classmethod
    def subscribe(cls, client_id, plan_id, access_token=None):
        requestor = api_requestor.APIRequestor(access_token)
        url = '/v1/plans/subscribe/'
        params = {'customer_key': client_id, 'plan_key': plan_id}
        headers = None
        response, access_token = requestor.request('post', url, params, headers)

        return util.convert_to_gpayments_object(response, access_token)
