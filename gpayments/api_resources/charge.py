from __future__ import absolute_import, division, print_function

from gpayments.api_resources.abstract import CreateableAPIResource
from gpayments.api_resources.abstract import UpdateableAPIResource
from gpayments.api_resources.abstract import ListableAPIResource


class Charge(CreateableAPIResource, ListableAPIResource,
             UpdateableAPIResource):
    OBJECT_NAME = 'charge'

    # TODO not implemented yet
    #def refund(self, idempotency_key=None, **params):
    #    url = self.instance_url() + '/refund'
    #    headers = None
    #    self.refresh_from(self.request('post', url, params, headers))
    #    return self
