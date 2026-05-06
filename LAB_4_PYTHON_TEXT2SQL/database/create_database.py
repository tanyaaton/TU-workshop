#!/usr/bin/env python3
"""
Create and populate SQLite database for Retail Inventory Management
This script creates the database schema and inserts sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta

def create_database(db_path='inventory.db'):
    """Create SQLite database with schema and sample data"""
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Connect to database (creates new file)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Creating database: {db_path}")
    
    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Execute schema (split by semicolon to handle multiple statements)
    for statement in schema_sql.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    print("✓ Schema created")
    
    # Insert sample data
    insert_sample_data(cursor)
    
    # Commit changes
    conn.commit()
    
    # Verify data
    verify_database(cursor)
    
    conn.close()
    print(f"\n✓ Database created successfully: {db_path}")
    print(f"  Location: {os.path.abspath(db_path)}")


def insert_sample_data(cursor):
    """Insert sample data into all tables"""
    
    print("\nInserting sample data...")
    
    # Insert Stores
    stores = [
        ('STORE001', 'Central Bangkok', 'Bangkok, Thailand', 'Somchai Pattana'),
        ('STORE002', 'Chiang Mai Branch', 'Chiang Mai, Thailand', 'Narin Srisuk'),
        ('STORE003', 'Phuket Branch', 'Phuket, Thailand', 'Pimchanok Thongchai'),
    ]
    
    cursor.executemany('''
        INSERT INTO stores (store_id, store_name, location, manager_name)
        VALUES (?, ?, ?, ?)
    ''', stores)
    print(f"  ✓ Inserted {len(stores)} stores")
    
    # Insert Products
    products = [
        ('SKU001', 'Coca-Cola 1.5L', 'Beverages', 18.50, 25.00, 'SUP001', 'Thai Beverage Co.'),
        ('SKU002', 'Fresh Milk 1L', 'Dairy', 35.00, 45.00, 'SUP002', 'Dairy Farm Ltd.'),
        ('SKU003', 'Lay\'s Chips 50g', 'Snacks', 8.00, 12.00, 'SUP003', 'Snack World'),
        ('SKU004', 'Pepsi 1.5L', 'Beverages', 18.00, 24.00, 'SUP001', 'Thai Beverage Co.'),
        ('SKU005', 'Yogurt 150g', 'Dairy', 12.00, 18.00, 'SUP002', 'Dairy Farm Ltd.'),
        ('SKU006', 'Pringles 110g', 'Snacks', 35.00, 49.00, 'SUP003', 'Snack World'),
        ('SKU007', 'Mineral Water 1.5L', 'Beverages', 8.00, 12.00, 'SUP004', 'Pure Water Co.'),
        ('SKU008', 'Cheese Slice 200g', 'Dairy', 45.00, 65.00, 'SUP002', 'Dairy Farm Ltd.'),
        ('SKU009', 'Doritos 150g', 'Snacks', 25.00, 35.00, 'SUP003', 'Snack World'),
        ('SKU010', 'Orange Juice 1L', 'Beverages', 28.00, 39.00, 'SUP005', 'Fresh Juice Ltd.'),
        ('SKU011', 'Butter 250g', 'Dairy', 55.00, 75.00, 'SUP002', 'Dairy Farm Ltd.'),
        ('SKU012', 'Potato Chips 100g', 'Snacks', 15.00, 22.00, 'SUP003', 'Snack World'),
        ('SKU013', 'Green Tea 500ml', 'Beverages', 12.00, 18.00, 'SUP006', 'Tea Master Co.'),
        ('SKU014', 'Ice Cream 1L', 'Dairy', 85.00, 120.00, 'SUP007', 'Ice Cream Factory'),
        ('SKU015', 'Chocolate Bar 50g', 'Snacks', 18.00, 25.00, 'SUP008', 'Sweet Treats'),
        ('SKU016', 'Energy Drink 250ml', 'Beverages', 22.00, 32.00, 'SUP009', 'Energy Plus'),
        ('SKU017', 'Cream Cheese 200g', 'Dairy', 65.00, 89.00, 'SUP002', 'Dairy Farm Ltd.'),
        ('SKU018', 'Popcorn 100g', 'Snacks', 20.00, 29.00, 'SUP003', 'Snack World'),
        ('SKU019', 'Iced Coffee 250ml', 'Beverages', 25.00, 35.00, 'SUP010', 'Coffee House'),
        ('SKU020', 'Whipping Cream 250ml', 'Dairy', 48.00, 68.00, 'SUP002', 'Dairy Farm Ltd.'),
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_id, product_name, category, unit_cost, retail_price, supplier_id, supplier_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', products)
    print(f"  ✓ Inserted {len(products)} products")
    
    # Insert Inventory
    inventory = []
    for product in products:
        product_id = product[0]
        for store in stores:
            store_id = store[0]
            # Vary stock levels
            if 'SKU001' in product_id or 'SKU002' in product_id:
                current_stock = 45  # Low stock
                reorder_point = 50
            elif 'SKU003' in product_id:
                current_stock = 120  # Good stock
                reorder_point = 50
            else:
                import random
                current_stock = random.randint(30, 150)
                reorder_point = random.randint(40, 60)
            
            max_capacity = 200
            last_updated = datetime.now().strftime('%Y-%m-%d')
            
            inventory.append((product_id, store_id, current_stock, reorder_point, max_capacity, last_updated))
    
    cursor.executemany('''
        INSERT INTO inventory (product_id, store_id, current_stock, reorder_point, max_capacity, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', inventory)
    print(f"  ✓ Inserted {len(inventory)} inventory records")
    
    # Insert Transactions
    transactions = []
    base_date = datetime.now() - timedelta(days=30)
    
    # Generate sample transactions
    for i in range(1, 51):
        txn_id = f"TXN{str(i).zfill(4)}"
        product_id = products[(i-1) % len(products)][0]
        store_id = stores[(i-1) % len(stores)][0]
        
        # Mix of transaction types
        if i % 5 == 0:
            txn_type = 'Received'
            quantity = 100
            notes = 'Weekly delivery'
        elif i % 17 == 0:
            txn_type = 'Returned'
            quantity = 2
            notes = 'Customer return'
        else:
            txn_type = 'Sold'
            quantity = (i % 10) + 1
            notes = 'Regular sale'
        
        txn_date = (base_date + timedelta(days=i % 30)).strftime('%Y-%m-%d')
        
        transactions.append((txn_id, product_id, store_id, txn_type, quantity, txn_date, notes))
    
    cursor.executemany('''
        INSERT INTO transactions (transaction_id, product_id, store_id, transaction_type, quantity, transaction_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', transactions)
    print(f"  ✓ Inserted {len(transactions)} transactions")


def verify_database(cursor):
    """Verify database contents"""
    
    print("\nVerifying database...")
    
    tables = ['products', 'stores', 'inventory', 'transactions']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table}: {count} records")
    
    # Test a view
    cursor.execute("SELECT COUNT(*) FROM v_low_stock_items")
    low_stock_count = cursor.fetchone()[0]
    print(f"  ✓ Low stock items: {low_stock_count} products")


if __name__ == '__main__':
    # Create database in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'inventory.db')
    
    print("=" * 60)
    print("SQLite Database Creation Script")
    print("Retail Inventory Management System")
    print("=" * 60)
    
    create_database(db_path)
    
    print("\n" + "=" * 60)
    print("Database is ready for use!")
    print("=" * 60)

# Made with Bob