from __future__ import absolute_import, division, print_function

from gpayments.api_resources.abstract.api_resource import APIResource
from gpayments import api_requestor, util


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, access_token=None,
               **params):
        requestor = api_requestor.APIRequestor(access_token)
        url = cls.class_url()
        headers = None
        response, access_token = requestor.request('post', url, params, headers)

        return util.convert_to_gpayments_object(response, access_token)
