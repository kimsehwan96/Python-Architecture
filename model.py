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