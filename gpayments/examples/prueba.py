from __future__ import absolute_import, division, print_function

import os

import gpayments

from gpayments.error import APIError

gpayments.client_id = ""
gpayments.client_secret = ""

gpayments.oauth.OAuth.token(client_id = gpayments.client_id, client_secret = gpayments.client_secret)

print("Attempting Account retreive...")

resp = gpayments.Account.retrieve()
print('Success: %r' % (resp))


tony = gpayments.Customer.retrieve("S5p6rB3qkyNPCaU6MhK0a5eWiqm6lGUf")
print('Tony: %r' % (tony))

tony.credit_card_security_code_number='123'
tony.credit_card_number='4242424242424242'
tony.exp_month=12
tony.exp_year=2035
tony.currency='usd'
tony.save()

newcustomer = gpayments.Customer.create(
    name="Mario Bros",
    email="mariobros@gmail.com",
    currency='crc',
    credit_card_number='4242424242424242',
    credit_card_security_code_number='123',
    exp_month=12,
    exp_year=2035)

print('Nuevo customer: %r' % (newcustomer))

try:
    cu = gpayments.Customer.retrieve(newcustomer.get('key'))
    cu.delete()
    cu = gpayments.Customer.retrieve('wswSqTMMHAWpDzL637PGG4WPsTyVgIQ5')
    cu.delete()
except APIError as e:
    print(e.message)


customers = gpayments.Customer.list()

print('Customers: %r' % (customers))
