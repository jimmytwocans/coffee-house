# CHANGE LOG
### __Sat Apr 26, 2025__
0925:
- CHANGELOG.md init
- Added to `cs480-s25-group-09/backend/app/db/models/models.py`:
   - Additional `import`s: `ForeignKey`,`CheckConstraint`, `PrimaryKeyConstraint`
   - Translated `customer_order` table in `schema.sql` to SQLAlchemy model

0955:
- `models.py`:
   - Organized `from sqlachemy import` list
   - Added `import`s: `Numeric`, `Time`
   - Translated tables from `schema.sql` to SQLAlchemy model:
      - `employee`
      - `manager`
      - `barista`
      - `day`

1130:
- `models.py`:
    - Reorganized model `Class`es to match order they're declared in `schema.sql`
    - Additional imports to `from sqlalchemy import`:
       - `TIMESTAMP`
    - Added `from sqlalchemy.sql import func`
    - Translated tables from `schema.sql` to SQLAlchemy model:
       - `promotion`
       - `promo_window`
       - `promoted_menu_items`
       - `recipe`
       - `recipe_steps`
       - `inventory`
       - `recipe_ingredients`
       - `refill`
       - `restocks`

1210:
- `models.py`:
   - Translated tables from `schema.sql` to SQLAlchemy model:
      - `transactions`
      - `order_update`
      - `refill_update`

1645:
- `cs480-s25-group-09/backend/app/db/queries.py`
   - Added list of methods needed for manager
   - Added methods
      - `add_employee(employee_data)`
      - `add_manager(ownership)`

1800:
- Edit to `schema.sql`:
   - Added attribute `transactions.balance`
   - Updated `models.py`
- Edits to `queries.py`:
   - Documentation for existing methods
   - Import from `models`: `Employee`, `Barista`, `Manager`, `Day`, `Inventory`, `Transtions`
   - Added methods:
      - `delete_employee(ssn)`
      - `schedule_barista_shifts(ssn, start_time, end_time, days)`
      - `change_employee_info(ssn, name, email, salary)`
      - `order_inventory_items(item_id, quantity, total_price)`

### __Sat May 3, 2025__
1015:
- Edits to `schema.sql`:
   - `inventory.name`: `ON DELETE CASCADE`
      - Removed - thinking: this would remove records from `recipe_incredients` and `restocks` - an inventory item should not be deleted from the database if it is in a recipe, and transactions should never be deleted.
- Edits to `cs480-s25-group-09/backend/app/db/queries.py`:
   - Import from `cs480-s25-group-09/backend/app/db/models/models.py`:
      - `RecipeIngredients`
   - Added methods:
      - `add_inventory_item(item_name, unit, price, initial_stock=0)`
      - `delete_inventory_item(item_name)`

1230:
- Edits to `queries.py`:
   - Import from `models.py`:
      - `Order`
      - `Refill`
   - Added methods:
      - `sales_report(start_date, end_date, isVerbose=True)`
      - `restocks_report(start_date, end_date, isVerbose=True)`
      - `balance_report(start_date, end_date, isVerbose=True)`

1340:
- `queries.py`:
   - Sorted imports, making them more readable
   - Added `sell_drinks(barista_ssn, payment_method, order_items)`

1510:
- Migrated logic from `queries.py` to `services.py` - the only thing `queries.py` should be doing is interacting with the database.
   -  `queries.add_employee()` > `services.hire_employee()`
      - Moved data validation over
      - `hire_employee()` takes an `isManager` parameter - if true, will update `manager` table
- Added documentation to `services.py`
   - `get_menu_items`
   - `hire_employee(employee_data, isManager=False)`
   - `get_baristas()`
   - `get_managers()`
   - `fire_employee(ssn)`
- Updated `add_employee` and `hire_employee`
   - `employee_data` includes starting schedule

1645:
- Migrate from `queries.py` to `services.py`:
   - `delete_employee` > `fire_employee`:
      - `ssn` validation
      - updating `manager.ownership`
   - `scheduule_barista_shifts` > `update_schedule`:
      - data validation: `ssn`, `start_time`, `end_time`, `days_working`
   - `change_employee_info` > `update_employee_info`:
      - data validation: `ssn`, `name`, `email`, `salary`
- `endpoints.py`:
   - `get.("/inventory")`
   - `post.("/baristas")`
   - `post("/refill")` - not functional

1845:
- Added functionality for:
   - `post("/refill")`
   - `services.refill(manager_ssn, items)`
   - `queries.order_inventory_items(manager_ssn, items, total_price)`
- Accounting reports, from `queries.py` to `services.py`
   - `sales_report` > `get_sales_report`
   - `refill_report` > `get_refill_report`