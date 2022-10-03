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