from __future__ import absolute_import, division, print_function

from gpayments import util


class VerifyMixin(object):

    def verify(self, **params):
        url = self.instance_url() + '/verify'
        headers = None
        self.refresh_from(self.request('post', url, params, headers))
        return self
