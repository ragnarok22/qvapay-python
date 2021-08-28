from __future__ import absolute_import
import requests
from qvapay.errors import QvaPayError
from qvapay.resources.info import Info
from qvapay.resources.invoice import Invoice
from qvapay.resources.transaction import Transaction, PaginatedTransactions


def validate_response(response):
    if response.status_code != 200:
            print(response.content)
            raise QvaPayError()


class Client(object):
    app_id = None
    app_secret = None
    version = None

    data = None

    def __init__(self, app_id, app_secret, version=1):
        """
        Creates a QvaPay client.
        * app_id: QvaPay app id.
        * app_secret: QvaPay app secret.
        Get your app credentials at: https://qvapay.com/apps/create
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.version = version
        self.url = 'https://qvapay.com/api/v' + str(version) + '/{endpoint}' + f'?app_id={self.app_id}&app_secret={self.app_secret}'
    
    def info(self):
        """
        Get info relating to your QvaPay app.
        https://qvapay.com/docs/2.0/app_info
        """

        response = requests.get(
            url=self.url.format(endpoint='info'),
        )

        validate_response(response)
        
        data = response.json()

        return Info(
            id=data['uuid'],
            user_id=data['user_id'],
            name=data['name'],
            url=data['url'],
            description=data['desc'],
            callback=data['callback'],
            logo=data['logo'],
            active=data['active'],
            enabled=data['enabled']
        )

    def balance(self):
        """
        Get your QvaPay balance.
        https://qvapay.com/docs/2.0/balance
        """

        response = requests.get(
            url=self.url.format(endpoint='balance')
        )

        validate_response(response)

        return response.json()
    
    def transactions(self, page=1):
        """
        Gets transactions list, paginated by 50 items per request.
        * page: Page to be fetched.
        https://qvapay.com/docs/2.0/transactions
        """

        response = requests.get(
            url=self.url.format(endpoint='transactions') + f'&page={page}'
        )

        validate_response(response)

        data = response.json()

        transactions = []
        for t in data['data']:
            transactions.append(Transaction(
                id=t['uuid'],
                user_id=t['user_id'],
                amount=t['amount'],
                description=t['description'],
                remote_id=t['remote_id'],
                status=t['status'],
                paid_by_user_id=t['paid_by_user_id'],
                # signed=t['signed'],
                created_at=t['created_at'],
                updated_at=t['updated_at'],
                # paid_by=t['paid_by']
            ))

        return PaginatedTransactions(
            transactions=transactions,
            current_page=data['current_page'],
            last_page=data['last_page']
        )
    
    def get_transaction(self, id):
        """
        Gets a transaction by its id (uuid).
        * id: Transaction uuid returned by QvaPay when created.
        https://qvapay.com/docs/2.0/transaction
        """

        response = requests.get(
            url=self.url.format(endpoint=f'transaction/{id}')
        )

        validate_response(response)

        data = response.json()

        return Transaction(
            id=data['uuid'],
            user_id=data['user_id'],
            amount=data['amount'],
            description=data['description'],
            remote_id=data['remote_id'],
            status=data['status'],
            paid_by_user_id=data['paid_by_user_id'],
            # signed=data['signed'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            paid_by=data['paid_by']
        )
    
    def create_invoice(self, amount, description, remote_id=None, signed=False):
        """
        Creates an invoice.
        * amount: Amount of money to receive to your wallet, expressed in dollars with two decimals.
        * description: Description of the invoice to be created, useful to show info to the user who pays. Max 300 chars.
        * remote_id: Invoice ID on your side (example: in your e-commerce store). Optional.
        * signed: Generates a signed URL, valid for 30 minutes. Useful to increase security, introducing an expiration datetime. Optional.
        https://qvapay.com/docs/2.0/create_invoice
        """

        url = self.url.format(endpoint='create_invoice') + f'&amount={amount}&description={description}'

        s = {
            True: '1',
            False: '0'
        }.get(signed)

        url += f'&remote_id={remote_id}&signed={s}'

        response = requests.get(url=url)

        validate_response(response)

        data = response.json()

        return Invoice(
            id=data['transation_uuid'],
            amount=data['amount'],
            description=data['description'],
            remote_id=data['remote_id'],
            signed=data['signed'],            
            url=data['url'],
            signed_url=data['signedUrl']
        )
