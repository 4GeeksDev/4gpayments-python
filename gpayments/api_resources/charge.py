from __future__ import absolute_import, division, print_function

from gpayments import api_requestor, util
from gpayments.api_resources.abstract import CreateableAPIResource
from gpayments.api_resources.abstract import ListableAPIResource
from gpayments.six.moves.urllib.parse import quote_plus


class Charge(CreateableAPIResource, ListableAPIResource):
    OBJECT_NAME = 'charge'

    @classmethod
    def _build_instance_url(cls, sid):
        if not sid:
            return cls.class_url()
        # para el caso de retrieve a charge id
        base = cls.class_logs_url()
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
        return "/v1/charges/create/" # this will not work with get all logs

    @classmethod
    def class_logs_url(cls):
        return "/v1/charges/logs/"  # this will not work with get all logs

    @classmethod
    def list(cls, access_token=None,
             **params):
        requestor = api_requestor.APIRequestor(access_token,
                                               api_base=cls.api_base())
        url = cls.class_logs_url()
        response, access_token = requestor.request('get', url, params)
        gpayments_object = util.convert_to_gpayments_object(response, access_token)
        return gpayments_object


