# Python SDK for the QvaPay API

```
   ___             ____             
  / _ \__   ____ _|  _ \ __ _ _   _ 
 | | | \ \ / / _` | |_) / _` | | | |
 | |_| |\ V / (_| |  __/ (_| | |_| |
  \__\_\ \_/ \__,_|_|   \__,_|\__, |
                              |___/ ✔️✔️

```

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

```python
from qvapay import Client

client = Client(app_id, app_secret, version=1)
```

### Endpoints

**Get your app info**

```python
info = client.info()
```

**Get your account balance**

```python
balance = client.balance()
```

**Create an invoice**

```python
transaction = client.create_invoice(
    amount=10,
    description='Ebook',
    remote_id='EE-BOOk-123' # example remote invoice id
)
id = transaction.id
```

**Get transaction**

```python
transaction = client.get_transaction(id)
```

**Get transactions**

```python
transactions = client.transactions()
```

You can also read the QvaPay API documentation: [https://qvapay.com/docs](https://qvapay.com/docs).
