from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Money(NamedTuple):
    currency: str
    value: int


Line = namedtuple('Line', ['sku', 'qty'])


def test_equal():
    assert Money('ghp', 10) == Money('ghp', 10)
    assert Name('Kim', 'Sehwan') != Name('Daniel', 'Kim')
    assert Line('Chair', 1) == Line('Chair', 1)


fiver = Money('ghp', 5)
tenner = Money('ghp', 10)


def can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner
    # fail


if __name__ == '__main__':
    test_equal()
    can_add_money_values_for_the_same_currency()
