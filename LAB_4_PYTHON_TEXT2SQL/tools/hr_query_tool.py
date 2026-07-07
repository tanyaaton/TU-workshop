"""
HR Query Tool for Watson Orchestrate
Converts natural language queries to SQL queries for the HR SQLite database
Supports Thai and English languages
"""

from typing import List, Dict, Any
from typing_extensions import TypedDict
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import sqlite3
import pandas as pd
import json
import re
import os


class HRQueryInput(TypedDict):
    query: str  # Natural language query in Thai or English


class HRQueryOutput(TypedDict):
    query_intent: str
    sql_query: str
    results: List[Dict[str, Any]]
    row_count: int
    summary: str
    formatted_output: str
    insights: List[str]


@tool(
    name="hr_query_tool",
    description=(
        "Converts natural language queries (Thai/English) to SQL queries for HR analytics. "
        "Can answer questions about employee headcount, salaries, leave balances, "
        "performance ratings, and department comparisons using a SQLite database."
    )
)
def main(input: HRQueryInput, context) -> HRQueryOutput:
    """
    Convert natural language to SQL query and execute against the HR SQLite database.

    Steps:
    1. Detect language (Thai / English)
    2. Parse the query with LLM → structured JSON
    3. Build SQL from the JSON
    4. Execute against SQLite
    5. Generate insights and format results
    """

    try:
        query    = input['query']
        language = detect_language(query)

        parsed_query = parse_query_with_llm(query, context)
        sql_query    = generate_sql(parsed_query)
        result_df    = execute_sql_query(sql_query, context)
        insights     = generate_insights(result_df, parsed_query['intent'], language)
        formatted    = format_results(result_df, query, language)
        summary      = create_summary(result_df, parsed_query['intent'], language)
        results      = result_df.to_dict('records') if not result_df.empty else []

        return {
            'query_intent':   parsed_query['intent'],
            'sql_query':      sql_query,
            'results':        results,
            'row_count':      len(results),
            'summary':        summary,
            'formatted_output': formatted,
            'insights':       insights,
        }

    except Exception as e:
        error_msg = (
            f"เกิดข้อผิดพลาด: {str(e)}"
            if 'language' in locals() and language == 'th'
            else f"Error: {str(e)}"
        )
        return {
            'query_intent':   'error',
            'sql_query':      '',
            'results':        [],
            'row_count':      0,
            'summary':        error_msg,
            'formatted_output': error_msg,
            'insights':       [],
        }


# ─────────────────────────────────────────────────────────────────────────────
# Language detection
# ─────────────────────────────────────────────────────────────────────────────

def detect_language(query: str) -> str:
    """Return 'th' if the query contains Thai characters, else 'en'."""
    return 'th' if re.search(r'[\u0E00-\u0E7F]', query) else 'en'


# ─────────────────────────────────────────────────────────────────────────────
# LLM-based query parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_query_with_llm(query: str, context) -> Dict:
    """Use the LLM (via Watson Orchestrate context) to parse the query into SQL parts."""

    system_prompt = """You are a SQL query generator for an HR Management SQLite database.

Database Schema:
1. departments: department_id, department_name, location, head_count_budget
2. employees: employee_id, full_name, department_id, job_title, employment_type, hire_date, salary, manager_id
3. leave_requests: leave_id, employee_id, leave_type, start_date, end_date, days_taken, status
4. performance_reviews: review_id, employee_id, review_period, rating, reviewer_id, comments

Pre-built views (use these for common queries):
- v_headcount_by_department  → headcount, avg/min/max salary, open positions per department
- v_leave_summary            → leave days used by type per employee
- v_high_performers          → employees with rating >= 4.0
- v_salary_band              → salary min/max/avg by department + job title

CRITICAL RULES:
- employment_type values: 'Full-time', 'Part-time', 'Contract'
- leave_type values: 'Annual', 'Sick', 'Maternity', 'Personal', 'Unpaid'
- leave status values: 'Approved', 'Pending', 'Rejected'
- rating is 1.0–5.0
- Always JOIN departments to get department_name when querying employees
- Use GROUP BY when aggregating (SUM, COUNT, AVG)

Parse the user query and return ONLY a JSON object with this structure:
{
  "intent": "headcount|salary_analysis|leave_analysis|performance|employee_info|department_comparison|high_performers|salary_band",
  "tables": ["employees"],
  "columns": ["employees.full_name", "employees.salary"],
  "joins": [{"table": "departments", "on": "employees.department_id = departments.department_id"}],
  "where_conditions": ["employees.employment_type = 'Full-time'"],
  "group_by": [],
  "order_by": "employees.salary DESC",
  "limit": 20
}

Return ONLY valid JSON, no other text."""

    try:
        llm_response = context.call_llm(
            system_prompt=system_prompt,
            user_prompt=f"Query: {query}",
            temperature=0.1,
        )
        json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return simple_query_parser(query)
    except Exception:
        return simple_query_parser(query)


# ─────────────────────────────────────────────────────────────────────────────
# Rule-based fallback parser
# ─────────────────────────────────────────────────────────────────────────────

def simple_query_parser(query: str) -> Dict:
    """Simple rule-based parser used as fallback when LLM is unavailable."""

    q = query.lower()

    # ── High performers / performance ──────────────────────────────────────
    if any(w in q for w in ['high performer', 'top performer', 'best employee', 'ผลงานดี', 'rating', 'คะแนน', 'performance']):
        return {
            'intent': 'performance',
            'tables': ['employees'],
            'columns': ['employees.full_name', 'employees.job_title', 'departments.department_name',
                        'performance_reviews.rating', 'performance_reviews.review_period'],
            'joins': [
                {'table': 'departments',         'on': 'employees.department_id = departments.department_id'},
                {'table': 'performance_reviews', 'on': 'employees.employee_id = performance_reviews.employee_id'},
            ],
            'where_conditions': [],
            'group_by': [],
            'order_by': 'performance_reviews.rating DESC',
            'limit': 20,
        }

    # ── Leave ──────────────────────────────────────────────────────────────
    if any(w in q for w in ['leave', 'ลา', 'วันลา', 'sick', 'annual leave', 'ลาป่วย', 'ลาพักร้อน']):
        return {
            'intent': 'leave_analysis',
            'tables': ['employees'],
            'columns': ['employees.full_name', 'departments.department_name',
                        'leave_requests.leave_type', 'leave_requests.days_taken', 'leave_requests.status'],
            'joins': [
                {'table': 'departments',    'on': 'employees.department_id = departments.department_id'},
                {'table': 'leave_requests', 'on': 'employees.employee_id = leave_requests.employee_id'},
            ],
            'where_conditions': ["leave_requests.status = 'Approved'"],
            'group_by': [],
            'order_by': 'leave_requests.days_taken DESC',
            'limit': 50,
        }

    # ── Salary ─────────────────────────────────────────────────────────────
    if any(w in q for w in ['salary', 'เงินเดือน', 'pay', 'compensation', 'wage']):
        return {
            'intent': 'salary_analysis',
            'tables': ['employees'],
            'columns': ['departments.department_name', 'employees.job_title',
                        'COUNT(employees.employee_id) AS headcount',
                        'ROUND(AVG(employees.salary),2) AS avg_salary',
                        'ROUND(MIN(employees.salary),2) AS min_salary',
                        'ROUND(MAX(employees.salary),2) AS max_salary'],
            'joins': [{'table': 'departments', 'on': 'employees.department_id = departments.department_id'}],
            'where_conditions': [],
            'group_by': ['departments.department_name', 'employees.job_title'],
            'order_by': 'avg_salary DESC',
            'limit': 50,
        }

    # ── Headcount / department ─────────────────────────────────────────────
    if any(w in q for w in ['headcount', 'head count', 'how many', 'จำนวน', 'พนักงาน', 'department', 'แผนก']):
        return {
            'intent': 'headcount',
            'tables': ['departments'],
            'columns': ['departments.department_name', 'departments.location',
                        'departments.head_count_budget',
                        'COUNT(employees.employee_id) AS actual_headcount',
                        '(departments.head_count_budget - COUNT(employees.employee_id)) AS open_positions'],
            'joins': [{'table': 'employees', 'on': 'departments.department_id = employees.department_id'}],
            'where_conditions': [],
            'group_by': ['departments.department_id', 'departments.department_name',
                         'departments.location', 'departments.head_count_budget'],
            'order_by': 'actual_headcount DESC',
            'limit': 10,
        }

    # ── Default: employee list ─────────────────────────────────────────────
    return {
        'intent': 'employee_info',
        'tables': ['employees'],
        'columns': ['employees.employee_id', 'employees.full_name', 'employees.job_title',
                    'departments.department_name', 'employees.employment_type', 'employees.hire_date'],
        'joins': [{'table': 'departments', 'on': 'employees.department_id = departments.department_id'}],
        'where_conditions': [],
        'group_by': [],
        'order_by': 'employees.full_name ASC',
        'limit': 50,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SQL builder
# ─────────────────────────────────────────────────────────────────────────────

def generate_sql(parsed: Dict) -> str:
    """Build a SQL SELECT statement from the parsed query structure."""

    columns = ', '.join(parsed.get('columns', ['*']))
    sql = f"SELECT {columns}\nFROM {parsed['tables'][0]}"

    for join in parsed.get('joins', []):
        sql += f"\nLEFT JOIN {join['table']} ON {join['on']}"

    where = parsed.get('where_conditions', [])
    if where:
        sql += f"\nWHERE {' AND '.join(where)}"

    group_by = parsed.get('group_by', [])
    if group_by:
        sql += f"\nGROUP BY {', '.join(group_by)}"

    order_by = parsed.get('order_by', '')
    if order_by:
        sql += f"\nORDER BY {order_by}"

    limit = parsed.get('limit', 0)
    if limit:
        sql += f"\nLIMIT {limit}"

    return sql


# ─────────────────────────────────────────────────────────────────────────────
# Database helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_db_path(context) -> str:
    """Resolve path to hr.db — looks next to the tool file first."""

    tool_dir = os.path.dirname(os.path.abspath(__file__))
    db_path  = os.path.join(tool_dir, 'hr.db')

    if os.path.exists(db_path):
        return db_path

    try:
        config = context.get_credentials()
        if 'db_path' in config:
            return config['db_path']
    except Exception:
        pass

    raise FileNotFoundError(
        f"Database not found at {db_path}. "
        "Please ensure hr.db is uploaded with the tool package using --package-root parameter."
    )


def execute_sql_query(sql_query: str, context) -> pd.DataFrame:
    """Execute SQL against the HR SQLite database and return a DataFrame."""

    db_path = get_db_path(context)
    conn    = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query(sql_query, conn)
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Insights & formatting
# ─────────────────────────────────────────────────────────────────────────────

def generate_insights(df: pd.DataFrame, intent: str, language: str) -> List[str]:
    """Generate actionable HR insights from query results."""

    insights = []
    if df.empty:
        return insights

    th = language == 'th'

    if intent == 'headcount':
        if 'open_positions' in df.columns:
            open_pos = df['open_positions'].sum()
            if open_pos > 0:
                insights.append(
                    f"🔍 มีตำแหน่งว่าง {open_pos} ตำแหน่งทั่วทั้งองค์กร" if th
                    else f"🔍 {open_pos} open positions across the organisation"
                )

    elif intent == 'salary_analysis':
        if 'avg_salary' in df.columns:
            overall_avg = df['avg_salary'].mean()
            insights.append(
                f"💰 เงินเดือนเฉลี่ยรวม: ฿{overall_avg:,.0f}" if th
                else f"💰 Overall average salary: ฿{overall_avg:,.0f}"
            )

    elif intent == 'performance':
        if 'rating' in df.columns:
            avg_rating = df['rating'].mean()
            top_count  = (df['rating'] >= 4.0).sum()
            insights.append(
                f"⭐ คะแนน performance เฉลี่ย: {avg_rating:.1f}/5.0" if th
                else f"⭐ Average performance rating: {avg_rating:.1f}/5.0"
            )
            insights.append(
                f"🏆 พนักงาน high performer (≥4.0): {top_count} คน" if th
                else f"🏆 High performers (≥ 4.0): {top_count} employees"
            )

    elif intent == 'leave_analysis':
        if 'days_taken' in df.columns:
            total_days = df['days_taken'].sum()
            insights.append(
                f"📅 รวมวันลาที่ได้รับอนุมัติ: {total_days} วัน" if th
                else f"📅 Total approved leave days: {total_days}"
            )

    if len(df) > 0:
        insights.append(
            f"✅ พบข้อมูล {len(df)} รายการ" if th
            else f"✅ Found {len(df)} record{'s' if len(df) != 1 else ''}"
        )

    return insights


def format_results(df: pd.DataFrame, query: str, language: str) -> str:
    """Format DataFrame as a Markdown table (max 8 columns)."""

    if df.empty:
        return "ไม่พบข้อมูล" if language == 'th' else "No data found"

    if len(df.columns) > 8:
        df = df.iloc[:, :8]

    return df.to_markdown(index=False, floatfmt=".2f")


def create_summary(df: pd.DataFrame, intent: str, language: str) -> str:
    """Create a one-line summary of the query results."""

    if df.empty:
        return "ไม่พบข้อมูลที่ตรงกับเงื่อนไข" if language == 'th' else "No data matches the criteria"

    count = len(df)
    if language == 'th':
        return f"พบข้อมูล {count} รายการ"
    return f"Found {count} record{'s' if count != 1 else ''}"


# ─────────────────────────────────────────────────────────────────────────────
# Local test entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("HR Query Tool — Ready for Watson Orchestrate")
    print("Using SQLite database (hr.db) for Text-to-SQL conversion")

# Made with Bob
