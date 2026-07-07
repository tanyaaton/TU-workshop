# Sample Queries for HR Analytics Agent

This document provides comprehensive test queries for the HR Analytics Agent in both Thai and English.

**Note:** The agent converts these natural language queries into SQL queries that run against the SQLite `hr.db` database.

---

## 👥 Headcount & Organisation Queries

### Department Headcount

**Thai:**
```
- แสดงจำนวนพนักงานแต่ละแผนก
- แผนกไหนมีพนักงานมากที่สุด
- เปรียบเทียบจำนวนพนักงานจริงกับ headcount budget
- มีตำแหน่งว่างกี่ตำแหน่งในแต่ละแผนก
```

**English:**
```
- Show headcount by department
- Which department has the most employees?
- Compare actual headcount vs approved budget
- How many open positions are there per department?
```

### Employee Type

**Thai:**
```
- มีพนักงานประเภท Contract กี่คน
- แสดงพนักงาน Part-time ทั้งหมด
- สัดส่วนพนักงาน Full-time กับ Contract คือเท่าไหร่
```

**English:**
```
- How many contract employees are there?
- Show all part-time employees
- What is the ratio of full-time to contract employees?
```

### Org Structure

**Thai:**
```
- ใครเป็นผู้จัดการของแผนก Engineering
- แสดงรายชื่อพนักงานใน Finance
- Somchai Pattana มีลูกทีมกี่คน
```

**English:**
```
- Who is the manager of the Engineering department?
- Show all employees in the Finance department
- How many direct reports does EMP001 have?
```

---

## 💰 Salary Analysis Queries

### Salary by Department

**Thai:**
```
- เปรียบเทียบเงินเดือนเฉลี่ยของแต่ละแผนก
- แผนกไหนจ่ายเงินเดือนสูงสุด
- แสดงช่วงเงินเดือน (min/max/avg) ของแต่ละแผนก
- ค่าใช้จ่ายเงินเดือนรวมต่อเดือนคือเท่าไหร่
```

**English:**
```
- Compare average salary by department
- Which department has the highest salaries?
- Show salary range (min/max/avg) per department
- What is the total monthly salary cost?
```

### Salary by Job Title

**Thai:**
```
- แสดง salary band ของแต่ละตำแหน่ง
- Software Engineer ได้เงินเดือนเฉลี่ยเท่าไหร่
- ตำแหน่งไหนได้รับเงินเดือนสูงสุด
```

**English:**
```
- Show salary bands by job title
- What is the average salary for a Software Engineer?
- Which job title has the highest average salary?
```

### Top Earners

**Thai:**
```
- พนักงานที่ได้รับเงินเดือนสูงสุด 10 คน
- พนักงาน Contract ที่ได้รับเงินเดือนสูงสุด
- แสดงพนักงานที่เงินเดือนสูงกว่า 80,000 บาท
```

**English:**
```
- Top 10 highest paid employees
- Highest paid contract employees
- Show employees earning more than 80,000 THB
```

---

## 📅 Leave Management Queries

### Leave Summary

**Thai:**
```
- สรุปวันลาของพนักงานทุกคน
- พนักงานคนไหนลามากที่สุด
- แสดงวันลาพักร้อนที่ใช้ไปแล้วของแต่ละคน
- ใครมีคำขอลาค้างอนุมัติบ้าง
```

**English:**
```
- Show leave summary for all employees
- Who has taken the most leave days?
- Show annual leave used per employee
- Who has pending leave requests?
```

### Leave by Type

**Thai:**
```
- รวมวันลาป่วยทั้งหมดในแต่ละแผนก
- มีการลาคลอดกี่คน
- แสดงวันลาส่วนตัวที่อนุมัติแล้ว
- แผนกไหนมีวันลารวมมากที่สุด
```

**English:**
```
- Total sick days taken per department
- How many employees took maternity leave?
- Show approved personal leave requests
- Which department has the most total leave days?
```

### Pending & Rejected

**Thai:**
```
- แสดงคำขอลาที่ยังค้างอนุมัติ
- มีคำขอลาที่ถูกปฏิเสธกี่รายการ
- แสดงคำขอลาของพนักงานในแผนก Engineering
```

**English:**
```
- Show all pending leave requests
- How many leave requests were rejected?
- Show leave requests for Engineering employees
```

---

## ⭐ Performance Review Queries

### High Performers

**Thai:**
```
- แสดงรายชื่อพนักงาน high performer (rating ≥ 4.0)
- พนักงานที่มีคะแนน performance สูงสุด 5 คน
- แผนกไหนมี high performer มากที่สุด
- แสดงพนักงาน rating 5.0
```

**English:**
```
- Show high performers (rating ≥ 4.0)
- Top 5 employees by performance rating
- Which department has the most high performers?
- Show employees with a perfect 5.0 rating
```

### Performance by Department

**Thai:**
```
- คะแนน performance เฉลี่ยของแต่ละแผนก
- แผนกไหนมีผลการปฏิบัติงานดีที่สุด
- เปรียบเทียบ rating ระหว่าง Engineering กับ Sales
```

**English:**
```
- Average performance rating by department
- Which department has the best average performance?
- Compare ratings between Engineering and Sales
```

### Underperformers

**Thai:**
```
- แสดงพนักงานที่มีคะแนนต่ำกว่า 3.0
- พนักงานที่ต้องการการพัฒนามีกี่คน
```

**English:**
```
- Show employees with rating below 3.0
- How many employees need a performance improvement plan?
```

---

## 🔍 Complex Analytical Queries

### Combined Analysis

**Thai:**
```
- พนักงาน high performer ที่ได้รับเงินเดือนต่ำกว่าค่าเฉลี่ยของแผนก
- พนักงานที่ลามากและมีผลงานต่ำ
- แสดงพนักงานใหม่ที่เข้าทำงานในปี 2023
- พนักงาน Contract ที่มีผลงานดีควรพิจารณาเป็น Full-time
```

**English:**
```
- High performers earning below their department average
- Employees with high leave and low performance
- Show new hires who joined in 2023
- Contract employees with good performance worth converting to full-time
```

### Workforce Planning

**Thai:**
```
- แผนกไหนมีตำแหน่งว่างมากที่สุด
- คาดการณ์ค่าใช้จ่ายเงินเดือนถ้าเติมตำแหน่งว่างทั้งหมด
- พนักงานที่ทำงานมานานกว่า 5 ปีมีกี่คน
```

**English:**
```
- Which departments have the most open positions?
- Estimate salary cost if all open positions are filled
- How many employees have more than 5 years of tenure?
```

---

## 🎯 Specific Use Cases

### Daily HR Operations

**Thai:**
```
- คำขอลาที่รอการอนุมัติวันนี้
- พนักงานใหม่ที่เข้าทำงานเดือนนี้
- สรุปจำนวนพนักงานปัจจุบันทั้งหมด
```

**English:**
```
- Leave requests pending approval today
- New hires this month
- Current total employee count
```

### Management Reports

**Thai:**
```
- รายงานสรุป headcount รายแผนก
- รายงานค่าใช้จ่ายเงินเดือนรายเดือน
- รายงานผลการปฏิบัติงานรอบ 2024-H1
```

**English:**
```
- Headcount summary report by department
- Monthly payroll cost report
- Performance review summary for 2024-H1
```

---

## 💡 Tips for Effective Queries

### Best Practices

1. **Be Specific** — mention department names, employee IDs, or date ranges
2. **Use Follow-ups** — build on previous results (e.g. "now show only Engineering")
3. **Ask for Comparisons** — compare departments, job titles, or time periods
4. **Request Rankings** — "top 5", "bottom 3", "highest", "lowest"
5. **Ask for Insights** — "what should HR do about this?"

### Good Query Examples

```
- "Show salary band for all job titles in Engineering"
- "Which department has the most pending leave requests?"
- "Top 10 performers and their current salary"
- "Employees hired in 2023 with performance rating above 4.0"
```

### Avoid

- Too vague: "แสดงข้อมูลพนักงาน" (no filter or context)
- Too broad: Asking for all tables at once
- Ambiguous names: Use employee IDs (EMP001) or full names when possible

---

## 📝 Notes

- All queries support Thai and English
- Results are returned as Markdown tables
- Insights are auto-generated from the result set
- Follow-up questions are suggested after each response
- Maximum 1,000 rows per result

---

**Happy Querying! 🚀**
