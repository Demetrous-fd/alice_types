from enum import Enum


class SlotsType(str, Enum):
    YANDEX_NUMBER = "YANDEX.NUMBER"
    YANDEX_FIO = "YANDEX.FIO"
    YANDEX_DATETIME = "YANDEX.DATETIME"
    YANDEX_GEO = "YANDEX.GEO"
