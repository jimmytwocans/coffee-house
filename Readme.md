# ☕ CoffeeHouse - Database Design

**CoffeeHouse** is a database system designed to manage the operations of a coffee shop, including order handling, promotions, inventory management, employee scheduling, and financial tracking. The schema is structured to support scalability, auditability, and promotional flexibility while ensuring normalized data design.

---

## 🧱 Core Entities and Relationships

### 🧾 `MenuItem`
Represents drinks available on the menu.

- Attributes: `name`, `type`, `size`, `price`, `hot_or_cold`
- Each `MenuItem` has **one recipe** and may be part of **promotions**.
- Linked to orders via the `customer-place-order` relationship.

---

### 🍽️ `Recipe` and `Recipe_Steps`
Defines the preparation method for each drink.

- One-to-one relationship with `MenuItem` via `as_recipe`.
- Each recipe has multiple ordered steps stored in `recipe_steps`.

---

### 🧂 `Inventory`
Tracks all ingredients (stock items).

- Attributes: `name`, `unit`, `price`, `stock_quantity`
- Connected to recipes via `recipe_ingredients`.
- Updated through the `restocks` relationship via `Refill`.

---

### 🔁 `Refill`
Represents stock refill actions.

- Connected to `Inventory` and `Transactions`.
- Captures the quantity restocked and cost via `refill_quant`.
- Logged financially in `Transactions` through `refill-update`.

---

### 💳 `Transaction`
Central financial log of the shop.

- Attributes: `trans_id`, `timestamp`, `amount`, `balance` (derived)
- Connected to both `Order` and `Refill` via `order-update` and `refill-update`.
- Ensures traceable financial history.

---

### 🧑‍🍳 `Barista` (subtype of `Employee`)
Staff member responsible for preparing drinks.

- Inherits: `name`, `ssn`, `email`, `salary` from `Employee`
- Assigned shifts (day, start_time, end_time)
- Connected to `Order` via `prepared_by`.

---

### 🛒 `Order`
Represents customer purchases.

- Attributes: `order_id`, `timestamp`, `payment_method`, `total_amt`
- Linked to multiple `MenuItems` with quantities via `item_quant`.
- Connected to a single `Barista` and `Transaction`.

---

### 📣 `Promotion`
Time-based or combo discounts for drinks.

- Attributes: `promo_id`, `description`, `start_time`, `end_time`, `day`, `discount%`
- Connected to `MenuItems` via `promotedMenuItem`.

---

## 💡 Highlights

- Orders deduct inventory automatically based on recipe ingredients.
- Promotions are time-bound and item-specific, affecting order totals.
- Every financial action (sale or refill) is logged in the `Transactions` table.
- Shift assignments are tracked for baristas to ensure operational transparency.
- Managers can place refil request and alters inventory(stock) and logged to transaction through refil-update.

---