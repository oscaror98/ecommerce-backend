from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = ProductService(db)

    try:
        return service.create_product(product)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_products(
    search: str | None = None,
    category_id: UUID | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = ProductService(db)

    return service.get_products(
        search=search,
        category_id=category_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = ProductService(db)

    try:
        return service.get_product(product_id)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: UUID,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = ProductService(db)

    try:
        return service.update_product(product_id, product)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = ProductService(db)

    try:
        service.delete_product(product_id)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )