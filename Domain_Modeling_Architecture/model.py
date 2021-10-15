from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

"""
dataclass

데이터를 담아두기 위한 클래스를 매우 적은양의 코드로 구현할 수 있도록 도와준다.

dataclass 데코레이터를 이용해 클래스를 생성하면, __init__(), __repr()__, __eq__()와 같은 메서드를 자동으로 생성해준다(물론 필요에따라, 매개변수에 Boolean값 대입해주어야 함).

@dataclass(frozen=True) <- 이 경우에는, 데이터클래스를 활용해 생성된 데이터의 불변성을 보장한다. 데이터를 변경해보려고 하면 예외가 발생한다. 

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False)

위와 같은 매개변수들이 존재한다.

내용 참고는 https://docs.python.org/ko/3/library/dataclasses.html

"""


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
            self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty