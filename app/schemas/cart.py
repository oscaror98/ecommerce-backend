from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CartItemDetail(BaseModel):
    product_id: UUID
    name: str
    price: Decimal
    quantity: int
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: list[CartItemDetail]
    total: Decimal

    model_config = ConfigDict(from_attributes=True)