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

    async def put_deal(self):
        """ The function adds/updates the transaction depending on the passed parameter 'action' """
        # Deal statuses after the status 'Preparation of documents, completed transactions are not taken into account'
        deal_stages = ["C13:FINAL_INVOICE", "C13:1", "C13:2", "C13:3", "C13:4"]
        # Default status for new deals
        deal_stage = "C13:EXECUTING"
        # Checking the status, if the status is after the status 'Preparation of documents, then the current status remains'
        if self.action == 'update' and self.deal[0]['STAGE_ID'] in deal_stages:
            deal_stage = self.deal[0]['STAGE_ID']
        # User verification, if a user with such a surname does not exist, then the user '..' is added.
        user = await self.get_user()
        user_id = '93'
        if self.exist_user(user):
            user_id = user[0]['ID']
        logging.info(f"DEAL USER - {user}")
        logging.info(f"DEAL USER - {user_id}")
        data = {
            'ID': self.deal_pk,
            'fields': {
                'TITLE': self.data.Number,
                'CATEGORY_ID': 13,
                'COMPANY_ID': self.company_pk,
                "STAGE_ID": deal_stage,
                "ASSIGNED_BY_ID": user_id,
                settings.DealFields.contract_number: self.data.Contract,
                settings.DealFields.account_number: self.data.Number,
                settings.DealFields.invoice_formation_date: self.data.Date,
                settings.DealFields.warehouse: self.data.Warehouse,
                settings.DealFields.specification_number: self.data.AdditionalData.SpecNum,
                settings.DealFields.specification_date: self.data.AdditionalData.SpecDate,
                settings.DealFields.delivery_condition: self.data.AdditionalData.DeliveryTerms,
                settings.DealFields.delivery_time: self.data.AdditionalData.DeliveryInWorkDays
            }
        }
        logging.info(f"DEAL ACTION - {self.action}")
        logging.info(f"DEAL DATA - {data}")
        return await b.call(
            f'crm.deal.{self.action}',
            data
        )

    async def update_deal(self):
        """
        Calling the add/update transaction function with the action = 'update' parameter
        * Updates the transaction by the ID of the created/updated company
        """
        await self.put_deal()
        return self.deal_pk

    async def add_deal(self):
        """ Calling the add/update transaction function with the action = 'add' parameter """
        return await self.put_deal()

    async def get_deal(self):
        """ The function gets the transaction by the 'Number' field from the request and/or the company ID """
        return await b.call(
            'crm.deal.list',
            {
                'FILTER': {
                    'COMPANY_ID': self.company_pk,
                    settings.DealFields.account_number: self.data.Number
                }
            }
        )

    async def get_deal_by_field(self):
        """ The function gets the transaction by the 'Number' field from the request and/or the company ID """
        return await b.call(
            'crm.deal.list',
            {
                'FILTER': {
                    settings.DealFields.account_number: self.data.Number
                }
            }
        )

    async def get_deals_by_company_pk(self):
        """ Returns a deal or a list of unclosed deals """
        return await b.get_all(
            'crm.deal.list',
            {
                'FILTER': {
                    'COMPANY_ID': self.company_pk,
                    'CLOSED': "N",
                },
                'SELECT': ['*', 'UF_*']
            }
        )

    async def get_deal_id_without_field(self) -> list:
        """
         The function goes through the list of transactions of the company obtained by the 'COMPANY_ID' filter
        * Returns the ID of the transaction where the 'Number' field is empty
        """
        deals = await self.get_deals_by_company_pk()
        for deal in deals:
            if deal[settings.DealFields.account_number] in self.empty_list:
                return [deal]
        return []

    def get_tax_rate(self, product) -> str:
        tax_rate = ''
        if product != '':
            tax_rate = '20%'
        return tax_rate

    async def set_products_to_deal(self):
        products = [
            {
                'productName': f'{product.Nomenclature}. {product.Characteristic}',
                'price': product.Price,
                'quantity': product.Quantity,
                "tax_rate": self.get_tax_rate(product.VAT),
                "taxIncluded": "Y",

            }
            for product in self.data.ProductsData
        ]

        data = {
            'ownerType': 'D',
            'ownerId': int(self.deal_pk),
            'productRows': products
        }
        logging.info(data)
        return await b.call(
            'crm.item.productrow.set',
            data
        )
