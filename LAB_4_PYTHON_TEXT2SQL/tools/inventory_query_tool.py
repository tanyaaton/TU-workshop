"""
Inventory Query Tool for Watson Orchestrate
Converts natural language queries to SQL queries for SQLite database
Supports Thai and English languages
"""

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import re
import os


class InventoryQueryInput(TypedDict):
    query: str  # Natural language query in Thai or English


class InventoryQueryOutput(TypedDict):
    query_intent: str
    sql_query: str
    results: List[Dict[str, Any]]
    row_count: int
    summary: str
    formatted_output: str
    insights: List[str]


@tool(
    name="inventory_query_tool",
    description="Converts natural language queries (Thai/English) to SQL queries for retail inventory analytics. Analyzes stock levels, sales data, product information, and generates actionable insights from SQLite database."
)
def main(input: InventoryQueryInput, context) -> InventoryQueryOutput:
    """
    Convert natural language to SQL query and execute against SQLite database
    
    Steps:
    1. Parse natural language query using LLM
    2. Generate SQL query
    3. Execute against SQLite database
    4. Format and return results with insights
    """
    
    try:
        query = input['query']
        
        # Detect language
        language = detect_language(query)
        
        # Parse query using LLM to generate SQL
        parsed_query = parse_query_with_llm(query, context)
        
        # Generate SQL query
        sql_query = generate_sql(parsed_query)
        
        # Execute query against SQLite
        result_df = execute_sql_query(sql_query, context)
        
        # Generate insights
        insights = generate_insights(result_df, parsed_query['intent'], language)
        
        # Format results
        formatted_output = format_results(result_df, query, language)
        
        # Create summary
        summary = create_summary(result_df, parsed_query['intent'], language)
        
        # Convert DataFrame to list of dicts
        results = result_df.to_dict('records') if not result_df.empty else []
        
        return {
            'query_intent': parsed_query['intent'],
            'sql_query': sql_query,
            'results': results,
            'row_count': len(results),
            'summary': summary,
            'formatted_output': formatted_output,
            'insights': insights
        }
        
    except Exception as e:
        error_msg = f"เกิดข้อผิดพลาด: {str(e)}" if 'language' in locals() and language == 'th' else f"Error: {str(e)}"
        return {
            'query_intent': 'error',
            'sql_query': '',
            'results': [],
            'row_count': 0,
            'summary': error_msg,
            'formatted_output': error_msg,
            'insights': []
        }


def detect_language(query: str) -> str:
    """Detect if query is in Thai or English"""
    # Check for Thai characters
    thai_pattern = re.compile(r'[\u0E00-\u0E7F]')
    return 'th' if thai_pattern.search(query) else 'en'


def parse_query_with_llm(query: str, context) -> Dict:
    """
    Use LLM to parse natural language query into structured format
    """
    
    system_prompt = """You are a SQL query generator for a retail inventory SQLite database.

Database Schema:
1. products: product_id, product_name, category, unit_cost, retail_price, supplier_id, supplier_name
2. inventory: product_id, store_id, current_stock, reorder_point, max_capacity, last_updated
3. stores: store_id, store_name, location, manager_name
4. transactions: transaction_id, product_id, store_id, transaction_type, quantity, transaction_date, notes

CRITICAL RULES:
- There is NO 'sales' table in this database
- For sales queries, ALWAYS use 'transactions' table with WHERE transaction_type = 'Sold'
- transaction_type values: 'Sold', 'Received', 'Returned', 'Adjusted'
- Always JOIN with products table to get product_name
- Use GROUP BY when aggregating (SUM, COUNT, AVG)

Example for sales/best-selling products query:
{
  "intent": "sales_analysis",
  "tables": ["products", "transactions"],
  "columns": ["products.product_name", "SUM(transactions.quantity) as total_sold"],
  "joins": [
    {"table": "transactions", "on": "products.product_id = transactions.product_id"}
  ],
  "where_conditions": ["transactions.transaction_type = 'Sold'"],
  "group_by": ["products.product_name"],
  "order_by": "total_sold DESC",
  "limit": 10
}

Parse the user's natural language query and return ONLY a JSON object with this exact structure:
{
  "intent": "stock_level|low_stock|sales_analysis|product_info|supplier_info|store_comparison|top_products|category_analysis|inventory_value|profit_analysis",
  "tables": ["products", "transactions"],
  "columns": ["products.product_name", "SUM(transactions.quantity) as total_sold"],
  "joins": [
    {"table": "transactions", "on": "products.product_id = transactions.product_id"}
  ],
  "where_conditions": ["transactions.transaction_type = 'Sold'"],
  "group_by": ["products.product_name"],
  "order_by": "total_sold DESC",
  "limit": 10
}

Return ONLY valid JSON, no other text."""

    user_prompt = f"Query: {query}"
    
    # Call LLM through context (Watson Orchestrate provides this)
    try:
        llm_response = context.call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1
        )
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            return parsed
        else:
            # Fallback to simple parsing
            return simple_query_parser(query)
            
    except Exception as e:
        # Fallback to simple parsing if LLM fails
        return simple_query_parser(query)


def simple_query_parser(query: str) -> Dict:
    """Simple rule-based query parser as fallback"""
    
    query_lower = query.lower()
    
    # Detect intent and build query structure
    if any(word in query_lower for word in ['ใกล้หมด', 'low stock', 'reorder', 'ต่ำกว่า']):
        intent = 'low_stock'
        tables = ['products', 'inventory']
        columns = ['products.product_name', 'inventory.current_stock', 'inventory.reorder_point', 'stores.store_name']
        joins = [
            {'table': 'inventory', 'on': 'products.product_id = inventory.product_id'},
            {'table': 'stores', 'on': 'inventory.store_id = stores.store_id'}
        ]
        where_conditions = ['inventory.current_stock < inventory.reorder_point']
        
    elif any(word in query_lower for word in ['ขาย', 'sales', 'sold', 'ยอดขาย', 'ขายดี', 'best-selling', 'top']):
        intent = 'sales_analysis'
        tables = ['products', 'transactions']
        columns = ['products.product_name', 'SUM(transactions.quantity) as total_sold']
        joins = [{'table': 'transactions', 'on': 'products.product_id = transactions.product_id'}]
        where_conditions = ["transactions.transaction_type = 'Sold'"]
        
    elif any(word in query_lower for word in ['สต็อก', 'stock', 'inventory', 'คงเหลือ']):
        intent = 'stock_level'
        tables = ['products', 'inventory', 'stores']
        columns = ['products.product_name', 'inventory.current_stock', 'stores.store_name']
        joins = [
            {'table': 'inventory', 'on': 'products.product_id = inventory.product_id'},
            {'table': 'stores', 'on': 'inventory.store_id = stores.store_id'}
        ]
        where_conditions = []
        
    elif any(word in query_lower for word in ['หมวด', 'category', 'ประเภท']):
        intent = 'category_analysis'
        tables = ['products']
        columns = ['category', 'COUNT(*) as product_count']
        joins = []
        where_conditions = []
        
    else:
        intent = 'product_info'
        tables = ['products']
        columns = ['*']
        joins = []
        where_conditions = []
    
    # Extract store ID if mentioned
    store_match = re.search(r'(STORE\d+|สาขา\s*\d+|store\s*\d+)', query, re.IGNORECASE)
    if store_match:
        store_text = store_match.group()
        store_num = re.search(r'\d+', store_text)
        if store_num:
            store_id = f"STORE{store_num.group().zfill(3)}"
            where_conditions.append(f"store_id = '{store_id}'")
    
    # Set GROUP BY based on intent
    if intent == 'category_analysis':
        group_by = ['category']
    elif intent == 'sales_analysis':
        group_by = ['products.product_name']
    else:
        group_by = []
    
    # Set ORDER BY based on intent
    if intent == 'sales_analysis':
        order_by = 'total_sold DESC'
    elif intent == 'low_stock':
        order_by = 'inventory.current_stock ASC'
    else:
        order_by = ''
    
    return {
        'intent': intent,
        'tables': tables,
        'columns': columns,
        'joins': joins,
        'where_conditions': where_conditions,
        'group_by': group_by,
        'order_by': order_by,
        'limit': 100
    }


def generate_sql(parsed_query: Dict) -> str:
    """Generate SQL query from parsed structure"""
    
    # Build SELECT clause
    columns = ', '.join(parsed_query.get('columns', ['*']))
    sql = f"SELECT {columns}"
    
    # Build FROM clause
    main_table = parsed_query['tables'][0]
    sql += f"\nFROM {main_table}"
    
    # Build JOIN clauses
    for join in parsed_query.get('joins', []):
        sql += f"\nLEFT JOIN {join['table']} ON {join['on']}"
    
    # Build WHERE clause
    where_conditions = parsed_query.get('where_conditions', [])
    if where_conditions:
        sql += f"\nWHERE {' AND '.join(where_conditions)}"
    
    # Build GROUP BY clause
    group_by = parsed_query.get('group_by', [])
    if group_by:
        sql += f"\nGROUP BY {', '.join(group_by)}"
    
    # Build ORDER BY clause
    order_by = parsed_query.get('order_by', '')
    if order_by:
        sql += f"\nORDER BY {order_by}"
    
    # Build LIMIT clause
    limit = parsed_query.get('limit', 0)
    if limit:
        sql += f"\nLIMIT {limit}"
    
    return sql


def get_db_path(context) -> str:
    """Get the path to the SQLite database file"""
    
    # When uploaded as package, database is in same directory as tool
    tool_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(tool_dir, 'inventory.db')
    
    # Check if database exists
    if os.path.exists(db_path):
        return db_path
    
    # Fallback: try to get from connection configuration
    try:
        config = context.get_credentials()
        if 'db_path' in config:
            return config['db_path']
    except:
        pass
    
    # If still not found, raise error with helpful message
    raise FileNotFoundError(
        f"Database not found at {db_path}. "
        "Please ensure inventory.db is uploaded with the tool package using --package-root parameter."
    )


def execute_sql_query(sql_query: str, context) -> pd.DataFrame:
    """Execute SQL query against SQLite database"""
    
    db_path = get_db_path(context)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    try:
        # Execute query and return as DataFrame
        df = pd.read_sql_query(sql_query, conn)
        return df
    finally:
        conn.close()


def generate_insights(df: pd.DataFrame, query_intent: str, language: str) -> List[str]:
    """Generate actionable insights from query results"""
    
    insights = []
    
    if df.empty:
        return insights
    
    if query_intent == 'low_stock':
        if 'current_stock' in df.columns and 'reorder_point' in df.columns:
            critical_count = len(df[df['current_stock'] < df['reorder_point'] * 0.5])
            if critical_count > 0:
                msg = f"⚠️ มีสินค้า {critical_count} รายการที่สต็อกต่ำมาก (ต่ำกว่า 50% ของจุด reorder)" if language == 'th' else f"⚠️ {critical_count} products are critically low (below 50% of reorder point)"
                insights.append(msg)
            
            msg = f"📦 ควรสั่งซื้อสินค้าเพิ่มทันที" if language == 'th' else f"📦 Should reorder these products immediately"
            insights.append(msg)
    
    elif query_intent == 'sales_analysis':
        if 'total_sold' in df.columns:
            total_sales = df['total_sold'].sum()
            msg = f"📊 ยอดขายรวม: {total_sales:,.0f} หน่วย" if language == 'th' else f"📊 Total units sold: {total_sales:,.0f}"
            insights.append(msg)
            
            if 'product_name' in df.columns and len(df) > 0:
                top_product = df.nlargest(1, 'total_sold')['product_name'].values[0]
                msg = f"🏆 สินค้าขายดีที่สุด: {top_product}" if language == 'th' else f"🏆 Best seller: {top_product}"
                insights.append(msg)
    
    elif query_intent == 'stock_level':
        if 'current_stock' in df.columns:
            total_stock = df['current_stock'].sum()
            msg = f"📦 สต็อกรวมทั้งหมด: {total_stock:,.0f} หน่วย" if language == 'th' else f"📦 Total inventory: {total_stock:,.0f} units"
            insights.append(msg)
    
    elif query_intent == 'inventory_value':
        if 'total_value' in df.columns:
            total_value = df['total_value'].sum()
            msg = f"💰 มูลค่าสต็อกรวม: ฿{total_value:,.2f}" if language == 'th' else f"💰 Total inventory value: ฿{total_value:,.2f}"
            insights.append(msg)
    
    # Add row count insight
    if len(df) > 0:
        msg = f"✅ พบข้อมูล {len(df)} รายการ" if language == 'th' else f"✅ Found {len(df)} records"
        insights.append(msg)
    
    return insights


def format_results(df: pd.DataFrame, query: str, language: str) -> str:
    """Format DataFrame results as Markdown table"""
    
    if df.empty:
        return "ไม่พบข้อมูล" if language == 'th' else "No data found"
    
    # Limit columns for readability (max 8 columns)
    if len(df.columns) > 8:
        df = df.iloc[:, :8]
    
    # Convert to Markdown table
    markdown = df.to_markdown(index=False, floatfmt=".2f")
    
    return markdown


def create_summary(df: pd.DataFrame, query_intent: str, language: str) -> str:
    """Create a summary of the query results"""
    
    if df.empty:
        return "ไม่พบข้อมูลที่ตรงกับเงื่อนไข" if language == 'th' else "No data matches the criteria"
    
    count = len(df)
    
    if language == 'th':
        summary = f"พบข้อมูล {count} รายการ"
    else:
        summary = f"Found {count} record{'s' if count != 1 else ''}"
    
    return summary


# For testing purposes
if __name__ == "__main__":
    # This section is for local testing only
    print("Inventory Query Tool - Ready for Watson Orchestrate")
    print("Using SQLite database for Text-to-SQL conversion")

# Made with Bob
