# LAB 6: Python Text-to-SQL Tool for Retail Inventory Analytics

Build a conversational analytics agent that converts natural language queries into SQL queries for retail inventory management using Watson Orchestrate, Python, and SQLite.

---

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Create a Python tool that converts natural language to SQL queries
- Deploy SQLite database with Watson Orchestrate using package root
- Build an agent that provides conversational data analytics
- Handle complex inventory queries in Thai and English
- Implement true Text-to-SQL conversion with LLM assistance

---

## 📋 Prerequisites

- Complete Lab 0 (Setup the lab environment)
- Access to Watson Orchestrate instance
- Python 3.8 or higher installed
- Basic understanding of Python and SQL concepts
- Watson Orchestrate CLI installed (`pip install ibm-watsonx-orchestrate`)

**Note:** No database server setup required - SQLite is file-based!

---

## 🏗️ Architecture Overview

```
User Query (Thai/English)
    ↓
Watson Orchestrate Agent
    ↓
Python Tool (inventory_query_tool)
    ↓
LLM Query Parser → Parse Intent & Generate SQL
    ↓
SQLite Database → Execute SQL Query
    ↓
Pandas DataFrame → Process Results
    ↓
Result Formatter → Markdown Table + Insights
    ↓
User Response
```

### Key Components

1. **SQLite Database**: File-based relational database (inventory.db)
2. **Python Tool**: Converts natural language to SQL queries
3. **LLM Parser**: Understands query intent and generates SQL
4. **SQL Executor**: Runs queries against SQLite
5. **Watson Orchestrate Agent**: Conversational interface

### Why SQLite?

✅ No external service dependencies  
✅ No API keys or authentication needed  
✅ True relational database with SQL  
✅ Portable single-file database  
✅ Works offline  
✅ Zero setup time for participants  

---

## 📊 PART 1: Database Setup

### Step 1: Understand Database Structure

The SQLite database contains 4 main tables with sample retail inventory data:

#### Table 1: products
| Column | Type | Description |
|--------|------|-------------|
| product_id | TEXT | Primary key (e.g., SKU001) |
| product_name | TEXT | Product name |
| category | TEXT | Product category |
| unit_cost | REAL | Cost price |
| retail_price | REAL | Selling price |
| supplier_id | TEXT | Supplier identifier |
| supplier_name | TEXT | Supplier name |

#### Table 2: stores
| Column | Type | Description |
|--------|------|-------------|
| store_id | TEXT | Primary key (e.g., STORE001) |
| store_name | TEXT | Store name |
| location | TEXT | Store location |
| manager_name | TEXT | Store manager |

#### Table 3: inventory
| Column | Type | Description |
|--------|------|-------------|
| inventory_id | INTEGER | Auto-increment primary key |
| product_id | TEXT | Foreign key to products |
| store_id | TEXT | Foreign key to stores |
| current_stock | INTEGER | Current stock level |
| reorder_point | INTEGER | Minimum stock threshold |
| max_capacity | INTEGER | Maximum storage capacity |
| last_updated | DATE | Last update date |

#### Table 4: transactions
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | TEXT | Primary key |
| product_id | TEXT | Foreign key to products |
| store_id | TEXT | Foreign key to stores |
| transaction_type | TEXT | Sold, Received, Adjusted, Returned |
| quantity | INTEGER | Transaction quantity |
| transaction_date | DATE | Transaction date |
| notes | TEXT | Additional notes |

### Step 2: Create Database

The database is already created for you! Simply run:

```bash
cd database
python3 create_database.py
```

This will:
- Create `inventory.db` file
- Set up all tables with proper schema
- Insert 20 sample products
- Add 3 store locations
- Create 60 inventory records
- Generate 50 sample transactions
- Create helpful views for common queries

**Database Location:** `database/inventory.db`

### Step 3: Verify Database (Optional)

You can verify the database using SQLite command line:

```bash
sqlite3 database/inventory.db

# Inside SQLite shell:
.tables                          # List all tables
.schema products                 # Show products table schema
SELECT COUNT(*) FROM products;   # Count products
SELECT * FROM v_low_stock_items; # View low stock items
.quit                            # Exit
```

---

## 🛠️ PART 2: Python Tool Implementation

### Step 4: Review Tool Code

The Python tool (`tools/inventory_query_tool.py`) uses the **@tool decorator** to register with Watson Orchestrate:

```python
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict  # Required for Python < 3.12
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(
    name="inventory_query_tool",
    description="Converts natural language queries to SQL for inventory analytics"
)
def main(input: InventoryQueryInput, context) -> InventoryQueryOutput:
    # Tool implementation
```

**Important Notes:**
- Use `typing_extensions.TypedDict` instead of `typing.TypedDict` for Python < 3.12
- The `@tool` decorator is from `ibm_watsonx_orchestrate.agent_builder.tools`

### Step 5: Understand Text-to-SQL Process

The tool performs the following steps:

1. **Parse Query**: Uses LLM to understand natural language intent
2. **Generate SQL**: Creates appropriate SQL query
3. **Execute Query**: Runs SQL against SQLite database
4. **Process Results**: Formats data using pandas
5. **Generate Insights**: Creates actionable recommendations
6. **Return Response**: Structured output with Markdown tables

**Example Flow:**

```python
# 1. User asks in natural language
query = "แสดงสินค้าที่มีสต็อกต่ำกว่า reorder point"

# 2. LLM parses intent
parsed = {
    "intent": "low_stock",
    "tables": ["products", "inventory"],
    "where_conditions": ["current_stock < reorder_point"]
}

# 3. Generate SQL
sql = """
SELECT p.product_name, i.current_stock, i.reorder_point
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE i.current_stock < i.reorder_point
"""

# 4. Execute and return results
```

### Step 6: Install Dependencies

Install the required packages:

```bash
cd tools
pip install -r requirements.txt
```

**Dependencies:**
```
ibm-watsonx-orchestrate>=1.0.0  # Watson Orchestrate SDK
pandas==2.1.0                    # Data processing
tabulate==0.9.0                  # Table formatting
```

**Note:** `sqlite3` is built into Python, no installation needed!

---

## 🔗 PART 3: Deploy to Watson Orchestrate

### Step 7: Quick Start - Automated Import

The easiest way to deploy everything is using the automated import script:

```bash
# Navigate to lab directory
cd TH-wxo-askHR-enablement-workshop/LAB_6_PYTHON_TEXT2SQL

# Run the automated import script
./import_all.sh
```

This script will:
1. Install required dependencies
2. Copy database to tools directory (for package upload)
3. Import the Python tool **with database as a package** using `--package-root`
4. Import the agent configuration

**That's it!** Skip to Part 4 to start testing.

---

### Understanding Package Root Deployment

#### What is Package Root?

**Package Root** is a Watson Orchestrate CLI parameter that allows you to upload an entire directory as a package, including:
- Python tool files
- Data files (like SQLite databases)
- Additional Python modules
- Configuration files

#### Why Use Package Root?

✅ **Self-Contained**: Tool and data travel together  
✅ **No External Dependencies**: No cloud storage or API keys needed  
✅ **Simple Deployment**: One command uploads everything  
✅ **Reliable**: Files guaranteed to be accessible at runtime  

#### Package Structure

```
tools/
├── inventory_query_tool.py    # Main Python tool (14KB)
├── inventory.db                # SQLite database (84KB)
└── requirements.txt            # Python dependencies
```

**Total Package Size**: ~100KB (well within limits)

#### How It Works

**Local Development:**
```
/Users/pat/Desktop/Business_domain_lab/
└── TH-wxo-askHR-enablement-workshop/
    └── LAB_6_PYTHON_TEXT2SQL/
        └── tools/
            ├── inventory_query_tool.py
            └── inventory.db
```

**Watson Orchestrate Sandbox:**
```
/tool_workspace/
├── inventory_query_tool.py
└── inventory.db
```

**Key Point**: The relative path `os.path.join(__file__, 'inventory.db')` works in both environments!

---

### Step 8: Manual Import (Alternative)

If you prefer to import manually:

```bash
# 1. Install dependencies
cd tools
pip install -r requirements.txt

# 2. Copy database to tools directory
cd ..
cp database/inventory.db tools/

# 3. Import the Python tool with package root (includes database)
orchestrate tools import --kind python -f tools/inventory_query_tool.py --package-root tools/

# 4. Import the agent
orchestrate agents import -f agent/inventory_analytics_agent.yaml
```

**Important:** The `--package-root tools/` parameter is crucial! It uploads the entire `tools/` directory as a package, ensuring the database file is accessible to the tool at runtime.

### Step 9: Verify Tool Import

After importing, verify the tool is available:

1. Go to **Watson Orchestrate** web interface
2. Navigate to **Toolset** section
3. You should see `inventory_query_tool` listed
4. Click on it to view details and test

---

## 🤖 PART 4: Configure Analytics Agent

### Step 10: Agent Configuration

The agent is automatically imported by the script. If you need to configure manually:

1. Navigate to **Agent Builder**
2. Click **Create agent +**
3. Enter details:
   - **Name**: `Inventory Analytics Agent`
   - **Description**: `Provides conversational analytics for retail inventory using Text-to-SQL`

### Step 11: Add Tool to Agent

1. In the agent, go to **Toolset** section
2. Click **Add tool**
3. Select `inventory_query_tool`
4. Click **Add**

### Step 12: Configure Agent Behavior

In the **Behavior** section, the following instructions are configured:

```
You are an Inventory Analytics assistant for retail supermarket staff.

IMPORTANT RULES:
1. Always use the inventory_query_tool for data queries
2. Explain what SQL query will be generated
3. Present results in clear Markdown tables
4. Highlight important insights (low stock, high sales, trends)
5. Provide actionable recommendations based on data
6. Handle both Thai and English queries naturally
7. If query is ambiguous, ask for clarification
8. Suggest follow-up questions to explore data further

Query Capabilities:
- Stock levels and availability
- Low stock alerts and reorder recommendations
- Sales analysis and trends
- Product performance by category
- Store comparisons
- Supplier information
- Top/bottom performers
- Inventory value calculations
- Profit margin analysis

Response Format:
1. Acknowledge the query
2. Explain the SQL query being executed
3. Show the data in a table
4. Provide key insights
5. Suggest next steps or related queries

Always be helpful, accurate, and proactive in providing insights!
```

### Step 13: Select Model

Choose **GPT-OSS 120B** or **Llama 3.3 70B** for best performance with Thai language and SQL generation.

---

## 📚 PART 5: Test the Agent

### Test 1: Stock Level Queries

**Thai Queries:**
```
- แสดงสินค้าที่มีสต็อกต่ำกว่า reorder point
- เช็คสต็อกทั้งหมดของสาขา STORE001
- สินค้าไหนที่สาขา 1 ใกล้หมด
```

**English Queries:**
```
- Show all products with stock below reorder point
- Check all inventory at STORE001
- Which products are running low at store 1?
```

**Expected SQL:**
```sql
SELECT p.product_name, i.current_stock, i.reorder_point, s.store_name
FROM products p
JOIN inventory i ON p.product_id = i.product_id
JOIN stores s ON i.store_id = s.store_id
WHERE i.current_stock < i.reorder_point
```

### Test 2: Sales Analytics

**Thai Queries:**
```
- สินค้าขายดี 10 อันดับแรก
- ยอดขายรวมของแต่ละหมวดสินค้า
- เปรียบเทียบยอดขายระหว่างสาขา
```

**English Queries:**
```
- Top 10 best-selling products
- Total sales by product category
- Compare sales between stores
```

**Expected SQL:**
```sql
SELECT p.product_name, SUM(t.quantity) as total_sold
FROM products p
JOIN transactions t ON p.product_id = t.product_id
WHERE t.transaction_type = 'Sold'
GROUP BY p.product_name
ORDER BY total_sold DESC
LIMIT 10
```

### Test 3: Complex Queries

**Thai Queries:**
```
- คำนวณมูลค่าสต็อกรวมของแต่ละสาขา
- แสดงสินค้าที่ไม่มีการขายในช่วง 30 วันที่ผ่านมา
- หาสินค้าที่มี profit margin สูงสุด
```

**English Queries:**
```
- Calculate total inventory value by store
- Show products with no sales in the last 30 days
- Find products with highest profit margin
```

### Additional Test Queries

For a comprehensive list of test queries organized by category, see the query examples below:

#### 📊 Stock Level Queries
- Basic stock checks
- Low stock alerts
- Stock by location

#### 💰 Sales Analytics Queries
- Sales performance
- Sales by category
- Sales by store

#### 📦 Product Information Queries
- Product details
- Product categories

#### 🏪 Supplier Queries
- Supplier information

#### 💵 Financial Queries
- Profit analysis
- Inventory value

#### 📈 Trend Analysis Queries
- Transaction history
- Performance trends

#### 🔍 Complex Analytical Queries
- Multi-criteria analysis
- Store performance
- Optimization recommendations

---

## 🎓 Key Takeaways

1. **True Text-to-SQL**: Actual SQL generation from natural language
2. **No External Dependencies**: SQLite is file-based, no server needed
3. **Bilingual Support**: Seamless Thai and English query handling
4. **Relational Database**: Proper joins, foreign keys, and constraints
5. **Actionable Insights**: Automated recommendations from data
6. **Easy Maintenance**: Update database directly with SQL
7. **Portable**: Single file database can be shared easily
8. **Workshop-Ready**: Zero setup time for participants

---

## 🔧 Troubleshooting

### Common Issues

**1. "Database file not found"**
- Ensure database was copied to tools directory: `ls -lh tools/inventory.db`
- Re-import with `--package-root`: 
  ```bash
  orchestrate tools import --kind python -f tools/inventory_query_tool.py --package-root tools/
  ```

**2. "SQL syntax error"**
- Check generated SQL in tool output
- Verify table and column names match schema
- Review `database/schema.sql` for correct structure

**3. "No data found"**
- Verify database has data: `sqlite3 database/inventory.db "SELECT COUNT(*) FROM products;"`
- Check WHERE conditions in generated SQL
- Review filter logic in query parser

**4. Query returns unexpected results**
- Check SQL JOIN conditions
- Verify data types (TEXT vs INTEGER)
- Review aggregation functions

**5. Tool execution timeout**
- Simplify complex queries
- Add indexes to frequently queried columns
- Limit result set with LIMIT clause

**6. Sales queries returning incorrect results**
- The tool has been updated to correctly use the `transactions` table
- Ensure you're using the latest version of the tool
- The LLM now correctly generates SQL with `WHERE transaction_type = 'Sold'`

---

## 🚀 Next Steps

After completing this lab, you can:

1. **Add More Data**: Insert additional products, stores, transactions via SQL
2. **Create Custom Views**: Build views for specific business queries
3. **Add Indexes**: Optimize query performance with strategic indexes
4. **Extend Schema**: Add tables for suppliers, customers, orders
5. **Advanced Analytics**: Implement forecasting, trend analysis, anomaly detection
6. **Export Data**: Generate reports in CSV, Excel, or PDF format

---

## 📊 Business Value

- **Self-Service Analytics**: Staff can query data without SQL knowledge
- **Faster Insights**: Instant answers to business questions
- **Better Decisions**: Data-driven inventory management
- **No Infrastructure**: No database server or cloud service needed
- **Cost Effective**: Free, open-source SQLite database
- **Bilingual**: Thai and English support for diverse workforce
- **Scalable**: Easy to add more data and query types
- **Portable**: Database file can be backed up, shared, or migrated easily

---

## 📝 Additional Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Watson Orchestrate Developer Portal](https://developer.watson-orchestrate.ibm.com/)
- [Text-to-SQL Best Practices](https://arxiv.org/abs/2208.13629)

---

## 🎯 Lab Summary

**What You Built:**
- ✅ SQLite database with retail inventory data
- ✅ Python Text-to-SQL conversion tool
- ✅ Bilingual conversational analytics agent
- ✅ Natural language query interface

**Skills Learned:**
- ✅ Database schema design
- ✅ SQL query generation from natural language
- ✅ LLM-powered query parsing
- ✅ Data analytics with pandas
- ✅ Watson Orchestrate agent development
- ✅ Package root deployment strategy

**Time to Complete:** 45-60 minutes

---

## 💡 Tips for Effective Queries

### Best Practices

1. **Be Specific**: Include store IDs, product names, or categories
2. **Use Time Ranges**: Specify "this month", "last week", etc.
3. **Ask Follow-ups**: Build on previous results
4. **Request Comparisons**: Compare stores, categories, or time periods
5. **Ask for Insights**: Request recommendations or analysis

### Query Patterns

**Good Queries:**
- "แสดงสินค้าที่สต็อกต่ำกว่า reorder point ที่สาขา STORE001"
- "Top 5 best-selling products in Beverages category"
- "Compare inventory value between all stores"

**Avoid:**
- Too vague: "แสดงข้อมูล" (Show data)
- Too complex: Multiple unrelated questions in one query
- Ambiguous: "สินค้า" without context

---

**Congratulations!** You've successfully created a conversational analytics agent for retail inventory management using Python Text-to-SQL and SQLite! 🎉

---

*Made with ❤️ for Watson Orchestrate Workshop*