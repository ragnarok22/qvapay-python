# Python SDK for the QvaPay API

![Banner](https://raw.githubusercontent.com/lugodev/qvapay-python/main/banner.jpg)

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
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

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

### Use context manager

The recommended way to use a client is as a context manager. For example:

```python
[async] with QvaPayClient(...) as client:
    # Do anything you want
    ...
```

### Get your app info

```python
info = client.get_info()
```

### Get your account balance

```python
balance = client.get_balance()
```

### Create an invoice

```python
transaction = client.create_invoice(
    amount=10,
    description='Ebook',
    remote_id='EE-BOOk-123' # example remote invoice id
)
```

### Get transaction

```python
transaction = client.get_transaction(id)
```

### Get transactions

```python
transactions = client.get_transactions(page=1)
```

## Async features

You can also use the asynchronous version of the methods simply by appending `_async` to the method name at the end. For example:

```python
info = await client.get_info_async()
```

You can also read the **QvaPay API** documentation: [qvapay.com/docs](https://qvapay.com/docs).

## Migration guide

### 0.1.0 -> 0.2.0

- `user_id` of `Transaction` model was removed
- `paid_by_user_id` of `Transaction` model was removed

### 0.0.3 -> 0.1.0

- `from qvapay.v1 import *` instead of `from qvapay import *`
- `QvaPayClient` instead of `Client`
- `client.get_info` instead of `client.info`
- `client.get_balance` instead of `client.balance`
- `client.get_transactions` instead of `client.transactions`

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://bio.link/lugodev"><img src="https://avatars.githubusercontent.com/u/18733370?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Carlos Lugones</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=lugodev" title="Code">💻</a></td>
    <td align="center"><a href="http://codeshard.github.io/"><img src="https://avatars.githubusercontent.com/u/5880754?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ozkar L. Garcell</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=codeshard" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/leynier"><img src="https://avatars.githubusercontent.com/u/36774373?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Leynier Gutiérrez González</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=leynier" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/jorgeajimenezl"><img src="https://avatars.githubusercontent.com/u/18174581?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jorge Alejandro Jimenez Luna</b></sub></a><br /><a href="https://github.com/lugodev/Qvapay Python/commits?author=jorgeajimenezl" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

<p align="center">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>
