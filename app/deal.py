import logging

from typing import Callable

import company
import settings

from utils import b

from models import Order


class DealService:
    empty_list = ['null', None, '']

    def __init__(self, data: Order):
        self.data = data
        self.deal = None
        self.deal_action = None
        self.deal_pk = None
        self.deal_pk_by_field = None
        self.deal_without_field = None
        self.deal_list = None
        self.action = 'update'
        self.company_pk = company.CompanyService(self.data).company_pk

    async def init(self):
        self.deal_action = await self.get_deal_action()
        self.deal_pk = await self.deal_action()
        await self.set_products_to_deal()
        return {'result': 200}

    async def get_deal_action(self) -> Callable:
        """
       The function determines the values of the 'action' parameter and passes it to the add/update function call

        *** Verification ***
        In the current company by INN and 'Account number':
        1. If a transaction by INN is found, it is simply updated
        2. If not found according to the data above, then we check only the 'Account Number' and if found,
        then we update the transaction and the 'COMPANY_ID'
        3. If both actions failed and the transaction was not found, then,
        by 'COMPANY_ID' we are looking for a deal in bitrix, if found, then we take the first one that comes along,
        and if there is no 'Account Number', then we update the transaction,
        and so iterate over all the company's transactions until we find a deal without a 'Number account'
        4. If each transaction has an 'Account Number', then create a new transaction
        """
        # The first case --- find a deal by the INN of the company and the account number of the transaction
        self.deal = await self.get_deal()
        if self.exist_deal_details():
            self.deal_pk = self.deal[0]['ID']
            self.action = 'update'
            return self.update_deal

        # The second case --- the transaction is based on the Account Number from ...
        self.deal = await self.get_deal_by_field()
        if self.exist_deal_details():
            self.deal_pk = self.deal[0]['ID']
            self.action = 'update'
            return self.update_deal

        # The third case --- the old company already had transactions with some information (without the Account Number)
        self.deal = await self.get_deal_id_without_field()
        if self.exist_deal_details():
            self.deal_pk = self.deal[0]['ID']
            self.action = 'update'
            return self.update_deal

        self.deal_pk = ''
        self.action = 'add'
        return self.add_deal

    def exist_deal_details(self) -> bool:
        """ The function returns True if the transaction bundle with the company exists """
        if len(self.deal) == 0:
            return False
        return True

    def exist_user(self, user):
        if len(user) == 0:
            return False
        return True