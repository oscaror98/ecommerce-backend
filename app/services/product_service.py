from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def create_product(self, data: ProductCreate) -> Product:

        category = self.category_repository.get_by_id(data.category_id)

        if category is None:
            raise ValueError("Category not found")

        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            stock=data.stock,
            image_url=data.image_url,
            category_id=data.category_id,
        )

        return self.product_repository.create(product)

    def get_products(self) -> list[Product]:
        return self.product_repository.get_all()

    def get_product(self, product_id: UUID) -> Product:

        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ValueError("Product not found")

        return product

    def update_product(
        self,
        product_id: UUID,
        data: ProductUpdate,
    ) -> Product:

        product = self.get_product(product_id)

        category = self.category_repository.get_by_id(data.category_id)

        if category is None:
            raise ValueError("Category not found")

        product.name = data.name
        product.description = data.description
        product.price = data.price
        product.stock = data.stock
        product.image_url = data.image_url
        product.category_id = data.category_id
        product.is_active = data.is_active

        return self.product_repository.update(product)

    def delete_product(self, product_id: UUID) -> None:

        product = self.get_product(product_id)

        self.product_repository.delete(product)

    def get_products(
        self,
        search: str | None = None,
        category_id: UUID | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Product]:

        return self.product_repository.get_all(
            search=search,
            category_id=category_id,
            skip=skip,
            limit=limit,
        )