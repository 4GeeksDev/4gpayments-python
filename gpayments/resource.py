from __future__ import absolute_import, division, print_function

#
# This module doesn't serve much purpose anymore. It's only here to maintain
# backwards compatibility.
#
# TODO: get rid of this module in the next major version.
#

import warnings

from gpayments import util
from gpayments.util import (  # noqa
    convert_array_to_dict,
    convert_to_gpayments_object,
)
from gpayments.gpayments_object import GpaymentsObject  # noqa
from gpayments.api_resources.abstract import (  # noqa
    APIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    SingletonAPIResource,
    UpdateableAPIResource,
)
from gpayments.api_resources import *  # noqa


class GpaymentsObjectEncoder(util.json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            '`GpaymentsObjectEncoder` is deprecated and will be removed in '
            'version 2.0 of the Gpayments bindings.  GpaymentsObject is now a '
            'subclass of `dict` and is handled natively by the built-in '
            'json library.',
            DeprecationWarning)
        super(GpaymentsObjectEncoder, self).__init__(*args, **kwargs)
