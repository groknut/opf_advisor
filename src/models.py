from enum import Enum


class BusinessScale(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @property
    def label(self) -> str:

        return {
            "small": "Малый",
            "medium": "Средний",
            "large": "Крупный",
        }[self.value]


class ActivityType(str, Enum):
    TRADE = "trade"
    SERVICES = "services"
    PRODUCTION = "production"
    IT = "it"
    OTHER = "other"

    @property
    def label(self) -> str:
        return {
            "trade": "Торговля",
            "services": "Услуги",
            "production": "Производство",
            "it": "IT",
            "other": "Другое",
        }[self.value]


class Opf(str, Enum):
    SELF_EMPLOYED = "Самозанятость"
    IP = "ИП"
    LLC = "ООО"
    JSC = "АО"

    @property
    def full_name(self) -> str:
        return {
            "Самозанятость": "Налог на профессиональный доход (самозанятость)",
            "ИП": "Индивидуальный предприниматель",
            "ООО": "Общество с ограниченной ответственностью",
            "АО": "Акционерное общество",
        }[self.value]


class TaxRegime(str, Enum):
    NPD = "НПД (самозанятость)"
    USN = "УСН"
    USN_INCOME = "УСН «Доходы»"
    USN_INCOME_EXPENSE = "УСН «Доходы минус расходы»"
    OSNO = "ОСНО"
    PSN = "ПСН (патент)"