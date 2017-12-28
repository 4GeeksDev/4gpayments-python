from __future__ import absolute_import, division, print_function

from gpayments import oauth, util
from gpayments.api_resources.abstract import CreateableAPIResource
from gpayments.api_resources.abstract import DeletableAPIResource
from gpayments.api_resources.abstract import UpdateableAPIResource
from gpayments.api_resources.abstract import ListableAPIResource
from gpayments.api_resources.abstract import nested_resource_class_methods

from gpayments.six.moves.urllib.parse import quote_plus


class Account(CreateableAPIResource, ListableAPIResource,
              UpdateableAPIResource, DeletableAPIResource):
    OBJECT_NAME = 'account'

    @classmethod
    def retrieve(cls, id=None, access_token=None, **params):
        instance = cls(id, access_token, **params)
        instance.refresh()
        return instance

    @classmethod
    def modify(cls, id=None, **params):
        return cls._modify(cls._build_instance_url(id), **params)

    @classmethod
    def _build_instance_url(cls, sid):
        if not sid:
            return "/v1/accounts/me/"
        sid = util.utf8(sid)
        base = cls.class_url()
        extn = quote_plus(sid)
        return "%s/%s" % (base, extn)

    def instance_url(self):
        return self._build_instance_url(self.get('id'))

    def deauthorize(self, **params):
        params['client_id'] = self.id
        return oauth.OAuth.deauthorize(**params)
