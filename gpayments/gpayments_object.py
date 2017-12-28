from __future__ import absolute_import, division, print_function

import datetime
import warnings
from copy import deepcopy

import gpayments
from gpayments import api_requestor, util, six


def _compute_diff(current, previous):
    if isinstance(current, dict):
        previous = previous or {}
        diff = current.copy()
        for key in set(previous.keys()) - set(diff.keys()):
            diff[key] = ""
        return diff
    return current if current is not None else ""


def _serialize_list(array, previous):
    array = array or []
    previous = previous or []
    params = {}

    for i, v in enumerate(array):
        previous_item = previous[i] if len(previous) > i else None
        if hasattr(v, 'serialize'):
            params[str(i)] = v.serialize(previous_item)
        else:
            params[str(i)] = _compute_diff(v, previous_item)

    return params


class GpaymentsObject(dict):
    class ReprJSONEncoder(util.json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return api_requestor._encode_datetime(obj)
            return super(GpaymentsObject.ReprJSONEncoder, self).default(obj)

    def __init__(self, id=None, access_token=None,
                 last_response=None, **params):
        super(GpaymentsObject, self).__init__()

        self._unsaved_values = set()
        self._transient_values = set()
        self._last_response = last_response

        self._retrieve_params = params
        self._previous = None

        object.__setattr__(self, 'access_token', access_token)

        if id:
            self['id'] = id

    @property
    def last_response(self):
        return self._last_response

    def update(self, update_dict):
        for k in update_dict:
            self._unsaved_values.add(k)

        return super(GpaymentsObject, self).update(update_dict)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(GpaymentsObject, self).__setattr__(k, v)

        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(GpaymentsObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        if not hasattr(self, k) or v != getattr(self, k):
            # Allows for unpickling in Python 3.x
            if not hasattr(self, '_unsaved_values'):
                self._unsaved_values = set()

            self._unsaved_values.add(k)

        super(GpaymentsObject, self).__setitem__(k, v)

    def __getitem__(self, k):
        try:
            return super(GpaymentsObject, self).__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Gpayments's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(list(self.keys()))))
            else:
                raise err

    def __delitem__(self, k):
        super(GpaymentsObject, self).__delitem__(k)

        # Allows for unpickling in Python 3.x
        if hasattr(self, '_unsaved_values'):
            self._unsaved_values.remove(k)

    # Custom unpickling method that uses `update` to update the dictionary
    # without calling __setitem__, which would fail if any value is an empty
    # string
    def __setstate__(self, state):
        self.update(state)

    # Custom pickling method to ensure the instance is pickled as a custom
    # class and not as a dict, otherwise __setstate__ would not be called when
    # unpickling.
    def __reduce__(self):
        reduce_value = (
            type(self),  # callable
            (  # args
                self.get('id', None),
                self.access_token,
            ),
            dict(self),  # state
        )
        return reduce_value

    @classmethod
    def construct_from(cls, values, key,
                       last_response=None):
        instance = cls(values.get('id'), access_token=key,
                       last_response=last_response)
        instance.refresh_from(values, access_token=key,
                              last_response=last_response)
        return instance

    def refresh_from(self, values, access_token=None, partial=False,
                     last_response=None):
        self.access_token = access_token or getattr(values, 'access_token', None)
        self._last_response = last_response

        # Wipe old state before setting new.  This is useful for e.g.
        # updating a customer, where there is no persistent card
        # parameter.  Mark those values which don't persist as transient
        if partial:
            self._unsaved_values = (self._unsaved_values - set(values))
        else:
            removed = set(self.keys()) - set(values)
            self._transient_values = self._transient_values | removed
            self._unsaved_values = set()
            self.clear()

        self._transient_values = self._transient_values - set(values)

        for k, v in six.iteritems(values):
            super(GpaymentsObject, self).__setitem__(
                k, util.convert_to_gpayments_object(v, access_token))

        self._previous = values

    @classmethod
    def api_base(cls):
        return None

    def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params
        requestor = api_requestor.APIRequestor(
            access_token=self.access_token, api_base=self.api_base())
        response, access_token = requestor.request(method, url, params, headers)

        return util.convert_to_gpayments_object(response, access_token)

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), six.string_types):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), six.string_types):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if six.PY2:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2,
                               cls=self.ReprJSONEncoder)

    def to_dict(self):
        warnings.warn(
            'The `to_dict` method is deprecated and will be removed in '
            'version 2.0 of the Gpayments bindings. The GpaymentsObject is '
            'itself now a subclass of `dict`.',
            DeprecationWarning)

        return dict(self)

    def serialize(self, previous):
        params = {}
        unsaved_keys = self._unsaved_values or set()
        previous = previous or self._previous or {}

        for k, v in six.iteritems(self):
            if k == 'id' or (isinstance(k, str) and k.startswith('_')):
                continue
            elif isinstance(v, gpayments.api_resources.abstract.APIResource):
                continue
            elif hasattr(v, 'serialize'):
                child = v.serialize(previous.get(k, None))
                if child != {}:
                    params[k] = child
            elif k in unsaved_keys:
                params[k] = _compute_diff(v, previous.get(k, None))
            elif k == 'additional_owners' and v is not None:
                params[k] = _serialize_list(v, previous.get(k, None))

        return params

    # This class overrides __setitem__ to throw exceptions on inputs that it
    # doesn't like. This can cause problems when we try to copy an object
    # wholesale because some data that's returned from the API may not be valid
    # if it was set to be set manually. Here we override the class' copy
    # arguments so that we can bypass these possible exceptions on __setitem__.
    def __copy__(self):
        copied = GpaymentsObject(self.get('id'), self.access_token)

        copied._retrieve_params = self._retrieve_params

        for k, v in six.iteritems(self):
            # Call parent's __setitem__ to avoid checks that we've added in the
            # overridden version that can throw exceptions.
            super(GpaymentsObject, copied).__setitem__(k, v)

        return copied

    # This class overrides __setitem__ to throw exceptions on inputs that it
    # doesn't like. This can cause problems when we try to copy an object
    # wholesale because some data that's returned from the API may not be valid
    # if it was set to be set manually. Here we override the class' copy
    # arguments so that we can bypass these possible exceptions on __setitem__.
    def __deepcopy__(self, memo):
        copied = self.__copy__()
        memo[id(self)] = copied

        for k, v in six.iteritems(self):
            # Call parent's __setitem__ to avoid checks that we've added in the
            # overridden version that can throw exceptions.
            super(GpaymentsObject, copied).__setitem__(k, deepcopy(v, memo))

        return copied
