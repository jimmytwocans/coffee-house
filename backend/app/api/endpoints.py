# Combined FastAPI endpoints for all entities
from fastapi import APIRouter
from app.services.services import (
    get_menu_items, get_baristas, get_managers, 
    hire_employee, refill, get_inventory, 
    place_customer_orders, fire_employee, update_employee_info, 
    run_sales_report, get_refill_reports, get_balance_report
)
from app.db.schemas.schemas import (
    BaristaOut, BaristaIn, ManagerOut, 
    InventoryOut, InventoryIn, OrderIn, 
    Employee, SimpleReportParams, VerboseReportParams, 
    SalesReportOut, RefillReportOut, BalanceReportOut)

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "API is working"}

@router.get("/menuitems")
async def get_menu_items_from_db():
    return get_menu_items()

@router.get("/inventory",response_model=list[InventoryOut])
async def get_inventory_from_db():
    return get_inventory()

@router.post("/baristas")
async def hire_employee_in_db(employee_data: BaristaIn):
    return hire_employee(employee_data.model_dump())

@router.get("/baristas", response_model=list[BaristaOut])
async def get_baristas_from_db():
    return get_baristas()

@router.get("/managers",response_model=list[ManagerOut])
async def get_managers_from_db():
    return get_managers()

# remove employee from db
@router.delete("/baristas/{ssn}")
async def remove_employee_from_db(ssn: str):
    print(f"Removing employee with SSN: {ssn}")
    print(f"SSN type: {type(ssn)}")
    return fire_employee(ssn)

@router.put("/baristas/{ssn}")
async def update_employee(employee_data: Employee):
    return update_employee_info(employee_data.model_dump())

@router.post("/refill")
async def refill_db(refill_data: InventoryIn):
    return refill(refill_data.model_dump())

@router.get("/inventory/{name}", response_model=InventoryOut)
async def get_inventory_item(name: str):
    inventory = get_inventory()
    for item in inventory:
        if item.name == name:
            return item
    return {"error": "Item not found"}

@router.get("/reports/simple/sales", response_model=str)
async def get_sales_report_from_db(report_params: SimpleReportParams):
    return run_sales_report(report_params.model_dump())

@router.get("/reports/simple/refill", response_model=str)
async def get_refill_report_from_db(report_params: SimpleReportParams):
    return get_refill_reports(report_params.model_dump())

@router.get("/reports/simple/balance", response_model=str)
async def get_balance_report_from_db(report_params: SimpleReportParams):
    return get_balance_report(report_params.model_dump())

@router.get("/reports/verbose/sales", response_model=SalesReportOut)
async def get_sales_report_from_db(report_params: VerboseReportParams):
    return run_sales_report(report_params.model_dump())

@router.get("/reports/verbose/refill", response_model=RefillReportOut)
async def get_refill_report_from_db(report_params: VerboseReportParams):
    return get_refill_reports(report_params.model_dump())

@router.get("/reports/verbose/balance", response_model=BalanceReportOut)
async def get_balance_report_from_db(report_params: VerboseReportParams):
    return get_balance_report(report_params.model_dump())

@router.post("/order")
async def create_order(order_data: OrderIn):
    return place_customer_orders(order_data.model_dump())
