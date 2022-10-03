import logging

from typing import Callable

import settings
from utils import b

from models import Order


class CompanyService:
    empty_list = ['null', None, '']

    def __init__(self, data: Order):
        self.data = data
        self.company_details = None
        self.company_action = None
        self.company_pk = None
        self.action = 'update'
