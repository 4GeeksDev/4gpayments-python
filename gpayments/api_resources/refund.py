from __future__ import absolute_import, division, print_function

from gpayments.api_resources.abstract import CreateableAPIResource
from gpayments.api_resources.abstract import ListableAPIResource


class Refund(CreateableAPIResource,
           ListableAPIResource):
    OBJECT_NAME = 'refund'
