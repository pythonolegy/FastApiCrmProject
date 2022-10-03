from company import CompanyService
from deal import DealService
from models import Order

import requests_saver


async def main(data):
    service = Service(data)
    return await service.init()


class Service:
    empty_list = ['null', None, '']

    def __init__(self, data: Order):
        self.data = data
        self.company = None
        self.deal = None
        self.deal_pk = None
        self.products = None

    async def init(self):
        self.company = CompanyService(self.data)
        await self.company.init()
        self.deal = DealService(self.data)
        self.deal.company_pk = self.company.company_pk
        await self.deal.init()
        requests_saver.write_file_requests(self.data)
        return {'result': True}