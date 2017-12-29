# 4Geeks Payments Python library

Biblioteca para interactuar con 4Geeks Payments API

Mira la documentación del API aqui http://docs.payments.4geeks.io

Basada en Stripe Python Library

Es Open Source.


Instalación
===========

```sh
pip install gpayments
```

```sh
easy_install gpayments
```

## Uso


```python
# primer uso para obtener el token
import gpayments
gpayments.client_id = "CLIENT_ID_HERE"
gpayments.client_secret = "CLIENT_SECRET_HERE"

# Intentar autenticarnos si el access_token no está seteado
if gpayments.access_token is None:
    auth = gpayments.auth()

# guardar el token por ejemplo en una BD
mi_token = auth.data['access_token']
# el token expirará en auth.data['expires_in'] en ese momento se deberá autenticar otra vez

```

No es necesario guardar el token en el programa porque la biblioteca lo hace automáticamente, pero se puede guardar en 
una BD para su uso posterior, por ejemplo después de un reinicio en cuyo caso no es necesario autenticarse nuevamente 
sino sólo establecer el token en la biblioteca de la siguiente manera:

```python
import gpayments

gpayments.access_token = "MI_ACCESS_TOKEN"

# aquí ya se puede empezar a utilizar todas las funciones del API
```

## Account

```python
resp = gpayments.Account.retrieve()
```

## Customer

```python
pablo = gpayments.Customer.create(
    name="Pablo Marmol",
    email="pablomarmol@gmail.com",
    currency='crc',
    credit_card_number='4242424242424242',
    credit_card_security_code_number='123',
    exp_month=12,
    exp_year=2035)
)

pablo2 = gpayments.Customer.retrieve(pablo.get('key'))

pablo2.name="Pablo Mármol"
pablo2.currency='usd'

pablo2.save()

pablo2.delete()

customers = gpayments.Customer.list()
```

## Charges
```python

charge = gpayments.Charge.create(
    amount=80.5,
    customer_key=pablo.get('key'),
    description="alguna descripcion",
    entity_description="my_company/test",
    currency='usd'
)

simplecharge = gpayments.SimpleCharge.create(
    amount=10.99,
    description='Description',
    entity_description='Entity Description',
    currency='usd',
    credit_card_number='4242424242424242',
    credit_card_security_code_number=123,
    exp_month=12,
    exp_year=2020
)

# list charges
charges = gpayments.Charge.list()

charge = gpayments.Charge.retrieve("1BTvroCqnAM123fqhvZw4d1kHk")

```

## Plan

```python

plan = gpayments.Plan.create(
    name="Basico mensual",
    amount=30,
    currency='usd',
    trial_period_days=0,
    interval='month', # day, week, month, year
    interval_count=1, # every month charge the customer
    credit_card_description='Basic monthly'
)

plans = gpayments.Plan.list()

mi_plan = gpayments.Plan.retrieve("daa45209-bdb6-463f-97c2-683ddb60f8f6")
mi_plan.delete()
```

## Subscriptions

```python

# Dos opciones para crear una nueva suscripcion:
# a) Teniendo el plan como una instancia:

plan = gpayments.Plan.retrieve('daa45209-bdb6-463f-97c2-683ddb60f8f6')
clienteid=pablo.get('key')
plan.subscribe(clienteid)

# b) Llamando al método, si tenemos las keys del plan y del customer

cliente_id="KjZyqvqPQBrDmOZL5glNJ1QS1F8fRM03"
plan_id="daa45209-bdb6-463f-97c2-683ddb60f8f6"
newsub=gpayments.Subscription.subscribe(cliente_id, plan_id)


plans = gpayments.Plan.list()

subscription_id="B6Vje4CBVugWea"
sub = gpayments.Subscription.retrieve(subscription_id)

sub.delete()

```

# Authors
* **Sergio Guzmán** Adaptación de Stripe Library para Gpayments por: [SITCO](http://www.sitcocr.com)

# License

This project is licensed under the MIT License

# Acknowledgments
* Stripe Payments Python Library