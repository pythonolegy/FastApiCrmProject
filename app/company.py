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

    async def init(self):
        self.company_details = await self.get_company_details()
        self.company_action = self.get_company_action()
        self.company_pk = await self.company_action()

    async def get_company_details(self):
        requisite = f'crm.requisite.list?FILTER[ENTITY_TYPE_ID]=4&FILTER[RQ_INN]={self.data.ContractorData.INN}'
        company = 'crm.company.list?FILTER[ID]=$result[requisite][0][ENTITY_ID]&SELECT[]=*&SELECT[]=UF_*'
        bank_details = 'crm.requisite.bankdetail.list?FILTER[ENTITY_ID]=$result[requisite][0][ID]'
        addresses = 'crm.address.list?FILTER[ENTITY_ID]=$result[company][0][ID]&FILTER[ENTITY_TYPE_ID]=4'
        return await b.call_batch({
            'halt': 0,
            'cmd': {
                'requisite': requisite,
                'company': company,
                'bank_details': bank_details,
                'addresses': addresses
            }
        })

    def exist_company_details(self) -> bool:
        if len(self.company_details['requisite']) == 0:
            return False
        return True

    def get_company_action(self) -> Callable:
        if self.exist_company_details():
            self.action = 'update'
            return self.update_company
        return self.add_company

