from __future__ import absolute_import, division, print_function

# Gpayments Python bindings
# API docs at http://docs.payments.4geeks.io/
# Authors:
# Sergio Guzman <sergio@sitcocr.com>
# Based on Stripe Python Library
# https://github.com/stripe/stripe-python

# Configuration variables

# api_key = None
access_token = None
client_id = None
client_secret = None
api_base = 'https://api.payments.4geeks.io'
connect_api_base = 'https://api.payments.4geeks.io'
api_version = None
verify_ssl_certs = True
proxy = None
default_http_client = None
app_info = None

# Set to either 'debug' or 'info', controls console logging
log = None

# Resource
from gpayments.api_resources import *  # noqa

# OAuth
from gpayments.oauth import OAuth  # noqa


def auth():
    return oauth.OAuth.token(client_id=client_id, client_secret=client_secret)

# Webhooks
from gpayments.webhook import Webhook, WebhookSignature  # noqa

# Error imports.  Note that we may want to move these out of the root
# namespace in the future and you should prefer to access them via
# the fully qualified `gpayments.error` module.

from gpayments.error import (  # noqa
    APIConnectionError,
    APIError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    CardError,
    IdempotencyError,
    InvalidRequestError,
    SignatureVerificationError,
    GpaymentsError)

# OAuth error classes are not imported into the root namespace and must be
# accessed via gpayments.oauth_error.<Exception>
from gpayments import oauth_error  # noqa

# DEPRECATED: These imports will be moved out of the root gpayments namespace
# in version 2.0

from gpayments.version import VERSION  # noqa
from gpayments.api_requestor import APIRequestor  # noqa

from gpayments.gpayments_object import  GpaymentsObject  # noqa
from gpayments.api_resources.abstract import (  # noqa
    APIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    SingletonAPIResource,
    UpdateableAPIResource)

from gpayments.resource import GpaymentsObjectEncoder  # noqa
from gpayments.util import (  # noqa
    convert_to_gpayments_object,
    json,
    logger)


# Sets some basic information about the running application that's sent along
# with API requests. Useful for plugin authors to identify their plugin when
# communicating with Gpayments.
#
# Takes a name and optional version and plugin URL.
def set_app_info(name, version=None, url=None):
    global app_info
    app_info = {
        'name': name,
        'version': version,
        'url': url,
    }
