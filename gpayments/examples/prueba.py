from __future__ import absolute_import, division, print_function

import os

import gpayments

from gpayments.error import APIError

gpayments.client_id = ""
gpayments.client_secret = ""

#gpayments.api_base = 'http://api.payments.4geeks.io'
gpayments.log = 'debug'

gpayments.oauth.OAuth.token(client_id = gpayments.client_id, client_secret = gpayments.client_secret)

#print("Attempting Account retreive...")

#resp = gpayments.Account.retrieve()
#print('Success: %r' % (resp))

'''simplecharge=gpayments.SimpleCharge.create(
    amount=10.99,
    description='Description',
    entity_description='Entity Description',
    currency='usd',
    credit_card_number='4242424242424242',
    credit_card_security_code_number=123,
    exp_month=12,
    exp_year=2020
)
print('Success: %r' % (simplecharge)) '''



try:
    chargeid = gpayments.Charge.retrieve("1BdPIDCqnAMAMqhvsVq78xpw")
    print('Charge: %r' % (chargeid))
except APIError as e:
    print (e.message)

try:
    tony = gpayments.Customer.retrieve("S5p6rB3qkyNPCaU6MhK0a5eWiqm6lGUf")
    print('Tony: %r' % (tony))
except APIError as e:
    print (e.message)

#tony.delete()

#tony.credit_card_security_code_number='123'
#tony.credit_card_number='4242424242424242'
#tony.exp_month=12
#tony.exp_year=2035
#tony.currency='usd'
#tony.email='tony@sitcocr.com'
#tony.currency='usd'
#tony.save()

'''newcustomer = gpayments.Customer.create(
    name="Mario Bros",
    email="mariobros@gmail.com",
    currency='crc',
    credit_card_number='4000000000000127',
    credit_card_security_code_number='123',
    exp_month=12,
    exp_year=2035)

print('Nuevo customer: %r' % (newcustomer))'''


'''plan = gpayments.Plan.create(
    name="Mi primer plan",
    amount=30,
    currency='usd',
    trial_period_days=0,
    interval='month', # day, week, month, year
    interval_count=1, # every month charge the customer
    credit_card_description='SITCO basic monthly'
) '''



#plan = gpayments.Plan.retrieve('06386d39-5b7f-4eee-8099-2a1caddc36c9')
#plan.delete()
#plans = gpayments.Plan.list()

#print('Charges: %r' % (plans))

'''plan = gpayments.Plan.create(
    name="SITCO Basico mensual",
    amount=30,
    currency='usd',
    trial_period_days=0,
    interval='month', # day, week, month, year
    interval_count=1, # every month charge the customer
    credit_card_description='SITCO basic monthly'
)'''


plan = gpayments.Plan.retrieve('daa45209-bdb6-463f-97c2-683ddb60f8f6')
clienteid='DbdQFKm6nOaZ86e1Ih0s1zWYXM9WSA6q'
plan.subscribe(clienteid)


gpayments.Subscription.subscribe('KjZyqvqPQBrDmOZL5glNJ1QS1F8fRM03 ', 'daa45209-bdb6-463f-97c2-683ddb60f8f6')



subscription_id = ''

ss = gpayments.Subscription.list()
print('Subscriptions: %r' % (ss))

exit(0)

sub = gpayments.Subscription.retrieve(subscription_id)
print('One Subscription: %r' % (sub))

#sub.delete()




#charges = gpayments.Charge.list()
#print('Charges: %r' % (charges))

exit(0)

'''resp = gpayments.Charge.create(
    amount=80.5,
    customer_key='KjZyqvqPQBrDmOZL5glNJ1QS1F8fRM03',
    description="alguna descripcion",
    entity_description="sitco/test",
    currency='usd'
)
print('Nuevo charge: %r' % (resp)) '''

try:
    #cu = gpayments.Customer.retrieve(newcustomer.get('key'))
    #cu.currency = 'usd'
    #cu.save()
    #cu = gpayments.Customer.retrieve(newcustomer.get('key'))
    #cu.delete()



    cu = gpayments.Customer.retrieve('KjZyqvqPQBrDmOZL5glNJ1QS1F8fRM03')
    cu.name = 'Luigi Bros'
    cu.currency = 'usd' # why is this required???
    cu.save()

except APIError as e:
    print(e.message)


#customers = gpayments.Customer.list()

#print('Customers: %r' % (customers))
