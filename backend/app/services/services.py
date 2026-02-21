# Combined service logic for all entities in services.py
from app.db.queries import (
    fetch_menu_items, fetch_baristas, fetch_managers, 
    add_manager, update_manager_ownership, delete_employee,
    add_employee, schedule_barista_shifts, change_employee_info,
    fetch_inventory, fetch_inventory_item, order_inventory_items,
    sales_report, refill_report, balance_report, sell_drinks,
    fetch_menu_item)
import re
from fastapi import HTTPException
from app.db.schemas.schemas import OrderItem
from datetime import time,datetime
# from app.db import dbclient

class ServiceError(Exception):
    """Custom exception for service errors."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

##################################################
# get_menu_items()
#
# Returns a list of all menu items from 
# the database.
##################################################
def get_menu_items():
    """
    Fetch menu items from the database.
    """
    try:
        menu_items = fetch_menu_items()
        print(f"Fetched menu items: ", menu_items)
        return menu_items
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# get_inventory()
#
# Returns a list of all inventory items from
# the database.
##################################################
def get_inventory():
    """
    Fetch inventory from the database.
    """
    try:
        inventory = fetch_inventory()
        return inventory
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
    
##################################################
# EMPLOYEE MANAGEMENT FUNCTIONS
##################################################

##################################################
# hire_employee(employee_data)
#
# Adds a new employee to the database.
# The employee data should be a dictionary
# containing the employee's information.
#
# Parameter:
#   - employee_data (dict): A dictionary containing 
#     the employee's information. Should include
#     'ssn', 'name', 'email', and 'salary'.
#   - isManager (bool): If True, the employee is a manager.
#       Default is False.
#       If True, the manager's ownership is updated.
#       to be equal among all managers.
#     NOT IMPLEMENTED IN CURRENT VERSION.
##################################################
def hire_employee(employee_data, isManager=False):
    """
    Add a new employee to the database.
    """
    try:
        print(f"Adding employee: {employee_data}")
        # validate employee_data
        required_keys = ['ssn', 'name', 'email', 'salary',
                        'days_working', 'start_time', 'end_time']
        
        for key in required_keys:
            if key not in employee_data:
                raise ServiceError(f"Missing required key: {key}")

        # validate ssn format
        if not isinstance(employee_data['ssn'], str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', employee_data['ssn']):
            raise ServiceError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        # validate name format
        if not isinstance(employee_data['name'], str) or not re.match(r'^[a-zA-Z\s]+$', employee_data['name']):
            raise ServiceError("Invalid name format. Name should only contain letters and spaces")

        # validate email format
        if not isinstance(employee_data['email'], str) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', employee_data['email']):
            raise ServiceError("Invalid email format")

        #validate salary format
        if not isinstance(employee_data['salary'], (int, float)) or employee_data['salary'] < 0:
            raise ServiceError("Invalid salary format. Salary must be a positive number")

        # validate days_working format
        if not isinstance(employee_data['days_working'], list):
            raise ServiceError("Invalid days_working format. Expected a list of strings")

        for day in employee_data['days_working']:
            if not isinstance(day, str) or day not in(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
                raise ServiceError(f"Invalid day format: {day}.")
            
        # validate start_time and end_time format
        # time_format = r'^([01][0-9]|2[0-3]):[0-5][0-9]$'  # 24-hour format: HH:MM

        if not isinstance(employee_data['start_time'], time): # or not re.match(time_format, employee_data['start_time']):
            raise ServiceError("Invalid start_time format. Expected format: HH:MM (24-hour format)")
        if not isinstance(employee_data['end_time'], time): # or not re.match(time_format, employee_data['end_time']):
            raise ServiceError("Invalid end_time format. Expected format: HH:MM (24-hour format)")

        # validate isManager format
        if not isinstance(isManager, bool):
            raise ServiceError("Invalid isManager format. isManager must be a boolean value")

        add_emplpyee_result = add_employee(employee_data)
        result = f"Added employee {employee_data['name']}: {add_emplpyee_result}"
        if isManager:
            new_manager = add_manager(employee_data['ssn'])
            result += f"\nAdded manager {employee_data['name']}: {new_manager}"

            managers = fetch_managers()
            ownership = 100 / len(managers) if managers else 0
            update_manager_ownership(ownership)
            result += f"\nUpdated manager ownership to {ownership}% for all managers."

        return result
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# get_baristas()
#
# Returns a list of all baristas from
# the database.
##################################################
def get_baristas():
    """
    Fetch baristas from the database.
    """
    try:
        baristas = fetch_baristas()
        return baristas
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# get_managers()
#
# Returns a list of all managers from
# the database.
##################################################
def get_managers():
    """
    Fetch managers from the database.
    """
    try:
        managers = fetch_managers()
        return managers
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

###################################################
# fire_employee(ssn)
#
# Fires an employee by SSN.
# If the employee is a manager, updates the
# ownership of all managers to be equal.
###################################################
def fire_employee(ssn):
    """
    Fire an employee by SSN.
    """
    try:
        
        # validate ssn format
        if not isinstance(ssn, str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
            raise ServiceError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        managers = fetch_managers()
        print(f"Fetched managers: ", managers)
        try:
            isManager = any(manager[1] == ssn for manager in managers)
        except Exception as e:
            print(f"Error checking if employee is a manager: {e}")
        # db = next(dbclient.get_db())
        result = delete_employee(ssn)

        if isManager:
            managers = fetch_managers()
            ownership = 100 / len(managers) if managers else 0
            update_manager_ownership(ownership)

        return result
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: !!!!!!!!!!!!" + str(e))

##################################################
# NOT UTILIZED IN CURRENT VERSION
##################################################
# update_schedule(ssn, start_time, end_time, days_working)
#
# Update the schedule of an employee by SSN.
#
# Parameters:
#   - ssn (str): The SSN of the employee.
#   - start_time (str): The start time of the shift.
#       Expected format: HH:MM AM/PM.
#   - end_time (str): The end time of the shift.
#       Expected format: HH:MM AM/PM.
#   - days_working (list): A list of days the employee
#       is working.
#
# Returns:
#   - True if the schedule was updated successfully
#   - False if not updated
#   - None if error occurred
##################################################
def update_schedule(ssn, start_time=None, end_time=None, days_working=None):
    """
    Update the schedule of an employee by SSN.
    """
    try:
        # validate ssn format
        if not isinstance(ssn, str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
            raise ServiceError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        # validate start_time and end_time format
        time_format = r'^([01][0-9]|2[0-3]):[0-5][0-9]$'  # 24-hour format: HH:MM
        if not isinstance('start_time', str) or not re.match(time_format, 'start_time'):
            raise ServiceError("Invalid start_time format. Expected format: HH:MM (24-hour format)")
        if not isinstance('end_time', str) or not re.match(time_format, 'end_time'):
            raise ServiceError("Invalid end_time format. Expected format: HH:MM (24-hour format)")
        # validate days_working format
        if days_working and not isinstance(days_working, list):
            raise ServiceError("Invalid days_working format. Expected a list of strings")

        for day in days_working:
            if not isinstance(day, str) or day not in(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
                raise ServiceError(f"Invalid day format: {day}.")

        result = schedule_barista_shifts(ssn, start_time, end_time, days_working)
        return f"Updated schedule for employee with SSN {ssn}: {result}"
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# update_info(ssn, name=None, email=None, salary=None)
#
# Update the information of an employee by SSN.
#
# Parameters:
#   - ssn (str): The SSN of the employee.
#   - name (str): The name of the employee.
#   - email (str): The email of the employee.
#   - salary (float): The salary of the employee.
#
# Returns:
#   - True if the information was updated successfully
#   - False if not updated
#   - None if error occurred
##################################################
def update_employee_info(employee_data):
    """
    Update the information of an employee by SSN.
    """
    try:
        # break employee_data into ssn, name, email, and salary
        ssn = employee_data['ssn']
        name = employee_data.get('name')
        email = employee_data.get('email')
        salary = employee_data.get('salary')

        # validate ssn format
        if not isinstance(ssn, str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
            raise ServiceError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        # validate name format
        if name and (not isinstance(name, str) or not re.match(r'^[a-zA-Z\s]+$', name)):
            raise ServiceError("Invalid name format. Name should only contain letters and spaces")

        # validate email format
        if email and (not isinstance(email, str) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)):
            raise ServiceError("Invalid email format")

        # validate salary format
        if salary and (not isinstance(salary, (int, float)) or salary < 0):
            raise ServiceError("Invalid salary format. Salary must be a positive number")

        result = change_employee_info(ssn, name, email, salary)
        return f"Updated info for employee with SSN {ssn}: {result}"
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# INVENTORY MANAGEMENT FUNCTIONS
##################################################

##################################################
# refill(manager_ssn, items)
#
# Refill an inventory item.
#
# Parameters:
#   - manager_ssn (str): The SSN of the manager.
#   - items (list): A list of dictionaries containing
#     the item ID and quantity to refill.
#     Example: [{'item_id': 'item1', 'quantity': 10}, {'item_id': 'item2', 'quantity': 5}]
#
# Returns:
#   - True if the refill was successful
#   - False if not successful
#   - None if error occurred
##################################################
def refill(refill_data):
    """
    Refill an inventory item.
    """
    print(f"Refilling inventory: {refill_data}")
    try:
        # break refill_data into manager_ssn, item_name, and quantity
        manager_ssn = refill_data['manager_ssn']
        item_name = refill_data['item_name']
        quantity = refill_data['quantity']

        # validate manager_ssn format
        if not isinstance(manager_ssn, str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', manager_ssn):
            raise ServiceError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        # validate items format

        if not isinstance(item_name, str):
            raise ServiceError("Invalid item_id format. Expected a string.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ServiceError("Invalid quantity format. Expected a positive integer")

        # Fetch the price of the item from the database
        item_data = fetch_inventory_item(item_name)
        if not item_data:
            raise ServiceError(f"{item_name} not found in inventory")

        price = item_data.price

        total_price = price * quantity

        result = order_inventory_items(manager_ssn, item_name, quantity, total_price)
        return f"Restocked {quantity} of {item_name} by manager with SSN {manager_ssn}: {result}"
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# get_inventory_item(item_id)
#
# Returns an inventory item by ID.
#
# Parameters:
#   - item_id (str): The ID of the inventory item.
#     Example: 'item1'
#
# Returns:
#   - The inventory item if found
#   - None if not found
#   - None if error occurred
##################################################
def get_inventory_item(item_id):
    """
    Fetch an inventory item by ID.
    """
    try:
        # validate item_id format
        if not isinstance(item_id, str):
            raise ServiceError("Invalid item_id format. Expected a positive integer")

        item = fetch_inventory_item(item_id)

        return item
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
# ACCOUNTING RECORD FUNCTIONS
##################################################

##################################################
# sales_report(start_date, end_date, isVerbose=True)
#
# Generates a sales report for a given date range.
# The report includes the total sales amount and
# the number of items sold.
#
# Parameters:
#   - start_date (str): The start date of the report.
#       Expected format: YYYY-MM-DD.
#   - end_date (str): The end date of the report.
#       Expected format: YYYY-MM-DD.
#   - isVerbose (bool): If True, prints the full report.
#       If False, prints a simple report.
#       Default is True.
#
# Returns:
#   - if isVerbose is True:
#       A dictionary containing the total sales amount,
#       the number of items sold, and a list of sales records.
#   - if isVerbose is False:
#       A string which contains the total sales amount and
#       the number of items sold.
#   - None if error occurred
##################################################
def run_sales_report(report_params):
    """
    Generate a sales report for a given date range.
    """
    try:
        start_date = report_params.get('start_date')
        end_date = report_params.get('end_date')
        is_verbose = report_params.get('isVerbose')

        # Validate date formats
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date):
            raise ServiceError("Invalid start_date format. Expected format: YYYY-MM-DD.")
        if not re.match(date_pattern, end_date):
            raise ServiceError("Invalid end_date format. Expected format: YYYY-MM-DD.")

        # Validate date range
        if start_date > end_date:
            raise ServiceError("start_date must be less than or equal to end_date.")

        # Validate isVerbose format
        if not isinstance(is_verbose, bool):
            raise ServiceError("Invalid isVerbose format. isVerbose must be a boolean value")

        report = sales_report(start_date, end_date, is_verbose)

        print(f"Generated sales report from {start_date} to {end_date}: ", report)
        return report
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

###################################################
# refill_report(start_date, end_date, isVerbose=True)
#
# Generates a refills report for a given date range.
# The report includes the total refills amount and
# the number of items refilled.
#
# Parameters:
#   - start_date (str): The start date of the report.
#       Expected format: YYYY-MM-DD.
#   - end_date (str): The end date of the report.
#       Expected format: YYYY-MM-DD.
#   - isVerbose (bool): If True, prints the full report.
#       If False, prints a simple report.
#       Default is True.
#
# Returns:
#   - if isVerbose is True:
#       A dictionary containing the total refills amount,
#       the number of items refilled, and a list of refills records.
#   - if isVerbose is False:
#       A string which contains the total expenses and
#       the number of refill orders placed.
#   - None if error occurred
def get_refill_reports(report_params):
    """
    Generate a refills report for a given date range.
    """
    try:
        # break report_params into start_date, end_date, and isVerbose
        start_date = report_params['start_date']
        end_date = report_params['end_date']
        isVerbose = report_params['isVerbose']

        # Validate date formats
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date):
            raise ServiceError("Invalid start_date format. Expected format: YYYY-MM-DD.")
        if not re.match(date_pattern, end_date):
            raise ServiceError("Invalid end_date format. Expected format: YYYY-MM-DD.")

        # Validate date range
        if start_date > end_date:
            raise ServiceError("start_date must be less than or equal to end_date.")

        # Validate isVerbose format
        if not isinstance(isVerbose, bool):
            raise ServiceError("Invalid isVerbose format. isVerbose must be a boolean value")

        report = refill_report(start_date, end_date, isVerbose)
        print(f"Generated refills report from {start_date} to {end_date}: ", report)
        return report
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

####################################################
# balance_report(start_date, end_date, isVerbose=True)
#
# Generates a balance report for a given date range.
# The report includes the total balance amount and
# both the number of items sold and the number of
# refill orders placed.
#
# Parameters:
#   - start_date (str): The start date of the report.
#       Expected format: YYYY-MM-DD.
#   - end_date (str): The end date of the report.
#       Expected format: YYYY-MM-DD.
#   - isVerbose (bool): If True, prints the full report.
#       If False, prints a simple report.
#       Default is True.
#
# Returns:
#   - if isVerbose is True:
#       A dictionary containing the total balance
#       amount, the number of items sold, the number 
#       of refill orders placed, and a list of sales 
#       and refills records.
#   - if isVerbose is False:
#       A string which contains the total balance 
#       amount, the number of items sold, and the 
#       number of refill orders placed.
#   - None if error occurred
####################################################
def get_balance_report(report_params):
    """
    Generate a balance report for a given date range.
    """
    try:
        # break report_params into start_date, end_date, and isVerbose
        start_date = report_params['start_date']
        end_date = report_params['end_date']
        isVerbose = report_params['isVerbose']
        
        # Validate date formats
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date):
            raise ServiceError("Invalid start_date format. Expected format: YYYY-MM-DD.")
        if not re.match(date_pattern, end_date):
            raise ServiceError("Invalid end_date format. Expected format: YYYY-MM-DD.")

        # Validate date range
        if start_date > end_date:
            raise ServiceError("start_date must be less than or equal to end_date.")

        # Validate isVerbose format
        if not isinstance(isVerbose, bool):
            raise ServiceError("Invalid isVerbose format. isVerbose must be a boolean value")

        report = balance_report(start_date, end_date, isVerbose)
        print(f"Generated balance report from {start_date} to {end_date}: ", report)
        return report
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

##################################################
def place_customer_orders(order_data):
    """
    Place customer orders.
    """
    try:
        # break order_data into barista_ssn, payment_method, and order_data
        barista_ssn = order_data['barista_ssn']
        payment_method = order_data['payment_method']
        order_info = order_data['order_info']

        # validate barista_ssn format
        if not isinstance(barista_ssn, str) or not re.match(r'^\d{3}-\d{2}-\d{4}$', barista_ssn):
            raise ServiceError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        # validate payment_method format
        if payment_method not in ["Cash", "Credit_card", "Debit_card"]:
            raise ServiceError("Invalid payment_method format. Expected 'Cash' or 'Card'")

        # print(f"Placing customer orders: {order_info}")
        # print(f"order_info type: {type(item_info)}")
        # validate order_data format
        if not isinstance(order_info, list) or not all(
            isinstance(item_info, dict) and 
                'item_name' in item_info and 
                'quantity' in item_info
            for item_info in order_info
        ):
            raise ServiceError("Invalid order_data format. Expected a list of item IDs and quantities.")

        for item_info in order_info:
            item_name = item_info.get('item_name')
            quantity = item_info.get('quantity')

            if not isinstance(item_name, str):
                raise ServiceError("Invalid item_name format. Expected a string.")
            if not isinstance(quantity, int) or quantity <= 0:
                raise ServiceError("Invalid quantity format. Expected a positive integer.")
            
        total_price = 0
        for item in order_info:
            menu_item = item['item_name']
            quantity = item['quantity']
            
            # Fetch the price of the item from the database
            item_data = fetch_menu_item(menu_item)
            if not item_data:
                raise ServiceError(f"{menu_item} not found in menu")
            
            price = item_data.price
            total_price += price * quantity

        result = sell_drinks(barista_ssn, payment_method, order_info, total_price)
        print(f"Placed customer orders by barista with SSN {barista_ssn}: ", result)
        return result
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
