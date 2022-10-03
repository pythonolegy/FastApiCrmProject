from fast_bitrix24 import BitrixAsync

from os import getenv

webhook = getenv('WEBHOOK')
b = BitrixAsync(webhook)
