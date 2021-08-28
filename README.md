# Python SDK for the QvaPay API

Non official, but friendly QvaPay library for the Python language.

## Setup

You can install this package by using the pip tool and installing:

```bash
$ pip install qvapay
```

Or:

```bash
$ easy_install qvapay
```

## Sign up on QvaPay

Create your account to process payments through QvaPay at [https://qvapay.com/register](https://qvapay.com/register).

## Using the client

First, import the Client class and create your QvaPay client using your app credentials.

```
from qvapay import Client

client = Client(app_id, app_secret, version=1)
```

### Endpoints

**Get your app info**

```
info = client.info()
```

**Get your account balance**

```
balance = client.balance()
```

**Create an invoice**

```
transaction = client.create_invoice(
    amount=10,
    description='Ebook',
    remote_id='EE-BOOk-123' # example remote invoice id
)
id = transaction.id
```

**Get transaction**

```
transaction = client.get_transaction(id)
```

**Get transactions**

```
transactions = client.transactions()
```

You can also read the QvaPay API documentation: [https://qvapay.com/docs](https://qvapay.com/docs).
