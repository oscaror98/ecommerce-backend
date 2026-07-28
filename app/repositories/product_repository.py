from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all(
        self,
        search: str | None = None,
        category_id: UUID | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Product]:

        query = self.db.query(Product)

        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        if category_id:
            query = query.filter(Product.category_id == category_id)

        return (
            query.order_by(Product.name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, product_id: UUID) -> Product | None:
        return self.db.get(Product, product_id)

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()