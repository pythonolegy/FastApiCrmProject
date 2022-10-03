COMPANY_FIELDS = {
    "CONTRACT_NUMBER": "UF_CRM_1638965208",
    "SPECIFICATION_NUMBER": "UF_CRM_1639053613234",
    "SIGNATORY_POSITION": "UF_CRM_1639497435500"
}

CONTACT_INFORMATION_TYPE = {
    "PHONE": "Phone",
    "POST_ADDRESS": "Post address",
    "BUSINESS_ADDRESS": "Office address",
    "EMAIL": "Email",
}
BUSINESS_ADDRESS_TYPE_BX = 6
POST_ADDRESS_TYPE_BX = 11
ADDRESS_TYPE = [
    {"FIELD": CONTACT_INFORMATION_TYPE["BUSINESS_ADDRESS"], "TYPE": BUSINESS_ADDRESS_TYPE_BX},
    {"FIELD": CONTACT_INFORMATION_TYPE["POST_ADDRESS"], "TYPE": POST_ADDRESS_TYPE_BX},
]


class DealFields:
    contract_number = 'UF_CRM_1637222924726'
    account_number = 'UF_CRM_1655640377'
    invoice_formation_date = 'UF_CRM_1636531719638'
    warehouse = 'UF_CRM_1655642232857'
    specification_number = 'UF_CRM_1639052531930'
    specification_date = 'UF_CRM_1655642303197'
    delivery_condition = 'UF_CRM_1655642397359'
    delivery_time = 'UF_CRM_1656913699059'