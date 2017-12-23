from __future__ import absolute_import, division, print_function

import warnings

from gpayments import api_requestor, util
from gpayments.api_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):

    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, access_token=None,
             **params):
        requestor = api_requestor.APIRequestor(access_token,
                                               api_base=cls.api_base())
        url = cls.class_url()
        response, access_token = requestor.request('get', url, params)
        gpayments_object = util.convert_to_gpayments_object(response, access_token)
        # gpayments_object._retrieve_params = params
        return gpayments_object
