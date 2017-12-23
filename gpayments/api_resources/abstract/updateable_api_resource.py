from __future__ import absolute_import, division, print_function

from gpayments import api_requestor, util
from gpayments.api_resources.abstract.api_resource import APIResource
from gpayments.six.moves.urllib.parse import quote_plus


class UpdateableAPIResource(APIResource):

    @classmethod
    def _modify(cls, url, access_token=None,
                **params):
        requestor = api_requestor.APIRequestor(access_token)
        headers = None
        response, access_token = requestor.request('put', url, params, headers)
        return util.convert_to_gpayments_object(response, access_token)

    @classmethod
    def modify(cls, sid, **params):
        url = "%s/%s" % (cls.class_url(), quote_plus(util.utf8(sid)))
        return cls._modify(url, **params)

    def save(self):
        updated_params = self.serialize(None)
        headers = None

        if updated_params:
            self.refresh_from(self.request('put', self.instance_url(),
                                           updated_params, headers))
        else:
            util.logger.debug("Trying to save already saved object %r", self)
        return self
