from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cart import Cart


class CartRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: UUID) -> Cart | None:
        return (
            self.db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

    def create(self, cart: Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart