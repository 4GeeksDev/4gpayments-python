from __future__ import absolute_import, division, print_function

from gpayments import six


class GpaymentsError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None,
                 json_body=None, headers=None):
        super(GpaymentsError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except BaseException:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to 4Geeks Support>')

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.request_id = self.headers.get('request-id', None)

    def __unicode__(self):
        if self.request_id is not None:
            msg = self._message or "<empty message>"
            return u"Request {0}: {1}".format(self.request_id, msg)
        else:
            return self._message

    if six.PY3:
        def __str__(self):
            return self.__unicode__()
    else:
        def __str__(self):
            return unicode(self).encode('utf-8')


class APIError(GpaymentsError):
    pass


class APIConnectionError(GpaymentsError):
    pass


class CardError(GpaymentsError):

    def __init__(self, message, param, code, http_body=None,
                 http_status=None, json_body=None, headers=None):
        super(CardError, self).__init__(
            message, http_body, http_status, json_body,
            headers)
        self.param = param
        self.code = code


class IdempotencyError(GpaymentsError):
    pass


class InvalidRequestError(GpaymentsError):

    def __init__(self, message, param, code=None, http_body=None,
                 http_status=None, json_body=None, headers=None):
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body,
            headers)
        self.param = param
        self.code = code


class AuthenticationError(GpaymentsError):
    pass


class PermissionError(GpaymentsError):
    pass


class RateLimitError(GpaymentsError):
    pass


class SignatureVerificationError(GpaymentsError):
    def __init__(self, message, sig_header, http_body=None):
        super(SignatureVerificationError, self).__init__(
            message, http_body)
        self.sig_header = sig_header
