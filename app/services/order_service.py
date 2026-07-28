from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.cart_repository import CartRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository


class OrderService:

    def __init__(self, db: Session):
        self.db = db
        self.order_repository = OrderRepository(db)
        self.order_item_repository = OrderItemRepository(db)
        self.cart_repository = CartRepository(db)
        self.product_repository = ProductRepository(db)

    def checkout(self, user_id):
        cart = self.cart_repository.get_by_user_id(user_id)

        if not cart:
            raise ValueError("Cart not found")

        if not cart.items:
            raise ValueError("Cart is empty")

        total = Decimal("0.00")

        for item in cart.items:
            if item.quantity > item.product.stock:
                raise ValueError(
                    f"Not enough stock for {item.product.name}"
                )

            total += item.product.price * item.quantity

        order = Order(
            user_id=user_id,
            total=total,
        )

        self.order_repository.create(order)

        for item in cart.items:

            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price,
            )

            self.order_item_repository.create(order_item)

            item.product.stock -= item.quantity

        self.cart_repository.clear_cart(cart)

        self.db.commit()

        self.db.refresh(order)

        return order