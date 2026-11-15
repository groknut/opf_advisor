from enum import Enum

class BusinessScale(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class ActivityType(str, Enum):
    TRADE = "trade"
    SERVICES = "services"
    PRODUCTION = "production"
    IT = "it"
    OTHER = "other"

class Opf(str, Enum):
    IP = "ИП"
    LLC = "ООО"
    JSC = "АО"
    SELF_EMPLOYED = "Самозанятость"
