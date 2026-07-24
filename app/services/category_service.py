from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate


class CategoryService:

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create_category(self, data: CategoryCreate) -> Category:

        existing = self.repository.get_by_name(data.name)

        if existing:
            raise ValueError("Category already exists")

        category = Category(
            name=data.name,
            description=data.description,
        )

        return self.repository.create(category)

    def get_categories(self):
        return self.repository.get_all()