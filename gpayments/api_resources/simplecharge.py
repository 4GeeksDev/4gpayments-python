from __future__ import absolute_import, division, print_function

from gpayments.api_resources.abstract import CreateableAPIResource


# use example:
# gpayments.SimpleCharge.create(
# amount=80.5,
# description='Description',
# entity_description='Entity Description',
# currency='usd',
# credit_card_number='4242424242424242',
# credit_card_security_code_number=123,
# exp_month=12,
# exp_year=2020,
# )

class SimpleCharge(CreateableAPIResource):
    OBJECT_NAME = 'simplecharge'

    @classmethod
    def class_url(cls):
        return "/v1/charges/simple/create/"
