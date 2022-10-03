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
        self.action = 'add'
        return self.add_company

    def get_contact_information_type(self, key: str):
        data = self.data.ContractorData.Contacts
        result = [x for x in data if x.ContactInfoType == key]
        if len(result) > 0:
            return result[0].View
        return ''

    def get_company_addresses(self, company_id: str) -> list:
        addresses = []
        for param in settings.ADDRESS_TYPE:
            address = self.get_contact_information_type(param["FIELD"])
            if address == '':
                continue
            data = {
                'fields': {
                    'ENTITY_ID': company_id,
                    'ENTITY_TYPE_ID': 4,
                    'ADDRESS_1': address,
                    'TYPE_ID': param["TYPE"]
                }
            }
            addresses.append(data)
        return addresses

    def get_contact_data_bx(self, key: str):
        data = self.get_contact_information_type(settings.CONTACT_INFORMATION_TYPE[key])
        if data == '':
            return data
        if ' / ' in data:
            emails = data.split(" / ")
            return [{"VALUE": emails[0]}, {"VALUE": emails[1]}]
        if '/' in data:
            emails = data.split("/")
            return [{"VALUE": emails[0]}, {"VALUE": emails[1]}]
        return [{"VALUE": data}]

    async def add_company(self) -> str:
        company_id = await self.put_company()
        requisite_id = await self.put_company_requisite(company_id)
        await self.put_company_banking_details(requisite_id)
        await self.put_company_address(company_id)
        return company_id

    async def get_user(self):
        return await b.call(
            'user.get',
            {
                'FILTER': {
                    "LAST_NAME": self.data.ManagerSurname,
                    "NAME": self.data.ManagerName
                }
            }
        )

    def exist_user(self, user):
        if len(user) == 0:
            return False
        return True

    async def put_company(self, company_pk: str = '') -> str:
        user = await self.get_user()
        user_id = ''
        if self.action == 'add':
            user_id = '93'
            if self.exist_user(user):
                user_id = user[0]['ID']
        logging.info(f"COMPANY USER - {user}")
        logging.info(f"COMPANY USER - {user_id}")
        return await b.call(
            f'crm.company.{self.action}',
            {
                'ID': company_pk,
                'fields': {
                    'TITLE': self.data.ContractorData.Title,
                    settings.COMPANY_FIELDS['CONTRACT_NUMBER']: self.data.Contract,
                    # settings.COMPANY_FIELDS["SPECIFICATION_NUMBER"]: self.data.AdditionalData.SpecNum,
                    "PHONE": self.get_contact_data_bx('PHONE'),
                    "EMAIL": self.get_contact_data_bx('EMAIL'),
                    settings.COMPANY_FIELDS["SIGNATORY_POSITION"]: self.data.ContractorData.CardPosition,
                    'ASSIGNED_BY_ID': user_id
                }
            }
        )

    async def put_company_requisite(self, company_pk, requisite_id: str = '') -> str:
        return await b.call(
            f'crm.requisite.{self.action}',
            {
                "ID": requisite_id,
                'fields': {
                    "ENTITY_ID": company_pk,
                    "ENTITY_TYPE_ID": 4,
                    "PRESET_ID": 1,
                    "NAME": self.data.ContractorData.Title,
                    "RQ_INN": self.data.ContractorData.INN,
                    "RQ_KPP": self.data.ContractorData.KPP,
                    "RQ_OKPO": self.data.ContractorData.OKPO,
                    "RQ_DIRECTOR": self.data.ContractorData.ManegerFullName,
                }
            }
        )

    async def put_company_banking_details(self, requisite_id, banking_id: str = ''):
        name = self.data.ContractorData.Bank
        if not self.data.ContractorData.Bank:
            name = 'Не заполнено'
        await b.call(
            f'crm.requisite.bankdetail.{self.action}',
            {
                'ID': banking_id,
                'fields': {
                    "ENTITY_ID": requisite_id,
                    "NAME": name,
                    "RQ_BIK": self.data.ContractorData.BIK,
                    "RQ_ACC_NUM": self.data.ContractorData.SettlementAccount,
                    "RQ_COR_ACC_NUM": self.data.ContractorData.CorrespondentAccount
                }
            }
        )

    async def put_company_address(self, company_id: str):
        await b.call(
            f'crm.address.add',
            self.get_company_addresses(company_id)
        )

    async def update_company(self) -> str:
        company_id = self.company_details['company'][0]['ID']
        requisite_id = self.company_details['requisite'][0]['ID']
        banking_id = self.company_details['bank_details'][0]['ID']
        await self.put_company(company_id)
        await self.put_company_requisite(company_id, requisite_id)
        await self.put_company_address(company_id)
        await self.put_company_banking_details(requisite_id, banking_id)
        return company_id
