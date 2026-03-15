import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import auto, StrEnum
from typing import Self, override
import log_setup

log = log_setup.getLogger('transaction')


@dataclass
class Transfer:
    date: datetime
    description: str
    amount: float
    valuta: str

    @classmethod
    def from_csv_line(cls, line: str) -> Self:
        splits = line.split(";")
        try:
            date = datetime.strptime(splits[0], "%d-%m-%Y")
            description = splits[1].lower()
            amount = float(splits[2].replace(".", "").replace(",", "."))
            valuta = splits[3]
            return cls(date=date, description=description, amount=amount, valuta=valuta)
        except ValueError:
            log.error(f"Transaction parse fail: '{line}'")
            raise


class Category(StrEnum):
    # Top
    TOP = auto()

    # Income
    INCOME = auto()
    SALARY = auto()
    MATERNITY_ALLOWANCE = auto()
    SU = auto()
    CHILD_MONEY = auto()

    # Housing
    HOUSING = auto()
    RENT_AND_LOAN = auto()
    EL_WATER_HEATING = auto()
    FURNITURE = auto()

    # Food and household
    FOOD_AND_HOUSEHOLD = auto()
    GROCERIES = auto()
    RESTAURANT_AND_CAFE = auto()
    BAKERY_AND_SPECIALS = auto()

    # Fixed expenses
    FIXED_EXPENSES = auto()
    UNION = auto()
    INSTITUTION = auto()
    INSURANCE = auto()
    GLASSES_AND_LENSES = auto()
    PHONE = auto()
    INTERNET = auto()


    # Transport
    TRANSPORT = auto()
    VEHICLE_LOAN = auto()
    GREEN_TAX = auto()
    FUEL_AND_PARKING = auto()
    REPAIR_AND_WHEELS = auto()
    PUBLIC_TRANSPORTATION = auto()
    BICYCLE = auto()

    # Misc
    MISC = auto()
    SPORT = auto()
    PADEL = auto()
    RUNNING = auto()
    ROAD_BIKING = auto()
    CROSSFIT = auto()
    VACATION = auto()
    TV_STREAMING = auto()

    # Other
    SAVINGS = auto()
    DEBT = auto()
    OTHER = auto()
    UNKNOWN = auto()
    IGNORE = auto()

    def parent(self) -> Self | None:
        match self:
            # Top
            case Category.INCOME:
                return Category.TOP
            case Category.HOUSING:
                return Category.TOP
            case Category.FOOD_AND_HOUSEHOLD:
                return Category.TOP
            case Category.FIXED_EXPENSES:
                return Category.TOP
            case Category.TRANSPORT:
                return Category.TOP
            case Category.MISC:
                return Category.TOP
            case Category.SAVINGS:
                return Category.TOP
            case Category.DEBT:
                return Category.TOP
            case Category.OTHER:
                return Category.TOP
            case Category.UNKNOWN:
                return Category.TOP
            case Category.IGNORE:
                return Category.TOP


            # Income
            case Category.SALARY:
                return Category.INCOME
            case Category.MATERNITY_ALLOWANCE:
                return Category.INCOME
            case Category.SU:
                return Category.INCOME
            case Category.CHILD_MONEY:
                return Category.INCOME

            # Housing
            case Category.RENT_AND_LOAN:
                return Category.HOUSING
            case Category.EL_WATER_HEATING:
                return Category.HOUSING
            case Category.FURNITURE:
                return Category.HOUSING

            # Food and household
            case Category.GROCERIES:
                return Category.FOOD_AND_HOUSEHOLD
            case Category.RESTAURANT_AND_CAFE:
                return Category.FOOD_AND_HOUSEHOLD
            case Category.BAKERY_AND_SPECIALS:
                return Category.FOOD_AND_HOUSEHOLD

            # Fixed expenses
            case Category.UNION:
                return Category.FIXED_EXPENSES
            case Category.INSTITUTION:
                return Category.FIXED_EXPENSES
            case Category.INSURANCE:
                return Category.FIXED_EXPENSES
            case Category.GLASSES_AND_LENSES:
                return Category.FIXED_EXPENSES
            case Category.PHONE:
                return Category.FIXED_EXPENSES
            case Category.INTERNET:
                return Category.FIXED_EXPENSES

            # Transport
            case Category.VEHICLE_LOAN:
                return Category.TRANSPORT
            case Category.GREEN_TAX:
                return Category.TRANSPORT
            case Category.FUEL_AND_PARKING:
                return Category.TRANSPORT
            case Category.REPAIR_AND_WHEELS:
                return Category.TRANSPORT
            case Category.PUBLIC_TRANSPORTATION:
                return Category.TRANSPORT
            case Category.BICYCLE:
                return Category.TRANSPORT

            # MISC
            case Category.SPORT:
                return Category.MISC
            case Category.TV_STREAMING:
                return Category.MISC
            case Category.VACATION:
                return Category.MISC
            case Category.UNKNOWN:
                return Category.MISC
            case Category.OTHER:
                return Category.MISC

            # Sport
            case Category.PADEL:
                return Category.SPORT
            case Category.CROSSFIT:
                return Category.SPORT
            case Category.RUNNING:
                return Category.SPORT
            case Category.ROAD_BIKING:
                return Category.SPORT

            # Top-level
            case _:
                return None


def category_to_pretty_dk(cat: Category) -> str:
    match cat:
        case Category.INCOME:
            return "Indkomst"
        case Category.SALARY:
            return "Løn"
        case Category.MATERNITY_ALLOWANCE:
            return "Barselsdagpenge"
        case Category.SU:
            return "SU"
        case Category.CHILD_MONEY:
            return "Børne- ungeydelse"
        case Category.HOUSING:
            return "Bolig"
        case Category.RENT_AND_LOAN:
            return "Leje og boliglån"
        case Category.EL_WATER_HEATING:
            return "El, vand og varme"
        case Category.FURNITURE:
            return "Møbler"
        case Category.FOOD_AND_HOUSEHOLD:
            return "Mad og husholdning"
        case Category.GROCERIES:
            return "Dagligvarer"
        case Category.RESTAURANT_AND_CAFE:
            return "Restaurant og Café"
        case Category.BAKERY_AND_SPECIALS:
            return "Bageri og specielle"
        case Category.FIXED_EXPENSES:
            return "Øvrige faste"
        case Category.UNION:
            return "A-Kasse og fagforening"
        case Category.INSTITUTION:
            return "Institution"
        case Category.INSURANCE:
            return "Forsikringer"
        case Category.GLASSES_AND_LENSES:
            return "Briller og linser"
        case Category.PHONE:
            return "Telefon"
        case Category.INTERNET:
            return "Internet"
        case Category.TRANSPORT:
            return "Transport"
        case Category.VEHICLE_LOAN:
            return "Billån og -leje"
        case Category.GREEN_TAX:
            return "Grøn ejerafgift"
        case Category.FUEL_AND_PARKING:
            return "Brændstof og parkering"
        case Category.PUBLIC_TRANSPORTATION:
            return "Offentlig transport"
        case Category.BICYCLE:
            return "Cykling (transport)"
        case Category.MISC:
            return "Diverse"
        case Category.SPORT:
            return "Sport"
        case Category.PADEL:
            return "Padel"
        case Category.CROSSFIT:
            return "Crossfit"
        case Category.RUNNING:
            return "Løb"
        case Category.ROAD_BIKING:
            return "Cykling"
        case Category.TV_STREAMING:
            return "TV, streaming, podcast, e-bog"
        case Category.VACATION:
            return "Ferie"
        case Category.SAVINGS:
            return "Opsparing"
        case Category.DEBT:
            return "Gæld"
        case Category.OTHER:
            return "Andet"
        case Category.IGNORE:
            return "Ignorer"
        case Category.UNKNOWN:
            return "Ukendt"
        case _:
            return cat.value

max_category_width = max(len(category_to_pretty_dk(cat)) for cat in Category) + 2

def get_subcats() -> dict[Category, list[Category]]:
    sub_cats: dict[Category, list[Category]] = {cat: [] for cat in Category}
    for cat in Category:
        if cat.parent():
            sub_cats[cat.parent()] += [cat]
    return sub_cats


@dataclass
class Transaction:
    transfer: Transfer
    category: Category
    owner: str

    @override
    def __str__(self) -> str:
        return f"Transaction({self.transfer.description}, {self.transfer.amount} {self.transfer.valuta} [{category_to_pretty_dk(self.category)} @ {self.owner} ({self.transfer.date.strftime('%d-%m-%Y')})])"


def get_timespan_months(transactions: list[Transaction]):
    min_t: Transaction = min(transactions, key=lambda x: x.transfer.date)
    max_t: Transaction = max(transactions, key=lambda x: x.transfer.date)
    min_dt: datetime = min_t.transfer.date
    max_dt: datetime = max_t.transfer.date

    log.debug(f"Earliest transaction = {min_t}")
    log.debug(f"Latest transaction = {max_t}")

    year_diff = max_dt.year - min_dt.year
    if year_diff == 0:
        result = max_dt.month - min_dt.month
    else:
        y_months = (max_dt.year - min_dt.year) * 12
        if min_dt.month < max_dt.month:
            result = y_months + (max_dt.month - min_dt.month)
        else:
            result = y_months - (min_dt.month - max_dt.month)
    result += 1

    log.info(f"Data timespan in months = {result}")

    return result


def get_timespan_months2(transactions: list[Transaction]):
    min_dt: datetime = min(transactions, lambda x: x.transfer.date)
    max_dt: datetime = max(transactions, lambda x: x.transfer.date)
    log.debug(f"{min_dt=}, {max_dt=}")

    def full_months_between(d1: datetime, d2: datetime) -> int:
        if d2 < d1:
            d1, d2 = d2, d1

        months = (d2.year - d1.year) * 12 + (d2.month - d1.month)

        # If the last month isn't complete, subtract one
        if d2.day < d1.day:
            months -= 1

        return months

    log.info(f"{full_months_between(min_dt, max_dt)=}")
