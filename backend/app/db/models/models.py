from sqlalchemy import (
    # Table organization
    Column, ForeignKey, CheckConstraint, PrimaryKeyConstraint, 
    # Data types
    String, Float, Integer, DateTime, Enum, Numeric, Time, Text, TIMESTAMP
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"

    ssn = Column(String(11), primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    salary = Column(Numeric(8,2))

    __table_args__ = (
        CheckConstraint("ssn ~ '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'", name="check_ssn_format"),
        CheckConstraint("email ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'", name="check_email_format")
    )

class Manager(Base):
    __tablename__ = "manager"

    ssn = Column(String(11), ForeignKey('employee.ssn',ondelete="CASCADE"), primary_key=True)
    ownership = Column(Numeric(5, 2), nullable=True)

    __table_args__ = (
        CheckConstraint("ownership >= 0 AND ownership <= 100", name="check_ownership_range"),
    )

class Barista(Base):
    __tablename__ = "barista"

    ssn = Column(String(11), ForeignKey('employee.ssn',ondelete="CASCADE"), primary_key=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)

class Day(Base):
    __tablename__ = "day"

    barista_ssn = Column(String(11), ForeignKey('barista.ssn',ondelete="CASCADE"), primary_key=True)
    day = Column(String(10), primary_key=True)

class PaymentMethodEnum(enum.Enum):
    Cash = "cash"
    Credit_Card = "credit_card"
    Debit_Card = "debit_card"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    total_amt = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethodEnum), nullable=False)
    prepared_by = Column(String,ForeignKey('barista.ssn',ondelete="SET NULL"), nullable=True)

class MenuItem(Base):
    __tablename__ = "menuitem"

    name = Column(String, primary_key=True ,nullable=False)
    type = Column(String, nullable=False)
    size = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    hot_or_cold = Column(String, nullable=False)

class CustomerOrder(Base):
    __tablename__ = "customer_orders"

    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    menu_item = Column(String(50), ForeignKey('menuitem.name'), nullable=False)
    item_quant = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('item_quant > 0', name='check_item_quant_positive'),
        PrimaryKeyConstraint('order_id', 'menu_item', name='pk_customer_orders')
    )
# create all models according to the database schema

class Promotion(Base):
    __tablename__ = "promotion"

    promo_id = Column(Integer, primary_key=True, autoincrement=True)
    discount = Column(Numeric(4, 2), nullable=False)
    day = Column(String(10), nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    description = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint('discount >= 0 AND discount <= 100', name='check_discount_range'),
    )

# class PromoWindow(Base):
#     __tablename__ = "promo_window"

#     promo_id = Column(Integer, ForeignKey('promotion.promo_id'), primary_key=True)
#     start_time = Column(Time, nullable=True)
#     end_time = Column(Time, nullable=True)
#     day = Column(String(10), nullable=True)

class PromotedMenuItems(Base):
    __tablename__ = "promoted_menu_items"

    promo_id = Column(Integer, ForeignKey('promotion.promo_id'), primary_key=True)
    name = Column(String(50), ForeignKey('menuitem.name'), primary_key=True)

class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_name = Column(String(50), ForeignKey('menuitem.name'), nullable=True)
    description = Column(Text, nullable=True)

class RecipeSteps(Base):
    __tablename__ = "recipe_steps"

    recipe_id = Column(Integer, ForeignKey('recipe.recipe_id'), primary_key=True)
    step_name = Column(Text, nullable=True)
    procedure = Column(Text, nullable=True)
    position = Column(Integer, primary_key=True)

class Inventory(Base):
    __tablename__ = "inventory"

    name = Column(Text, primary_key=True)
    unit = Column(String(20), nullable=True)
    price = Column(Numeric(6, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
    )

class RecipeIngredients(Base):
    __tablename__ = "recipe_ingredients"

    inventory_name = Column(Text, ForeignKey('inventory.name'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.recipe_id'), primary_key=True)
    quantity = Column(Numeric, nullable=True)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
    )

class Refill(Base):
    __tablename__ = "refill"

    refill_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    total_amt = Column(Numeric(7, 2), nullable=True)
    placed_by = Column(String(11), ForeignKey('manager.ssn'), nullable=True)

class Restocks(Base):
    __tablename__ = "restocks"

    inventory_name = Column(String(100), ForeignKey('inventory.name'), primary_key=True)
    refill_id = Column(Integer, ForeignKey('refill.refill_id'), primary_key=True)
    refill_quant = Column(Integer, nullable=True)

class Transactions(Base):
    __tablename__ = "transactions"

    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    type = Column(String(20), nullable=False)
    balance = Column(Numeric(7, 2), nullable=True)

    __table_args__ = (
        CheckConstraint("type IN ('refill', 'order')", name="check_transaction_type"),
    )

class OrderUpdate(Base):
    __tablename__ = "order_update"

    trans_id = Column(Integer, ForeignKey('transactions.trans_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)

class RefillUpdate(Base):
    __tablename__ = "refil_update"

    trans_id = Column(Integer, ForeignKey('transactions.trans_id'), primary_key=True)
    refill_id = Column(Integer, ForeignKey('refill.refill_id'), nullable=False)