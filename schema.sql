
-- init.sql: Coffee House Management DB
-- Run this in psql or any PostgreSQL GUI tool

-- Drop if exists (optional for fresh start)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Optional: Force UTF-8
SET client_encoding = 'UTF8';

-- Table: employee
CREATE TABLE employee (
    ssn CHAR(11) PRIMARY KEY NOT NULL UNIQUE CHECK (ssn ~'^\d{3}-\d{2}-\d{4}$'),
    name VARCHAR(100) NOT NULL ,
    email VARCHAR(100) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    salary NUMERIC(8, 2)
);

-- Table: manager (inherits employee)
CREATE TABLE manager (
    ssn CHAR(11) PRIMARY KEY REFERENCES employee(ssn) ON DELETE CASCADE,
    ownership NUMERIC(5, 2) CHECK (ownership >= 0 AND ownership <= 100)
);

-- Table: barista (inherits employee)
CREATE TABLE barista (
    ssn CHAR(11) PRIMARY KEY REFERENCES employee(ssn) ON DELETE CASCADE,
    start_time TIME,
    end_time TIME
);

-- Table: shifts
CREATE TABLE day (
    barista_ssn CHAR(11) REFERENCES barista(ssn),
    day VARCHAR(10),
    PRIMARY KEY (barista_ssn, day)
);

-- Table: order
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amt NUMERIC CHECK (total_amt >= 0),
    payment_method VARCHAR(15) CHECK (payment_method IN ('cash', 'credit_card', 'debit_card')),
    prepared_by CHAR(11) REFERENCES barista(ssn)
);

-- Table: menuItem
CREATE TABLE menuItem (
    name VARCHAR(100) PRIMARY KEY,
    type VARCHAR(50),
    size VARCHAR(10),
    price NUMERIC CHECK (price >= 0),
    hot_or_cold VARCHAR(10) CHECK (hot_or_cold IN ('hot', 'cold'))
);

-- Table: customer_orders (links order to menuItems)
CREATE TABLE customer_orders (
    order_id INT REFERENCES orders(order_id),
    menu_item VARCHAR(50) REFERENCES menuItem(name),
    item_quant INT NOT NULL CHECK (item_quant > 0),
    PRIMARY KEY (order_id, menu_item)
);

-- Table: promotion
CREATE TABLE promotion (
    promo_id SERIAL PRIMARY KEY,
    discount NUMERIC(4,2) CHECK (discount >= 0 AND discount <= 100),
    day VARCHAR(10),
    start_time TIME,
    end_time TIME,
    description TEXT
);

-- Table: promo_window
/* CREATE TABLE promo_window (
    promo_id INT PRIMARY KEY REFERENCES promotion(promo_id),
    start_time TIME,
    end_time TIME,
    day VARCHAR(10)
);
 */
-- Table: promoted_menu_items
CREATE TABLE promoted_menu_items (
    promo_id INT REFERENCES promotion(promo_id),
    name TEXT REFERENCES menuItem(name),
    PRIMARY KEY (promo_id, name)
);

-- Table: Recipe
CREATE TABLE recipe (
    recipe_id SERIAL PRIMARY KEY,
    recipe_name TEXT REFERENCES menuItem(name),
    -- recipe_name VARCHAR(100),
    description TEXT
);

-- Table: recipe_steps
CREATE TABLE recipe_steps (
    recipe_id SERIAL REFERENCES recipe(recipe_id),
    step_name TEXT,
    procedure TEXT,
    position INT,
    PRIMARY KEY (recipe_id, position)
);

-- Table: inventory
CREATE TABLE inventory (
    name TEXT PRIMARY KEY,
    unit VARCHAR(20),
    price NUMERIC(6, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INT NOT NULL
);

-- Table: recipe_ingredients
CREATE TABLE recipe_ingredients (
    inventory_name TEXT REFERENCES inventory(name),
    recipe_id INT REFERENCES recipe(recipe_id),
    quantity NUMERIC CHECK (quantity >= 0), --extra.
    PRIMARY KEY (recipe_id, inventory_name)
);

-- Table: reffil 
CREATE TABLE refill (
    refill_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amt NUMERIC(7, 2),
    placed_by VARCHAR(11) REFERENCES manager(ssn)
);    

-- Table: restocks (inventory updated through refills)
CREATE TABLE restocks (
    inventory_name VARCHAR(100) REFERENCES inventory(name),
    refill_id INT REFERENCES refill(refill_id),
    refill_quant INT,
    PRIMARY KEY (inventory_name, refill_id)
);

-- Table: transactions
CREATE TABLE transactions (
    trans_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(20) CHECK (type IN ('order', 'refill')),
    balance NUMERIC(7, 2) DEFAULT 10000.00
);

--Table: order_updates (to link transactions to orders)
CREATE TABLE order_update (
    trans_id INT PRIMARY KEY REFERENCES transactions(trans_id),
    order_id INT REFERENCES orders(order_id)
);

-- Table: refil_updates (to link transactions to refils)
CREATE TABLE refil_update (
    trans_id INT PRIMARY KEY REFERENCES transactions(trans_id),
    refill_id INT REFERENCES refill(refill_id)
);

-- ✅ SAMPLE DATA INSERTS BELOW ---

-- 1. Employees
INSERT INTO employee (ssn, name, email, salary) VALUES
('123-45-6789', 'Alice Manager', 'alice@coffee.com', 75000.00),
('987-65-4321', 'Bob Barista', 'bob@coffee.com', 45000.00),
('111-22-3333', 'Charlie Barista', 'charlie@coffee.com', 43000.00),
('444-55-6666', 'Daisy Manager', 'daisy@coffee.com', 78000.00),
('777-88-9999', 'Eve Barista', 'eve@coffee.com', 42000.00);

-- 2. Managers
INSERT INTO manager (ssn, ownership) VALUES
('123-45-6789', 60.00),
('444-55-6666', 40.00);

-- 3. Baristas
INSERT INTO barista (ssn, start_time, end_time) VALUES
('987-65-4321', '08:00', '14:00'),
('111-22-3333', '14:00', '20:00'),
('777-88-9999', '10:00', '16:00');

-- 4. Shifts
INSERT INTO day (barista_ssn, day) VALUES
('987-65-4321', 'Monday'),
('111-22-3333', 'Tuesday'),
('777-88-9999', 'Wednesday'),
('987-65-4321', 'Thursday'),
('111-22-3333', 'Friday');

-- 5. Menu Items
INSERT INTO menuItem (name, type, size, price, hot_or_cold) VALUES
('Espresso', 'coffee', 'small', 3.00, 'hot'),
('Latte', 'coffee', 'medium', 4.50, 'hot'),
('Iced Tea', 'tea', 'large', 3.50, 'cold'),
('Mocha', 'coffee', 'large', 5.00, 'hot'),
('Smoothie', 'fruit', 'medium', 4.00, 'cold'),
('Crossiant', 'snack', 'small', 3.00, 'hot'),
('donut','snack','small',2.59,'cold');

-- 6. Orders
INSERT INTO orders (total_amt, payment_method, prepared_by) VALUES
(10.00, 'cash', '987-65-4321'),
(9.50, 'credit_card', '111-22-3333'),
(8.00, 'debit_card', '777-88-9999'),
(13.00, 'cash', '987-65-4321'),
(7.50, 'credit_card', '111-22-3333');

-- 7. Customer Orders
INSERT INTO customer_orders (order_id, menu_item, item_quant) VALUES
(1, 'Espresso', 2),
(1, 'Latte', 1),
(2, 'Iced Tea', 2),
(3, 'Mocha', 1),
(4, 'Smoothie', 2),
(5, 'Espresso', 1);

-- 8. Promotions
INSERT INTO promotion (discount, day, start_time, end_time, description) VALUES
(10.00, 'Monday', '08:00', '10:00', '10% off all coffee'),
(15.00, 'Wednesday', '14:00', '16:00', 'Midweek Mocha deal'),
(5.00, 'Friday', '10:00', '12:00', 'Smoothie special'),
(20.00, 'Sunday', '09:00', '11:00', 'Family day 20% off'),
(12.50, 'Saturday', '15:00', '18:00', 'Weekend Latte Rush');

/* -- 9. Promo Windows
INSERT INTO promo_window (promo_id, start_time, end_time, day) VALUES
(1, '08:00', '10:00', 'Monday'),
(2, '14:00', '16:00', 'Wednesday'),
(3, '10:00', '12:00', 'Friday'),
(4, '09:00', '11:00', 'Sunday'),
(5, '15:00', '18:00', 'Saturday');
 */
-- 10. Promoted Menu Items
INSERT INTO promoted_menu_items (promo_id, name) VALUES
(1, 'Espresso'),
(2, 'Mocha'),
(3, 'Smoothie'),
(4, 'Latte'),
(5, 'Latte');

-- 11. Recipes
INSERT INTO recipe (recipe_name, description) VALUES
('Espresso', 'Strong black coffee'),
('Latte', 'Espresso with steamed milk'),
('Mocha', 'Espresso with chocolate syrup and milk'),
('Iced Tea', 'Brewed tea served cold'),
('Smoothie', 'Blended fruit and yogurt');

-- 12. Recipe Steps
INSERT INTO recipe_steps (recipe_id, step_name, procedure, position) VALUES
(1, 'Brew', 'Brew coffee beans at 90°C', 1),
(2, 'Steam Milk', 'Steam milk to 65°C', 1),
(2, 'Mix', 'Add steamed milk to espresso', 2),
(3, 'Add Chocolate', 'Add syrup to cup', 1),
(3, 'Mix', 'Mix espresso, chocolate, milk', 2);

-- 13. Inventory
INSERT INTO inventory (name, unit, price, stock_quantity) VALUES
('coffee_beans', 'grams', 0.10, 5000),
('milk', 'ml', 0.05, 10000),
('chocolate_syrup', 'ml', 0.15, 3000),
('tea_leaves', 'grams', 0.08, 2000),
('fruit_mix', 'grams', 0.12, 4000);

-- 14. Recipe Ingredients
INSERT INTO recipe_ingredients (inventory_name, recipe_id, quantity) VALUES
('coffee_beans', 1, 20),
('coffee_beans', 2, 15),
('milk', 2, 200),
('coffee_beans', 3, 15),
('chocolate_syrup', 3, 30),
('milk', 3, 150),
('tea_leaves', 4, 10),
('fruit_mix', 5, 100),
('milk', 5, 50);

-- 15. Refills
INSERT INTO refill (total_amt, placed_by) VALUES
(50.00, '123-45-6789'),
(75.00, '444-55-6666'),
(60.00, '123-45-6789'),
(45.00, '444-55-6666'),
(90.00, '123-45-6789');

-- 16. Restocks
INSERT INTO restocks (inventory_name, refill_id, refill_quant) VALUES
('coffee_beans', 1, 1000),
('milk', 2, 2000),
('chocolate_syrup', 3, 1000),
('tea_leaves', 4, 500),
('fruit_mix', 5, 1500);

-- 17. Transactions
INSERT INTO transactions (type) VALUES
('order'), ('order'), ('refill'), ('refill'), ('order');

-- 18. Order Update
INSERT INTO order_update (trans_id, order_id) VALUES
(1, 1),
(2, 2),
(5, 5);

-- 19. Refill Update
INSERT INTO refil_update (trans_id, refill_id) VALUES
(3, 1),
(4, 2);


