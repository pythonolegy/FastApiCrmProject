from pydantic import BaseModel
from typing import List, Any, Union


class ProductData(BaseModel):
    Nomenclature: str
    NomenclatureID: str
    Characteristic: str
    CharacteristicID: str
    Price: Union[str, int]
    Quantity: Union[str, int]
    VAT: Union[str, float]


class ContragentDataContacts(BaseModel):
    ContactInfoType: str
    View: str


class ContragentData(BaseModel):
    Title: str
    INN: int
    KPP: Union[str, int]
    OKPO: Union[str, int]
    SettlementAccount: Union[str, int]
    CorrespondentAccount: Union[str, int]
    BIK: Union[str, int]
    Bank: str
    ManegerFullName: str
    ManagerStatus: str
    CardPosition: str
    Contacts: List[ContragentDataContacts]


class AdditionalData(BaseModel):
    SpecNum: Union[str, int]
    SpecDate: str
    DeliveryTerms: str
    DeliveryInWorkDays: Union[str, int]


class Order(BaseModel):
    DocumentTitle: str
    Number: str
    Date: str
    Warehouse: str
    WarehouseID: str
    Contract: str
    ContractID: str
    Manager: str
    ManagerID: str
    ManagerSurname: str
    ManagerName: str
    ProductsData: List[ProductData]
    ContractorData: ContragentData
    AdditionalData: AdditionalData


def get_pydantic_value(data: Order, key: str, default: Any) -> Any:
    key_words = key.split('.')
    value = data
    for key_word in key_words:
        value = getattr(value, key_word, default)
    return value
