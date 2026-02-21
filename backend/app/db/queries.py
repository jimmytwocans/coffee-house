# from dbclient import db_client
import re
from app.db.models.models import (
    # Employee
    Employee, Barista, Manager, Day,
    # Inventory
    MenuItem, Inventory, RecipeIngredients,
    # Finances
    Transactions,  Order, Refill, Restocks, RefillUpdate, CustomerOrder, OrderUpdate, Recipe)
from app.db.dbclient import get_db
from sqlalchemy import func
from decimal import Decimal

class QueryError(Exception):
    """Custom exception for query errors."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

##################################################
# fetch_menu_items()
#
# Returns all menu items from the database.
# Returns None if there is an error in the query.
##################################################
def fetch_menu_items():
    """
    Fetch menu items from the database for a given menu ID.
    """
    try:
        db = next(get_db())
        # query = db.query(MenuItem).all()
        return db.query(MenuItem).all()
    except Exception as e:
        raise QueryError("Error fetching menu items in query", details={"error": str(e)})
    
##################################################
# fetch_inventory()
#
# Returns all inventory items from the database.
# Returns None if there is an error in the query.
##################################################
def fetch_inventory():
    """
    Fetch inventory items from the database.
    """
    try:
        db = next(get_db())
        # query = db.query(Inventory).all()
        return db.query(Inventory).all()
    except Exception as e:
        raise QueryError("Error fetching inventory items in query", details={"error": str(e)})

##################################################
# EMPLOYEE MANAGEMENT
##################################################

##################################################
# add_employee(employee_data)
# Adds employee to the database.
# Also adds employee to the barista table.
#
# Parameter:
#   employee_data should be a dictionary 
#       containing employee details
#       e.g., {ssn, name, email, salary}
#
# Returns the new employee object 
#   if added successfully.
# Returns None if there was an error in the query.
##################################################
def add_employee(employee_data):
    """
    Add a new employee to the database.
    """
    try:
        db = next(get_db())

        # Add the employee to the employee table
        employee_table = {
            'ssn': employee_data['ssn'],
            'name': employee_data['name'],
            'email': employee_data['email'],
            'salary': employee_data['salary']
        }
        new_employee = Employee(**employee_table)
        db.add(new_employee)

        db.flush()

        barista_table = {
            'ssn': employee_data['ssn'],
            'start_time': employee_data['start_time'],
            'end_time': employee_data['end_time']
        }
        # Add employee to the barista table
        new_barista = Barista(**barista_table)
        db.add(new_barista)

        db.flush()

        for day in employee_data['days_working']:
            new_day = Day(barista_ssn=employee_data['ssn'], day=day)
            db.add(new_day)

        db.commit()
        return new_employee
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error adding employee in query error"+str(e))

##################################################
# add_manager(ssn)
#
# Adds a new manager to the database.
#
# Parameter:
#   ssn should be a string in 
#       the format XXX-XX-XXXX.
#
# Returns the new manager object if 
#         added successfully.
# Returns None if there was an error in the query.
##################################################
def add_manager(ssn):
    """
    Add a new manager to the database.
    """
    try:
        db = next(get_db())

        # add new manager
        new_manager = Manager(ssn=ssn)
        db.add(new_manager)

        db.commit()
        return new_manager
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error adding manager in query", details={"error": str(e)})

##################################################
# fetch_managers()
# 
# Returns a list of all managers from
# the database.
# Returns None if there is an error in the query.
##################################################    
def fetch_managers():
    """
    Fetch managers from the database.
    """
    try:
        db = next(get_db())
        # query = db.query(Manager).all()
        result = db.query(
            Employee.name,
            Employee.ssn,
            Manager.ownership
        ).join(Manager, Employee.ssn == Manager.ssn).all()
        return result
    except Exception as e:
        raise QueryError("Error fetching managers in query", details={"error": str(e)})

###################################################
# update_manager_ownership(ownership)
#
# Updates the ownership percentage of all managers 
# in the database to be equal.
#
# Parameter:
#   ownership should be a float or int.
#
# Returns True if the ownership was 
#   updated successfully.
# Returns False if there was an error 
#   in the query.
###################################################
def update_manager_ownership(ownership):
    """
    Update manager ownership in the database.
    """
    try:
        db = next(get_db())

        managers = db.query(Manager).all()
        for manager in managers:
            manager.ownership = ownership

        db.commit()
    except Exception as e:
        raise QueryError("Error updating manager ownership in query", details={"error": str(e)})

##################################################
# fetch_baristas()
#
# Returns a list of all baristas from
# the database.
# Returns None if there is an error in the query.
##################################################
def fetch_baristas():
    """
    Fetch baristas from the database.
    Returns:
        A list of dictionaries, where each dictionary contains:
        - name: str
        - ssn: str
        - email: str
        - salary: float
        - days_working: List[str]
        - start_time: time
        - end_time: time
    """
    try:
        db = next(get_db())

        # Fetch baristas and their working days
        baristas = db.query(
            Employee.name,
            Employee.ssn,
            Employee.email,
            Employee.salary,
            Barista.start_time,
            Barista.end_time
        ).join(Barista, Employee.ssn == Barista.ssn).all()

        # Fetch days for each barista
        days_by_barista = db.query(Day.barista_ssn, Day.day).all()

        # Group days by barista SSN
        days_working = {}
        for day in days_by_barista:
            if day.barista_ssn not in days_working:
                days_working[day.barista_ssn] = []
            days_working[day.barista_ssn].append(day.day)

        # Combine barista data with their working days
        result = []
        for barista in baristas:
            result.append({
                "name": barista.name,
                "ssn": barista.ssn,
                "email": barista.email,
                "salary": barista.salary,
                "days_working": days_working.get(barista.ssn, []),
                "start_time": barista.start_time,
                "end_time": barista.end_time
            })

        return result
    except Exception as e:
        raise QueryError("Error fetching baristas in query", details={"error": str(e)})
    
##################################################
# delete_employee(ssn)
#
# Deletes an employee from the database.
# Cascades delete from barista and manager tables.
#
# Parameter:
#   ssn should be a string in 
#       the format XXX-XX-XXXX.
#
# Returns True if the employee was 
#              deleted successfully.
# Returns False if there was an error 
#               in the query.
##################################################
def delete_employee(ssn):
    """
    Delete an employee from the database.
    """
    try:
        db = next(get_db())

        # delete employee from employee table
        # will cascade delete from barista and manager tables due to foreign key constraints
        db.query(Employee).filter(Employee.ssn == ssn).delete()

        db.commit()
        return True
    except Exception as e:
        raise QueryError("Error deleting employee in query"+" error"+str(e))

def fetch_one_manager(ssn):
    """
    Fetch a single manager from the database.
    """
    # validate ssn format
    if not isinstance(ssn, str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
        raise QueryError("Invalid SSN format. Expected format: XXX-XX-XXXX")

    try:
        db = next(get_db())
        # query = db.query(Manager).filter(Manager.ssn == ssn).first()
        result = db.query(
            Employee.name,
            Employee.ssn,
            Manager.ownership
        ).join(Manager, Employee.ssn == Manager.ssn).filter(Manager.ssn == ssn).first()
        return result
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error fetching manager in query", details={"error": str(e)})


##################################################
# schedule_barista_shifts(ssn, start_time, end_time, days)
# 
# Schedules barista shifts in the database.
#
# Parameters:
#   ssn should be a string in the 
#       format XXX-XX-XXXX.
#   start_time should be a string in the 
#              format HH:MM:SS.
#   end_time should be a string in the 
#            format HH:MM:SS.
#   days should be a list of strings representing 
#        the days of the week. 
# 
# Returns:
#    - True if the shifts were 
#           scheduled successfully.
#    - False if there was an error in the query.
##################################################    
def schedule_barista_shifts(ssn, start_time=None, end_time=None, days=None):
    """
    Schedule barista shifts in the database.
    """
    try:
        db = next(get_db())

        # check if barista exists
        barista = db.query(Barista).filter(Barista.ssn == ssn).first()
        if not barista:
            raise QueryError("Barista does not exist")

        # Ensure that if the barista has no shifts scheduled, start_time, end_time, and days cannot be None
        if not barista.start_time and not barista.end_time and not db.query(Day).filter(Day.barista_ssn == ssn).first():
            if not start_time or not end_time or not days:
                raise QueryError("Barista has no shifts scheduled. Start time, end time, and days cannot be None.")

        # update start and end time if provided
        if start_time:
            barista.start_time = start_time
        if end_time:
            barista.end_time = end_time

        # update days if provided
        if days:
            for day in days:
                db.query(Day).filter(Day.barista_ssn == ssn).filter(Day.day == day).update({"day": day})

        db.commit()
        return True
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error scheduling barista shifts in query", details={"error": str(e)})
    
##################################################
# change_employee_info(ssn, name, email, salary)
#
# Changes employee information in the database.
#
# Parameters:
#   ssn should be a string in the 
#       format XXX-XX-XXXX.
#   name should be a string.
#   email should be a string in the 
#         format name@website.com
#   salary should be a float or int.
# 
# Returns True if the employee information 
#              was changed successfully.
# Returns False if there was an error in the query.
################################################## 
def change_employee_info(ssn, name=None, email=None, salary=None):
    """
    Change employee information in the database.
    """
    try:
        db = next(get_db())

        # fetch employee
        employee = db.query(Employee).filter(Employee.ssn == ssn).first()
        if not employee:
            raise QueryError("Employee does not exist in database")

        # update employee information
        if name:
            employee.name = name
        if email:
            employee.email = email
        if salary:
            employee.salary = salary

        db.commit()
        return True
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error changing employee information in query", details={"error": str(e)})

##################################################
# INVENTORY MANAGEMENT
##################################################

##################################################
# order_inventory_items(item_id, quantity, total_price)
#
# Orders inventory items from the database.
# Reduces the coffee shop balance by the total price.
# Also ensures the coffee shop has enough balance 
# to complete the order. Adds the number of items
# to the inventory.
#
# Parameters:
#   item_id should be a string.
#   quantity should be an int.
#   total_price should be a float or int.
#
# Returns True if the inventory items 
#              were ordered successfully.
# Returns False if there was an error in the query.
##################################################
def order_inventory_items(manager_ssn, item_name, quantity, total_price):
    """
    Order inventory items from the database.
    """
    try:
        db = next(get_db())

        latest = db.query(Transactions).order_by(Transactions.trans_id.desc()).first()
        updated_balance = (latest.balance if latest else 0) - total_price
        if updated_balance < 0:
            raise QueryError("Insufficient balance to complete order")

        # Create transaction
        new_transaction = Transactions(
            type="refill",
            timestamp=func.now(),
            balance=updated_balance
        )
        db.add(new_transaction)
        db.flush()
        transaction_id = new_transaction.trans_id

        # Create refill
        new_refill = Refill(
            total_amt=total_price,
            placed_by=manager_ssn
        )
        db.add(new_refill)
        db.flush()
        refill_id = new_refill.refill_id

        # Link transaction and refill
        new_refill_update = RefillUpdate(
            trans_id=transaction_id,
            refill_id=refill_id
        )
        db.add(new_refill_update)

        # Update inventory quantity
        inventory_item = db.query(Inventory).filter(Inventory.name == item_name).first()
        if not inventory_item:
            raise QueryError(f"Inventory item '{item_name}' does not exist.")
        inventory_item.stock_quantity += quantity

        # Log restock
        new_restock = Restocks(
            inventory_name=item_name,
            refill_id=refill_id,
            refill_quant=quantity
        )
        db.add(new_restock)

        db.commit()
        return True

    except QueryError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise QueryError("Error ordering inventory items in query details=error " + str(e))

##################################################
# fetch_inventory_item(item_id)
#
# Fetches a single inventory item from the database.
#
# Parameters:
#   item_id should be a string.
#
# Returns the inventory item if found.
# Returns None if there was an error in the query.
##################################################

def fetch_inventory_item(item_id):
    """
    Fetch a single inventory item from the database.
    """
    try:
        db = next(get_db())
        # query = db.query(Inventory).filter(Inventory.name == item_id).first()
        return db.query(Inventory).filter(Inventory.name == item_id).first()
    except Exception as e:
        raise QueryError("Error fetching inventory item in query", details={"error": str(e)})

##################################################
# NOT USED IN CURRENT IMPLEMENTATION
##################################################
# add_inventory_item(item_name, unit, price, initial_stock=0)
#
# Adds a new inventory item to the database.
# Also checks if the item already exists in the database.
#
# Parameters:
#   item_name should be a string and cannot 
#       be empty or null.
#   unit should be a string and cannot be null.
#   price should be a float or int and must be 
#       greater than 0.
#   initial_stock should be a non-negative int 
#       and defaults to 0.
#
# Returns: True if the item was added successfully.
#          False if there was an error in the query.
##################################################
def add_inventory_item(item_name, unit, price, initial_stock=0):
    """
    Add a new inventory item to the database.
    """
    # Validate item_name
    if not item_name or not isinstance(item_name, str):
        raise QueryError("Invalid item name. Item name cannot be null or empty.")

    # Validate unit
    if not unit or not isinstance(unit, str):
        raise QueryError("Invalid unit. Unit cannot be null.")

    # Validate price
    if not isinstance(price, (int, float)) or price <= 0:
        raise QueryError("Invalid price. Price must be a number greater than 0.")

    # Validate initial_stock
    if not isinstance(initial_stock, int) or initial_stock < 0:
        raise QueryError("Invalid initial stock. Initial stock must be a non-negative integer.")

    try:
        db = next(get_db())

        # Check if the item already exists in the database
        existing_item = db.query(Inventory).filter(Inventory.name == item_name).first()
        if existing_item:
            raise QueryError(f"Inventory item '{item_name}' already exists in the database.\n" + 
                             "Database record for this item:\n" +
                             f"Name: {existing_item.name}, Unit: {existing_item.unit}, Price: {existing_item.price}, Stock Quantity: {existing_item.stock_quantity}")

        # Add the new inventory item
        new_item = Inventory(
            name=item_name,
            unit=unit,
            price=price,
            stock_quantity=initial_stock
        )
        db.add(new_item)

        # Commit the changes
        db.commit()
        return True
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error adding new inventory item in query", details={"error": str(e)})

##################################################
# NOT USED IN CURRENT IMPLEMENTATION
##################################################
# delete_inventory_item(item_name)
# Delete an inventory item from the database.
# 
# Parameters:
#    - item_name: The name of the inventory item 
#                 to delete.
# 
# Returns:
#    - True if the item was deleted successfully.
#    - False if there was an error in the query.
##################################################
def delete_inventory_item(item_name):
    """
    Delete an inventory item from the database.
    """
    # Validate item_name
    if not item_name or not isinstance(item_name, str):
        raise QueryError("Invalid item name. Item name cannot be null or empty.")

    try:
        db = next(get_db())

        # Check if the item exists in the database
        inventory_item = db.query(Inventory).filter(Inventory.name == item_name).first()
        if not inventory_item:
            raise QueryError(f"Inventory item '{item_name}' does not exist in the database.")

        # Check if the item is used in any recipes
        recipe_usage = db.query(RecipeIngredients).filter(RecipeIngredients.inventory_name == item_name).first()
        if recipe_usage:
            raise QueryError(f"Inventory item '{item_name}' is currently used in a recipe and cannot be deleted.")

        # Check if the stock quantity is 0
        if inventory_item.stock_quantity > 0:
            raise QueryError(f"Inventory item '{item_name}' still has stock remaining and cannot be deleted.")

        # Delete the inventory item
        db.delete(inventory_item)

        # Commit the changes
        db.commit()
        return True
    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error deleting inventory item in query", details={"error": str(e)})

##################################################
# ACCOUNTING REPORTS
##################################################

def sales_report(start_date, end_date, is_verbose=True):
    """
    Generate a sales report for a given date range.
    The report can be either detailed (verbose) 
    or simple.
    
    Parameters:
        - start_date: The start date of the report 
                      (format: YYYY-MM-DD).
        - end_date: The end date of the report 
                    (format: YYYY-MM-DD).
        - is_verbose: 
               - If True, returns a detailed list 
                 of transactions.
               - If False, returns the total revenue.
    
     Returns:
        - A list of transactions (verbose) or the 
          total revenue (simple).
        - An empty list (verbose) or 0 (simple) if 
          no transactions are found.
    """
    try:
        db = next(get_db())

        # Query transactions within the date range
        sales = db.query(Order).filter(
            Order.timestamp >= start_date,
            Order.timestamp <= end_date
        ).all()

        if not sales:
            return [] if is_verbose else 0

        if is_verbose:
            # Return a detailed list of transactions
            return [
                {
                    "id": sale.id,
                    "timestamp": sale.timestamp,
                    "total_amt": sale.total_amt,
                    "payment_method": sale.payment_method,
                    "prepared_by": sale.prepared_by
                }
                for sale in sales
            ]
        else:
            # Return the total revenue, number of sales
            total_revenue = sum(sale.total_amt for sale in sales)
            num_sales = len(sales)
            return f"Total Revenue: {total_revenue}, Number of Sales: {num_sales}"
    except Exception as e:
        raise QueryError("Error generating sales report in query", details={"error": str(e)})

##################################################
# Generate an report of restock orders for a given date range.
# The report can be either detailed (verbose)
# or simple.
#
# Parameters:
#    - start_date: The start date of the report
#                  (format: YYYY-MM-DD).
#    - end_date: The end date of the report
#                (format: YYYY-MM-DD).
#    - is_verbose:
#           - If True, returns a detailed list
#             of transactions.
#           - If False, returns the total amount
#             spent on restock orders at end 
#             of date range.
#
##################################################
def refill_report(start_date, end_date, is_verbose=True):
    """
    Generate a report of restock orders for a given date range.
    """
    try:
        db = next(get_db())

        # Query transactions within the date range
        refills = db.query(Refill).filter(
            Refill.timestamp >= start_date,
            Refill.timestamp <= end_date
        ).all()

        if not refills:
            return [] if is_verbose else 0

        if is_verbose:
            # Return a detailed list of transactions
            return [
                {
                    "id": refill.id,
                    "timestamp": refill.timestamp,
                    "total_amt": refill.total_amt,
                    "placed_by": refill.placed_by
                }
                for refill in refills
            ]
        else:
            # Return the summary
            total_expense = sum(refill.total_amt for refill in refills)
            num_refills = len(refills)
            return f"Total Expense: {total_expense}, Number of Refills: {num_refills}"
    except Exception as e:
        raise QueryError("Error generating refill report in query", details={"error": str(e)})

##################################################
# Generate a balance report for a given date range.
#
# Parameters:
#    - start_date: The start date of the report 
#                  (format: YYYY-MM-DD).
#    - end_date: The end date of the report 
#                (format: YYYY-MM-DD).
#    - is_verbose: 
#       - If True, returns a combined detailed 
#         list of sales and restocks.
#       - If False, returns the total balance at 
#         the end of the date range.
#
# Returns:
#    - A combined detailed list of sales and 
#      refills (verbose).
#    - The total balance at the end of the 
#      date range (simple).
#    - An empty list (verbose) or 0 (simple) 
#      if no data is found in the given date range.
##################################################

def balance_report(start_date, end_date, is_verbose=True):
    """
    Generate a balance report for a given date range.
    """
    try:
        db = next(get_db())

        if is_verbose:
            # Fetch sales report
            sales = db.query(
                Transactions.trans_id.label("trans_id"),
                Order.timestamp.label("timestamp"),
                Order.total_amt.label("total_amt"),
                Transactions.balance.label("balance")
            ).join(
                Transactions, 
                (Order.timestamp == Transactions.timestamp) & (Transactions.type == "order")
            ).filter(
                Order.timestamp >= start_date,
                Order.timestamp <= end_date
            ).all()

            # Fetch restocks report
            restocks = db.query(
                Transactions.trans_id.label("trans_id"),
                Refill.timestamp.label("timestamp"),
                Refill.total_amt.label("total_amt"),
                Transactions.balance.label("balance")
            ).join(
                Transactions, 
                (Refill.timestamp == Transactions.timestamp) & (Transactions.type == "refill")
            ).filter(
                Refill.timestamp >= start_date,
                Refill.timestamp <= end_date
            ).all()

            # Combine sales and restocks into a single detailed list
            combined_report = [
                { "type:": "sale",
                  "trans_id": sale.trans_id,
                  "timestamp": sale.timestamp,
                  "total_amt": sale.total_amt,
                  "balance": sale.balance }
                for sale in sales
            ] + [
                { "type:": "refill",
                  "trans_id": restock.trans_id,
                  "timestamp": restock.timestamp,
                  "total_amt": restock.total_amt,
                  "balance": restock.balance }
                for restock in restocks
            ]

            # Sort the combined report by timestamp in descending order
            combined_report.sort(key=lambda x: x["timestamp"], reverse=True)

            return combined_report
        else:
            # Fetch the total balance at the end of the date range
            # count of sales
            sales_count = db.query(Order).filter(
                Order.timestamp >= start_date,
                Order.timestamp <= end_date
            ).count()
            refill_count = db.query(Refill).filter(
                Refill.timestamp >= start_date,
                Refill.timestamp <= end_date
            ).count()
            balance = db.query(Transactions).filter(
                Transactions.timestamp <= end_date
            ).order_by(Transactions.timestamp.desc()).first()

            return f"Total Balance: {balance.balance}, Number of Sales: {sales_count}, Number of Refill Orders: {refill_count}"
    except Exception as e:
        raise QueryError("Error generating balance report in query", details={"error": str(e)})

##################################################
# Baristas sell drinks by creating a new order in the database.
#
# Parameters:
#   - barista_ssn: The SSN of the barista who prepared the order.
#   - payment_method: The payment method used for the order (e.g., "Cash", "Card").
#   - order_items: A list of dictionaries, where each dictionary contains:
#      - menu_item: The name of the menu item ordered.
#      - item_quant: The quantity of the menu item ordered.
#
# Returns:
#   - The order ID if successful.
#   - None if there was an error.
##################################################
def sell_drinks(barista_ssn, payment_method, order_items, total_price):
    """
    Sell drinks by creating a new order in the database.
    """
    try:
        db = next(get_db())

        for item in order_items:
            item_name = item.item_name if hasattr(item, 'item_name') else item['item_name']
            quantity = item.quantity if hasattr(item, 'quantity') else item['quantity']

            recipe = db.query(Recipe).filter(Recipe.recipe_name == item_name).first()
            if not recipe:
                raise QueryError(f"Recipe for '{item_name}' does not exist.")

            recipe_ingredients = db.query(RecipeIngredients).filter(
                RecipeIngredients.recipe_id == recipe.recipe_id
            ).all()

            for ingredient in recipe_ingredients:
                inventory_item = db.query(Inventory).filter(
                    Inventory.name == ingredient.inventory_name
                ).first()
                if not inventory_item:
                    raise QueryError(f"Inventory item '{ingredient.inventory_name}' does not exist.")

                required_quantity = ingredient.quantity * quantity
                if inventory_item.stock_quantity < required_quantity:
                    raise QueryError(
                        f"Not enough {ingredient.inventory_name} in stock to make {quantity} {item_name}. "
                        f"Required: {required_quantity}, Available: {inventory_item.stock_quantity}"
                    )

                inventory_item.stock_quantity -= required_quantity

        latest_tx = db.query(Transactions).order_by(Transactions.trans_id.desc()).first()
        updated_balance = (latest_tx.balance if latest_tx else 0) + Decimal(str(total_price))

        new_transaction = Transactions(
            type="order",
            timestamp=func.now(),
            balance=updated_balance
        )
        db.add(new_transaction)
        db.flush()
        transaction_id = new_transaction.trans_id

        new_order = Order(
            timestamp=func.now(),
            total_amt=total_price,
            payment_method=payment_method.lower(),
            prepared_by=barista_ssn
        )
        db.add(new_order)
        db.flush()
        order_id = new_order.order_id

        new_order_update = OrderUpdate(
            trans_id=transaction_id,
            order_id=order_id
        )
        db.add(new_order_update)

        for item in order_items:
            item_name = item.item_name if hasattr(item, 'item_name') else item['item_name']
            quantity = item.quantity if hasattr(item, 'quantity') else item['quantity']

            customer_order = CustomerOrder(
                order_id=order_id,
                menu_item=item_name,
                item_quant=quantity
            )
            db.add(customer_order)

        db.commit()
        return order_id

    except QueryError as e:
        raise e
    except Exception as e:
        raise QueryError("Error selling drinks in query details=error"+ str(e))

def fetch_menu_item(item_name):
    """
    Fetch a single menu item from the database.
    """
    try:
        db = next(get_db())
        # query = db.query(MenuItem).filter(MenuItem.name == item_name).first()
        return db.query(MenuItem).filter(MenuItem.name == item_name).first()
    except Exception as e:
        raise QueryError("Error fetching menu item in query", details={"error": str(e)})
    
# fetch baristas
# reduce inventory for each order
# fetch manager
# fetch customer orders
# create new customer order

# create all queries required by the application 