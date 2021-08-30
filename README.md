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

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://bio.link/lugodev"><img src="https://avatars.githubusercontent.com/u/18733370?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Carlos Lugones</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=lugodev" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

<p align="center">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>
