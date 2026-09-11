import asyncio
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import delete

from app.db.engine import AdminSessionLocal
from app.db.models import (
    Customer,
    Order,
    OrderItem,
    Payment,
    Product,
    SupportTicket,
)


async def seed_database() -> None:
    async with AdminSessionLocal() as session:
        # Clear existing data.
        await session.execute(delete(SupportTicket))
        await session.execute(delete(Payment))
        await session.execute(delete(OrderItem))
        await session.execute(delete(Order))
        await session.execute(delete(Product))
        await session.execute(delete(Customer))

        now = datetime.now(timezone.utc)

        customers = [
            Customer(
                name="Ali Khan",
                email="ali@example.com",
                segment="premium",
                country="Pakistan",
                created_at=now,
            ),
            Customer(
                name="Sara Ahmed",
                email="sara@example.com",
                segment="standard",
                country="Pakistan",
                created_at=now,
            ),
            Customer(
                name="John Smith",
                email="john@example.com",
                segment="premium",
                country="United States",
                created_at=now,
            ),
            Customer(
                name="Emma Wilson",
                email="emma@example.com",
                segment="standard",
                country="United Kingdom",
                created_at=now,
            ),
            Customer(
                name="Omar Hassan",
                email="omar@example.com",
                segment="premium",
                country="United Arab Emirates",
                created_at=now,
            ),
        ]

        session.add_all(customers)
        await session.flush()

        products = [
            Product(
                name="Laptop Pro 15",
                category="electronics",
                price=Decimal("1499.99"),
            ),
            Product(
                name="Wireless Headphones",
                category="electronics",
                price=Decimal("199.99"),
            ),
            Product(
                name="Mechanical Keyboard",
                category="accessories",
                price=Decimal("129.99"),
            ),
            Product(
                name="4K Monitor",
                category="electronics",
                price=Decimal("499.99"),
            ),
            Product(
                name="USB-C Dock",
                category="accessories",
                price=Decimal("159.99"),
            ),
        ]

        session.add_all(products)
        await session.flush()

        orders = [
            Order(
                customer_id=customers[0].id,
                status="completed",
                total_amount=Decimal("1699.98"),
                created_at=now,
            ),
            Order(
                customer_id=customers[1].id,
                status="completed",
                total_amount=Decimal("129.99"),
                created_at=now,
            ),
            Order(
                customer_id=customers[2].id,
                status="pending",
                total_amount=Decimal("499.99"),
                created_at=now,
            ),
            Order(
                customer_id=customers[3].id,
                status="completed",
                total_amount=Decimal("159.99"),
                created_at=now,
            ),
            Order(
                customer_id=customers[4].id,
                status="cancelled",
                total_amount=Decimal("199.99"),
                created_at=now,
            ),
        ]

        session.add_all(orders)
        await session.flush()

        order_items = [
            OrderItem(
                order_id=orders[0].id,
                product_id=products[0].id,
                quantity=1,
                unit_price=Decimal("1499.99"),
            ),
            OrderItem(
                order_id=orders[0].id,
                product_id=products[1].id,
                quantity=1,
                unit_price=Decimal("199.99"),
            ),
            OrderItem(
                order_id=orders[1].id,
                product_id=products[2].id,
                quantity=1,
                unit_price=Decimal("129.99"),
            ),
            OrderItem(
                order_id=orders[2].id,
                product_id=products[3].id,
                quantity=1,
                unit_price=Decimal("499.99"),
            ),
            OrderItem(
                order_id=orders[3].id,
                product_id=products[4].id,
                quantity=1,
                unit_price=Decimal("159.99"),
            ),
            OrderItem(
                order_id=orders[4].id,
                product_id=products[1].id,
                quantity=1,
                unit_price=Decimal("199.99"),
            ),
        ]

        session.add_all(order_items)

        payments = [
            Payment(
                order_id=orders[0].id,
                status="successful",
                amount=Decimal("1699.98"),
                payment_method="credit_card",
                created_at=now,
            ),
            Payment(
                order_id=orders[1].id,
                status="successful",
                amount=Decimal("129.99"),
                payment_method="paypal",
                created_at=now,
            ),
            Payment(
                order_id=orders[2].id,
                status="failed",
                amount=Decimal("499.99"),
                payment_method="credit_card",
                created_at=now,
            ),
            Payment(
                order_id=orders[3].id,
                status="successful",
                amount=Decimal("159.99"),
                payment_method="bank_transfer",
                created_at=now,
            ),
            Payment(
                order_id=orders[4].id,
                status="failed",
                amount=Decimal("199.99"),
                payment_method="credit_card",
                created_at=now,
            ),
        ]

        session.add_all(payments)

        support_tickets = [
            SupportTicket(
                customer_id=customers[0].id,
                category="payment",
                status="open",
                priority="high",
                created_at=now,
            ),
            SupportTicket(
                customer_id=customers[1].id,
                category="delivery",
                status="closed",
                priority="medium",
                created_at=now,
            ),
            SupportTicket(
                customer_id=customers[2].id,
                category="technical",
                status="open",
                priority="high",
                created_at=now,
            ),
            SupportTicket(
                customer_id=customers[4].id,
                category="payment",
                status="open",
                priority="critical",
                created_at=now,
            ),
        ]

        session.add_all(support_tickets)

        await session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    asyncio.run(seed_database())