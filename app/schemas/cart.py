from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CartResponse(BaseModel):
    id: UUID
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)