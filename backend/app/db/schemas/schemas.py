from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, time
from typing import Optional, Literal, List
from datetime import time, datetime

class BaristaOut(BaseModel):
    name: str
    ssn: str
    email: str
    salary: float
    days_working: List[str]
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)

class BaristaIn(BaseModel):
    ssn: str
    name: str
    email: str
    salary: float
    days_working: List[str]
    start_time: time 
    end_time: time

    model_config = ConfigDict(from_attributes=True)

class ManagerOut(BaseModel):
    name: str
    ssn: str
    ownership: float

    model_config = ConfigDict(from_attributes=True)

class InventoryOut(BaseModel):
    name: str
    unit: str
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)

class InventoryIn(BaseModel):
    manager_ssn: str
    item_name: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class Employee(BaseModel):
    ssn: str
    name: str
    email: EmailStr
    salary: float

    model_config = ConfigDict(from_attributes=True)

class SimpleReportParams(BaseModel):
    start_date: datetime
    end_date: datetime
    isVerbose: bool = False

    model_config = ConfigDict(from_attributes=True)

class VerboseReportParams(BaseModel):
    start_date: datetime
    end_date: datetime
    isVerbose: bool = True

    model_config = ConfigDict(from_attributes=True)

class OrderItem(BaseModel):
    item_name: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class OrderIn(BaseModel):
    barista_ssn: str
    payment_method: Literal["Cash", "Card"]
    order_info: List[OrderItem]  # List of dictionaries with item name and 

    model_config = ConfigDict(from_attributes=True)

class SalesReportInfo(BaseModel):
    order_id: int
    timestamp: datetime
    total_amt: float
    payment_method: str
    prepared_by: str

    model_config = ConfigDict(from_attributes=True)

class SalesReportOut(BaseModel):
    report: list[SalesReportInfo]

    model_config = ConfigDict(from_attributes=True)

class RefillReportInfo(BaseModel):
    refill_id: int
    timestamp: datetime
    total_amt: float
    placed_by: str

    model_config = ConfigDict(from_attributes=True)

class RefillReportOut(BaseModel):
    report: list[RefillReportInfo]

    model_config = ConfigDict(from_attributes=True)

class BalanceReportInfo(BaseModel):
    type: str
    trans_id: int
    timestamp: datetime
    total_amt: float
    balance: float

    model_config = ConfigDict(from_attributes=True)

class BalanceReportOut(BaseModel):
    report: list[BalanceReportInfo]

    model_config = ConfigDict(from_attributes=True)


""" class MenuItemSchema(BaseModel):
    name: str
    type: str
    size: str
    price: float
    hot_or_cold: str

    model_config = ConfigDict(from_attributes=True) """


""" class OrderSchema(BaseModel):
    timestamp: datetime
    total_amt: float
    payment_method: Literal["Cash", "Card"]
    prepared_by: str

    model_config = ConfigDict(from_attributes=True) """


""" class Manager(BaseModel):
    ssn: str
    ownership: float

    model_config = ConfigDict(from_attributes=True) """


""" class Barista(BaseModel):
    ssn: str
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True) """


""" class Day(BaseModel):
    barista_ssn: str
    day: str

    model_config = ConfigDict(from_attributes=True) """


""" class CustomerOrders(BaseModel):
    order_id: int
    menu_item: str
    item_quant: int

    model_config = ConfigDict(from_attributes=True) """


""" class Promotion(BaseModel):
    promo_id: int
    discount: float
    day: str
    description: str

    model_config = ConfigDict(from_attributes=True) """


""" class PromoWindow(BaseModel):
    promo_id: int
    start_time: time
    end_time: time
    day: str

    model_config = ConfigDict(from_attributes=True) """


""" class PromotedMenuItems(BaseModel):
    promo_id: int
    name: str

    model_config = ConfigDict(from_attributes=True) """


""" class Recipe(BaseModel):
    recipe_id: int
    recipe_name: str
    description: str

    model_config = ConfigDict(from_attributes=True) """


""" class RecipeSteps(BaseModel):
    recipe_id: int
    step_name: Optional[str]
    procedure: Optional[str]
    position: int

    model_config = ConfigDict(from_attributes=True) """


""" class Inventory(BaseModel):
    name: str
    unit: str
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True) """


""" class RecipeIngredients(BaseModel):
    inventory_name: str
    recipe_id: int
    quantity: float

    model_config = ConfigDict(from_attributes=True) """


""" class Refill(BaseModel):
    refill_id: int
    timestamp: time
    total_amt: float
    placed_by: str

    model_config = ConfigDict(from_attributes=True) """


""" class Restocks(BaseModel):
    inventory_name: str
    refill_id: int
    refill_quant: int

    model_config = ConfigDict(from_attributes=True) """


""" class Transactions(BaseModel):
    trans_id: Optional[int]
    timestamp: Optional[datetime]
    type: Literal['order', 'refill']
    balance: float

    model_config = ConfigDict(from_attributes=True) """


""" class OrderUpdate(BaseModel):
    trans_id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True) """


""" class RefillUpdate(BaseModel):
    trans_id: int
    refill_id: int

    model_config = ConfigDict(from_attributes=True) """
