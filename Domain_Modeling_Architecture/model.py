from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

""" 할당 노트

제품은 스큐라고 발음하는 SKU로 식별 된다.

스큐는 재고 유지단위의 약자이다.

고객은 주문을 넣는다. 주문은 주문 참조 번호에 의해 식별되고, 한줄 이상의 '주문 라인'을 포함한다.

각 주문 라인에는 SKU와 수량이 있다.

RED-CHAIR 10단위
BLUE-LAMP 1단위

구매 부서는  재고를 작은 Batch로 주문한다. 재고 배치는 유일한 ID, SKU, 수량으로 이루어진다.

배치에 주문 라인을 할당해야한다. 주문 라인을 배치에 할당하면 해당 배치에 속하는 재고를 고객의 주소로 배송한다.

어떤 배치의 재고를 주문 라인에 x단위로 할당하면 가용 재고 수량은 x만큼 줄어든다.

배치의 가용 재고 수량이 주문 라인의 수량보다 작으면 이  주문 라인을  배치에 할당 할  수 없다.

같은 주문 라인을 두 번 이상  할당해서는 안된다.

배치가 현재 배송중이면 ETA 정보가 배치에 들어있다. ETA가 없는 배치는 창고 재고다.

창고 재고를 배송  중인 배치보다 먼저 할당해야 한다.

배송중인 배치를 할당할 경우 ETA가 가장 빠른 배치를 먼저 할당한다.

"""


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
    """
    주문은 주문 참조 번호에 의해 식별되고
    각 주문 라인에는 SKU와 수량이 있다.
    """
    orderid: str
    sku: str
    qty: int


class Batch:
    """
    재고 배치는 유일한 ID, SKU, 수량으로 이루어진다.

    배치에 주문 라인을 할당해야한다. 주문 라인을 배치에 할당하면 해당 배치에 속하는 재고를 고객의 주소로 배송한다.

    어떤 배치의 재고를 주문 라인에 x단위로 할당하면 가용 재고 수량은 x만큼 줄어든다.

    배치의 가용 재고 수량이 주문 라인의 수량보다 작으면 이  주문 라인을  배치에 할당 할  수 없다.

    배치가 현재 배송중이면 ETA 정보가 배치에 들어있다. ETA가 없는 배치는 창고 재고다.
    """
    def __init__(
            self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref # ID
        self.sku = sku # product Name. 제품 명
        self.eta = eta  #eta는 있을수도, 없을수도.
        self._purchased_quantity = qty
        self._allocations = set() #  type : Set[OrderLine]

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        # 배치의 sku와, 주문 라인의 sku가 동일해야 함, 재고 수량도 주문 라인 수량보다 많아야 하고;
        return self.sku == line.sku and self.available_quantity >= line.qty