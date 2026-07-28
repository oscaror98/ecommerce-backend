from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.user import User
from app.repositories.cart_item_repository import CartItemRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartItemDetail, CartResponse
from app.schemas.cart_item import CartItemCreate


class CartService:

    def __init__(self, db: Session):
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)

    def get_or_create_cart(self, user: User) -> Cart:

        cart = self.cart_repository.get_by_user_id(user.id)

        if cart:
            return cart

        cart = Cart(user_id=user.id)

        return self.cart_repository.create(cart)

    def get_cart(self, user: User) -> CartResponse:

        cart = self.get_or_create_cart(user)

        items = []
        total = Decimal("0.00")

        for item in cart.items:

            subtotal = item.product.price * item.quantity

            total += subtotal

            items.append(
                CartItemDetail(
                    product_id=item.product.id,
                    name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                    subtotal=subtotal,
                )
            )

        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            items=items,
            total=total,
        )

    def add_item(
        self,
        user: User,
        data: CartItemCreate,
    ):

        cart = self.get_or_create_cart(user)

        product = self.product_repository.get_by_id(data.product_id)

        if product is None:
            raise ValueError("Product not found")

        if product.stock < data.quantity:
            raise ValueError("Not enough stock")

        item = self.cart_item_repository.get_item(
            cart.id,
            data.product_id,
        )

        if item:

            new_quantity = item.quantity + data.quantity

            if new_quantity > product.stock:
                raise ValueError("Not enough stock")

            item.quantity = new_quantity

            return self.cart_item_repository.update(item)

        item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity,
        )

        return self.cart_item_repository.create(item)

    def remove_item(
        self,
        user: User,
        product_id,
    ):

        cart = self.get_or_create_cart(user)

        item = self.cart_item_repository.get_item(
            cart.id,
            product_id,
        )

        if item is None:
            raise ValueError("Product not found in cart")

        self.cart_item_repository.delete(item)