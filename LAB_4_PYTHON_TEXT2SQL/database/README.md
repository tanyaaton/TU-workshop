# SQLite Database for Retail Inventory Management

This directory contains the SQLite database and related files for LAB 6.

## 📁 Files

- **`schema.sql`** - Database schema definition with tables, indexes, and views
- **`create_database.py`** - Python script to create and populate the database
- **`inventory.db`** - SQLite database file (created by running create_database.py)

## 🗄️ Database Structure

### Tables

#### 1. products
Master data for all products in the inventory system.

```sql
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_cost REAL NOT NULL,
    retail_price REAL NOT NULL,
    supplier_id TEXT NOT NULL,
    supplier_name TEXT NOT NULL
);
```

**Sample Data:** 20 products across categories (Beverages, Dairy, Snacks)

#### 2. stores
Information about retail store locations.

```sql
CREATE TABLE stores (
    store_id TEXT PRIMARY KEY,
    store_name TEXT NOT NULL,
    location TEXT NOT NULL,
    manager_name TEXT NOT NULL
);
```

**Sample Data:** 3 stores (Bangkok, Chiang Mai, Phuket)

#### 3. inventory
Current stock levels at each store for each product.

```sql
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
    UNIQUE(product_id, store_id)
);
```

**Sample Data:** 60 inventory records (20 products × 3 stores)

#### 4. transactions
Historical record of all inventory movements.

```sql
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
    CHECK (transaction_type IN ('Sold', 'Received', 'Adjusted', 'Returned'))
);
```

**Sample Data:** 50 transactions over the past 30 days

### Views

Pre-built views for common queries:

#### v_low_stock_items
Products below reorder point with ordering recommendations.

```sql
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    i.store_id,
    s.store_name,
    i.current_stock,
    i.reorder_point,
    (i.reorder_point - i.current_stock) as units_to_order
FROM products p
JOIN inventory i ON p.product_id = i.product_id
JOIN stores s ON i.store_id = s.store_id
WHERE i.current_stock < i.reorder_point;
```

#### v_product_sales
Sales summary by product with revenue and profit.

```sql
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity ELSE 0 END) as total_sold,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity * p.retail_price ELSE 0 END) as total_revenue,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity * (p.retail_price - p.unit_cost) ELSE 0 END) as total_profit
FROM products p
LEFT JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.product_id;
```

#### v_store_inventory_value
Inventory value by store.

```sql
SELECT 
    s.store_id,
    s.store_name,
    COUNT(DISTINCT i.product_id) as product_count,
    SUM(i.current_stock) as total_units,
    SUM(i.current_stock * p.unit_cost) as inventory_cost_value,
    SUM(i.current_stock * p.retail_price) as inventory_retail_value
FROM stores s
LEFT JOIN inventory i ON s.store_id = i.store_id
LEFT JOIN products p ON i.product_id = p.product_id
GROUP BY s.store_id;
```

#### v_category_performance
Performance metrics by product category.

```sql
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) as product_count,
    SUM(i.current_stock) as total_stock,
    AVG(p.retail_price - p.unit_cost) as avg_profit_margin,
    SUM(CASE WHEN t.transaction_type = 'Sold' THEN t.quantity ELSE 0 END) as total_sold
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.category;
```

## 🚀 Quick Start

### Create Database

```bash
python3 create_database.py
```

This will:
1. Remove existing database if present
2. Create new `inventory.db` file
3. Execute schema from `schema.sql`
4. Insert sample data
5. Verify data integrity

### Query Database

Using SQLite command line:

```bash
# Open database
sqlite3 inventory.db

# List tables
.tables

# Show schema
.schema products

# Query data
SELECT * FROM products LIMIT 5;
SELECT * FROM v_low_stock_items;

# Exit
.quit
```

Using Python:

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('inventory.db')

# Query with pandas
df = pd.read_sql_query("SELECT * FROM products", conn)
print(df)

# Close connection
conn.close()
```

## 📊 Sample Queries

### Stock Management

```sql
-- Products below reorder point
SELECT * FROM v_low_stock_items;

-- Stock by store
SELECT s.store_name, COUNT(*) as product_count, SUM(i.current_stock) as total_units
FROM stores s
JOIN inventory i ON s.store_id = i.store_id
GROUP BY s.store_name;

-- Products with zero stock
SELECT p.product_name, s.store_name
FROM products p
JOIN inventory i ON p.product_id = i.product_id
JOIN stores s ON i.store_id = s.store_id
WHERE i.current_stock = 0;
```

### Sales Analytics

```sql
-- Top 10 best sellers
SELECT * FROM v_product_sales
ORDER BY total_sold DESC
LIMIT 10;

-- Sales by category
SELECT category, SUM(total_sold) as category_sales
FROM v_product_sales
GROUP BY category
ORDER BY category_sales DESC;

-- Recent transactions
SELECT t.transaction_date, p.product_name, t.transaction_type, t.quantity
FROM transactions t
JOIN products p ON t.product_id = p.product_id
ORDER BY t.transaction_date DESC
LIMIT 20;
```

### Financial Analysis

```sql
-- Inventory value by store
SELECT * FROM v_store_inventory_value;

-- Products with highest profit margin
SELECT product_name, 
       retail_price - unit_cost as profit,
       ROUND((retail_price - unit_cost) / unit_cost * 100, 2) as margin_percent
FROM products
ORDER BY margin_percent DESC
LIMIT 10;

-- Total inventory value
SELECT 
    SUM(i.current_stock * p.unit_cost) as total_cost,
    SUM(i.current_stock * p.retail_price) as total_retail_value,
    SUM(i.current_stock * (p.retail_price - p.unit_cost)) as potential_profit
FROM inventory i
JOIN products p ON i.product_id = p.product_id;
```

## 🔧 Maintenance

### Add New Product

```sql
INSERT INTO products (product_id, product_name, category, unit_cost, retail_price, supplier_id, supplier_name)
VALUES ('SKU021', 'New Product', 'Category', 10.00, 15.00, 'SUP001', 'Supplier Name');

-- Add inventory for all stores
INSERT INTO inventory (product_id, store_id, current_stock, reorder_point, max_capacity)
SELECT 'SKU021', store_id, 0, 50, 200
FROM stores;
```

### Update Stock Levels

```sql
-- Receive inventory
UPDATE inventory 
SET current_stock = current_stock + 100,
    last_updated = CURRENT_DATE
WHERE product_id = 'SKU001' AND store_id = 'STORE001';

-- Record transaction
INSERT INTO transactions (transaction_id, product_id, store_id, transaction_type, quantity, transaction_date, notes)
VALUES ('TXN051', 'SKU001', 'STORE001', 'Received', 100, CURRENT_DATE, 'Weekly delivery');
```

### Backup Database

```bash
# Create backup
cp inventory.db inventory_backup_$(date +%Y%m%d).db

# Or use SQLite backup command
sqlite3 inventory.db ".backup inventory_backup.db"
```

## 📈 Performance Tips

1. **Use Indexes**: Already created on frequently queried columns
2. **Use Views**: Pre-built views for common queries
3. **Limit Results**: Use LIMIT clause for large result sets
4. **Analyze Queries**: Use EXPLAIN QUERY PLAN to optimize

```sql
-- Check query execution plan
EXPLAIN QUERY PLAN
SELECT * FROM v_low_stock_items;
```

## 🔍 Troubleshooting

**Database locked error:**
- Close all connections to the database
- Check for other processes accessing the file

**Constraint violation:**
- Verify foreign key references exist
- Check UNIQUE constraints
- Validate CHECK constraints

**Performance issues:**
- Add indexes on frequently queried columns
- Use views for complex queries
- Vacuum database periodically: `VACUUM;`

## 📝 Notes

- Database file size: ~100KB with sample data
- SQLite version: 3.x compatible
- Character encoding: UTF-8
- Date format: YYYY-MM-DD
- Supports Thai and English text

---

**Made with Bob**