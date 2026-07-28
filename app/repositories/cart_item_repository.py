from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cart_item import CartItem


class CartItemRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_item(
        self,
        cart_id: UUID,
        product_id: UUID,
    ) -> CartItem | None:

        return (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    def create(self, item: CartItem) -> CartItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: CartItem) -> CartItem:
        self.db.commit()
        self.db.refresh(item)
        return item