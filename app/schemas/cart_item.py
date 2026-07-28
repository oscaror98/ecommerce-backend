from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CartItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int

    model_config = ConfigDict(from_attributes=True)