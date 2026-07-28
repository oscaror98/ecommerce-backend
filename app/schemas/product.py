from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    image_url: str | None = None
    category_id: UUID


class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    image_url: str | None = None
    category_id: UUID
    is_active: bool


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    stock: int
    image_url: str | None
    is_active: bool
    category_id: UUID

    model_config = ConfigDict(from_attributes=True)