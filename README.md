# Python Architecture study

## Chapter1 도메인 모델링

도메인이란 우리가 해결해야 할 문제를 의미함.

모델은 유용한 특성을 포함하는 프로세스나 map 을 의미함.

도메인 모델을 이해하려면 우리가 해결하고자 하는 문제(도메인)에 대한 전문가와 이야기 해야 하며, 그들의 전문 용어를 기록해야 한다.

전문가들과 대화를 할 때 최초로 만들 최소한의 도메인 모델에 사용할 용어와 규칙 몇 가지를 정해야 하며, 가능 한 각 규칙을 잘 보여주는 구체적인 예제를 요청하는게 좋다.

아래는 그 예시

```text
제품은 SKU 로 식별된다. SKU는 재고 유지 단위의 약자다.

고객은 주문을 넣는다. 주문은 주문 참조 번호에 의해 식별된다. 한줄 이상의 주문 라인을 포함한다.

각 주문 라인에는 SKU와 수량이 있다. 

구매 부서는 재고를 작은 배치로 주문한다. 재고 배치는 유일한 ID(참조 번호라고 부름), SKU, 수량으로 이루어 진다.

배치에 주문 라인을 할당해야 한다. 주문 라인을 배치에 할당하면 해당 배치에 속하는 재고를 고객의 주소로 배송한다. 어떤 배치의 재고를 주문 라인에 x단위로 할당하면, 가용 재고 수량은 x만큼 줄어든다.

예를들면 아래와 같다

20단위의 TABLE 로 이루어진 배치가 있고 , 2단위의 TABLE 을 요구하는 주문 라인이 있다.

해당 배치에 예시와 같은 주문 라인을 배치하면, 18단위의 TABLE이 남아야 한다.

배치의 가용 재고 수량이 주문 라인의 수량보다 작으면 주문 라인을 배치에 할당 할 수 없다.

같은 주문 라인을 두 번 이상 할당해서는 안 된다.

배치가 현재 배송중이면 ETA 정보가 배치에 들어있다. ETA가 없는 배치는 창고 재고다. 창고 재고를 배송 중인 배치보다(창고로 배송 중인) 더 먼저 할당 해야 한다. 배송 중인 배치를 할당 할 때는 ETA가 가장 빠른 배치를 먼저 할당한다.

ETA는 도착 예정 시각으로 날짜 (연/월/일)를 기록한다. 
```

전문가와의 대화를 통해 위와 같은 프로세스를 인지했고, 이를 코드로 구현하기 위해서는 아래와 같이 생각을 하면 좋다. (도메인 주도 개발)

1. pydantic / dataclasses 등으로 모델링 및 기타 클래스화 할 요소가 무엇이 있는지 확인해보기. (위에서는 주문라인, 배치 등이 있다.)
2. TDD와 병행한다. 위 노트에 적혀져있는 시나리오를 포함한 테스트를 작성한다.

위 정보를 토대로 `model.py`를 아래와 같이 작성해보았다.

```python3
import dataclasses
from datetime import date
from typing import Optional

@dataclasses.dataclass(frozen=True)
class OrderLine:
    orderId: str
    sku: str
    quantity: int

class Batch:
    def __init__(
        self,
        reference: str,
        sku: str,
        available_quantity: int,
        eta: Optional[date] = None
    ) -> None:
        self.reference = reference
        self.sku = sku
        self.available_quantity = available_quantity
        self.eta = eta
    
    def can_allocate(self, orderLine) -> bool: 
        return orderLine.sku == self.sku and self.available_quantity >= orderLine.quantity

    def allocate(self, orderLine: OrderLine) -> None:
        if orderLine.sku is not self.sku:
            raise RuntimeError(
                f"You can't allocate {orderLine.orderId} OrderLine in \
                {self.reference} Batch because each other's sku isn't same \
                Orderline sku : {orderLine.sku}\n \
                Batch sku : {self.sku}")
        if self.can_allocate(orderLine=orderLine):
            self.available_quantity -= orderLine.quantity
```

(왜 이렇게 구현했는지 내용 추가)

위 정보를 토대로 간단한 최초의 테스트 코드를 아래와 같이 작성하였다.

```python3
from datetime import date, timedelta
import pytest
from model import OrderLine, Batch
# from model import ...

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-1", "RED-TABLE", 20, date.today())
    line = OrderLine("ref1", "RED-TABLE", 2)

    batch.allocate(line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    pytest.fail("todo")


def test_cannot_allocate_if_available_smaller_than_required():
    pytest.fail("todo")


def test_can_allocate_if_available_equal_to_required():
    pytest.fail("todo")


def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")

```