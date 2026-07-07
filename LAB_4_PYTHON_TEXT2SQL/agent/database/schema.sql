-- SQLite Database Schema for Retail Inventory Management
-- Created for LAB 6: Python Text-to-SQL Workshop

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS products;

-- Products Table
-- Stores product master data including pricing and supplier information
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_cost REAL NOT NULL,
    retail_price REAL NOT NULL,
    supplier_id TEXT NOT NULL,
    supplier_name TEXT NOT NULL,
    CHECK (unit_cost >= 0),
    CHECK (retail_price >= unit_cost)
);

-- Stores Table
-- Stores information about retail locations
CREATE TABLE stores (
    store_id TEXT PRIMARY KEY,
    store_name TEXT NOT NULL,
    location TEXT NOT NULL,
    manager_name TEXT NOT NULL
);

-- Inventory Table
-- Tracks current stock levels at each store
CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    current_stock INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 0,
    max_capacity INTEGER NOT NULL DEFAULT 0,
    last_updated DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    UNIQUE(product_id, store_id),
    CHECK (current_stock >= 0),
    CHECK (reorder_point >= 0),
    CHECK (max_capacity >= reorder_point)
);

-- Transactions Table
-- Records all inventory movements (sales, receipts, adjustments)
CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CHECK (transaction_type IN ('Sold', 'Received', 'Adjusted', 'Returned')),
    CHECK (quantity != 0)
);

-- Create indexes for better query performance
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_supplier ON products(supplier_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_inventory_store ON inventory(store_id);
CREATE INDEX idx_inventory_stock ON inventory(current_stock);
CREATE INDEX idx_transactions_product ON transactions(product_id);
CREATE INDEX idx_transactions_store ON transactions(store_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);

-- Create views for common queries

-- View: Low Stock Items
CREATE VIEW v_low_stock_items AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    i.store_id,
    s.store_name,
    i.current_stock,
    i.reorder_point,
    i.max_capacity,
    (i.reorder_point - i.current_stock) as units_to_order
FROM products p
JOIN inventory i ON p.product_id = i.product_id
JOIN stores s ON i.store_id = s.store_id
WHERE i.current_stock < i.reorder_point
ORDER BY (i.reorder_point - i.current_stock) DESC;

-- View: Product Sales Summary
CREATE VIEW v_product_sales AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.supplier_name,
    COUNT(DISTINCT t.transaction_id) as transaction_count,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity ELSE 0 END) as total_sold,
    SUM(CASE WHEN t.transaction_type = 'Returned' THEN t.quantity ELSE 0 END) as total_returned,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity * p.retail_price ELSE 0 END) as total_revenue,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity * (p.retail_price - p.unit_cost) ELSE 0 END) as total_profit
FROM products p
LEFT JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.product_id, p.product_name, p.category, p.supplier_name;

-- View: Store Inventory Value
CREATE VIEW v_store_inventory_value AS
SELECT 
    s.store_id,
    s.store_name,
    s.location,
    COUNT(DISTINCT i.product_id) as product_count,
    SUM(i.current_stock) as total_units,
    SUM(i.current_stock * p.unit_cost) as inventory_cost_value,
    SUM(i.current_stock * p.retail_price) as inventory_retail_value,
    SUM(i.current_stock * (p.retail_price - p.unit_cost)) as potential_profit
FROM stores s
LEFT JOIN inventory i ON s.store_id = i.store_id
LEFT JOIN products p ON i.product_id = p.product_id
GROUP BY s.store_id, s.store_name, s.location;

-- View: Category Performance
CREATE VIEW v_category_performance AS
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) as product_count,
    SUM(i.current_stock) as total_stock,
    AVG(p.retail_price - p.unit_cost) as avg_profit_margin,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity ELSE 0 END) as total_sold,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity * p.retail_price ELSE 0 END) as total_revenue
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Insert sample comment
-- This schema supports:
-- 1. Product master data management
-- 2. Multi-store inventory tracking
-- 3. Transaction history (sales, receipts, adjustments)
-- 4. Supplier information
-- 5. Performance analytics through views
-- 6. Natural language to SQL query conversion

-- Made with Bob