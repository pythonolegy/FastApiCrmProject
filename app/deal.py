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