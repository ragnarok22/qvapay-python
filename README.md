# Python SDK for the QvaPay API

![Banner](banner.jpg)

Non official, but friendly QvaPay library for the Python language.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Test](https://github.com/lugodev/qvapay-python/workflows/CI/badge.svg)](https://github.com/lugodev/qvapay-python/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/lugodev/qvapay-python/branch/main/graph/badge.svg)](https://codecov.io/gh/lugodev/qvapay-python)
[![Version](https://img.shields.io/pypi/v/qvapay?color=%2334D058&label=Version)](https://pypi.org/project/qvapay)
[![Last commit](https://img.shields.io/github/last-commit/lugodev/qvapay-python.svg?style=flat)](https://github.com/lugodev/qvapay-python/commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/lugodev/qvapay-python)](https://github.com/lugodev/qvapay-python/commits)
[![Github Stars](https://img.shields.io/github/stars/lugodev/qvapay-python?style=flat&logo=github)](https://github.com/lugodev/qvapay-python/stargazers)
[![Github Forks](https://img.shields.io/github/forks/lugodev/qvapay-python?style=flat&logo=github)](https://github.com/lugodev/qvapay-python/network/members)
[![Github Watchers](https://img.shields.io/github/watchers/lugodev/qvapay-python?style=flat&logo=github)](https://github.com/lugodev/qvapay-python)
[![GitHub contributors](https://img.shields.io/github/contributors/lugodev/qvapay-python?label=code%20contributors)](https://github.com/lugodev/qvapay-python/graphs/contributors)<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Setup

You can install this package by using the pip tool and installing:

```bash
pip install qvapay
```

Or

```bash
easy_install qvapay
```

## Sign up on **QvaPay**

Create your account to process payments through **QvaPay** at [qvapay.com/register](https://qvapay.com/register).

## Using the client

First, import the `QvaPayClient` class and create your **QvaPay** client using your app credentials.

```python
from qvapay.v1 import QvaPayClient

client = QvaPayClient(app_id, app_secret)
```

It is also possible to use the `QvaPayAuth` class (which by default obtains its properties from environment variables or from the content of the `.env` file) and the static method `QvaPayClient.from_auth` to initialize the client.

```python
from qvapay.v1 import QvaPayAuth, QvaPayClient

client = QvaPayClient.from_auth(QvaPayAuth())
```

### Get your app info

```python
info = client.get_info()
```

Or

```python
info = await client.get_info_async()
```

### Get your account balance

```python
balance = client.get_balance()
```

Or

```python
balance = await client.get_balance_async()
```

### Create an invoice

```python
transaction = client.create_invoice(
    amount=10,
    description='Ebook',
    remote_id='EE-BOOk-123' # example remote invoice id
)
```

Or

```python
transaction = await client.create_invoice_async(
    amount=10,
    description='Ebook',
    remote_id='EE-BOOk-123' # example remote invoice id
)
```

### Get transaction

```python
transaction = client.get_transaction(id)
```

Or

```python
transaction = await client.get_transaction_async(id)
```

### Get transactions

```python
transactions = client.get_transactions(page=1)
```

Or

```python
transactions = await client.get_transactions_async(page=1)
```

You can also read the **QvaPay API** documentation: [qvapay.com/docs](https://qvapay.com/docs).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://lugodev.com"><img src="https://avatars.githubusercontent.com/u/18733370?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Carlos Lugones</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=lugodev" title="Code">💻</a></td>
    <td align="center"><a href="http://codeshard.github.io/"><img src="https://avatars.githubusercontent.com/u/5880754?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ozkar L. Garcell</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=codeshard" title="Code">💻</a></td>
  </tr>
</table>
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

<p align="center">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>
