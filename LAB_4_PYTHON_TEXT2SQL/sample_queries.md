# Sample Queries for Inventory Analytics Agent

This document provides comprehensive test queries for the Inventory Analytics Agent in both Thai and English.

**Note:** The agent converts these natural language queries into SQL queries that run against the SQLite database.

---

## 📊 Stock Level Queries

### Basic Stock Checks

**Thai:**
```
- แสดงสต็อกทั้งหมด
- เช็คสต็อกของสาขา STORE001
- สินค้าไหนมีสต็อกเหลือน้อย
- แสดงสต็อกของสินค้าในหมวด Beverages
```

**English:**
```
- Show all inventory
- Check stock at STORE001
- Which products have low stock?
- Show stock for Beverages category
```

### Low Stock Alerts

**Thai:**
```
- แสดงสินค้าที่มีสต็อกต่ำกว่า reorder point
- สินค้าไหนใกล้หมดที่สาขา 1
- แสดงสินค้าที่ต้องสั่งซื้อเพิ่ม
- สินค้าไหนที่สต็อกต่ำกว่า 20 ชิ้น
- เช็คสินค้าที่ใกล้หมดทุกสาขา
```

**English:**
```
- Show products with stock below reorder point
- Which products are running low at store 1?
- Show products that need reordering
- Which products have less than 20 units?
- Check low stock items across all stores
```

### Stock by Location

**Thai:**
```
- เปรียบเทียบสต็อกระหว่างสาขา 1 และสาขา 2
- สาขาไหนมีสินค้าใกล้หมดมากที่สุด
- แสดงสต็อกของ Coca-Cola ทุกสาขา
- สาขาไหนมีสต็อกมากที่สุด
```

**English:**
```
- Compare stock between store 1 and store 2
- Which store has the most low-stock items?
- Show Coca-Cola stock across all stores
- Which store has the highest inventory?
```

---

## 💰 Sales Analytics Queries

### Sales Performance

**Thai:**
```
- สินค้าขายดี 10 อันดับแรก
- แสดงยอดขายของแต่ละสินค้า
- สินค้าไหนขายได้มากที่สุดในเดือนนี้
- ยอดขายรวมทั้งหมด
- สินค้าไหนขายได้น้อยที่สุด
```

**English:**
```
- Top 10 best-selling products
- Show sales by product
- Which product sold the most this month?
- Total sales across all products
- Which products have the lowest sales?
```

### Sales by Category

**Thai:**
```
- ยอดขายรวมของแต่ละหมวดสินค้า
- หมวดไหนขายดีที่สุด
- แสดงยอดขายของหมวด Beverages
- เปรียบเทียบยอดขายระหว่างหมวดสินค้า
```

**English:**
```
- Total sales by product category
- Which category sells the best?
- Show sales for Beverages category
- Compare sales between categories
```

### Sales by Store

**Thai:**
```
- แสดงยอดขายของแต่ละสาขา
- สาขาไหนมียอดขายสูงสุด
- เปรียบเทียบยอดขายระหว่างสาขา
- ยอดขายของสาขา STORE001
```

**English:**
```
- Show sales by store
- Which store has the highest sales?
- Compare sales between stores
- Sales at STORE001
```

---

## 📦 Product Information Queries

### Product Details

**Thai:**
```
- แสดงสินค้าทั้งหมดในหมวด Beverages
- ราคาขายของ Coca-Cola คือเท่าไหร่
- สินค้าไหนมีราคาแพงที่สุด
- แสดงข้อมูลสินค้า SKU001
- มีสินค้าอะไรบ้างในระบบ
```

**English:**
```
- Show all products in Beverages category
- What is the retail price of Coca-Cola?
- Which product is the most expensive?
- Show details for SKU001
- What products are in the system?
```

### Product Categories

**Thai:**
```
- มีหมวดสินค้าอะไรบ้าง
- แสดงจำนวนสินค้าในแต่ละหมวด
- หมวดไหนมีสินค้ามากที่สุด
- แสดงสินค้าทั้งหมดในหมวด Dairy
```

**English:**
```
- What product categories exist?
- Show product count by category
- Which category has the most products?
- Show all products in Dairy category
```

---

## 🏪 Supplier Queries

### Supplier Information

**Thai:**
```
- แสดงสินค้าทั้งหมดจากซัพพลายเออร์ Thai Beverage
- ซัพพลายเออร์ไหนมีสินค้ามากที่สุด
- มีซัพพลายเออร์อะไรบ้าง
- แสดงข้อมูลซัพพลายเออร์ของ Coca-Cola
```

**English:**
```
- Show all products from Thai Beverage supplier
- Which supplier has the most products?
- What suppliers are in the system?
- Show supplier information for Coca-Cola
```

---

## 💵 Financial Queries

### Profit Analysis

**Thai:**
```
- สินค้าไหนมี profit margin สูงสุด
- คำนวณกำไรของแต่ละสินค้า
- แสดงสินค้าที่มีกำไรต่ำที่สุด
- คำนวณ profit margin ของหมวด Beverages
```

**English:**
```
- Which products have the highest profit margin?
- Calculate profit for each product
- Show products with lowest profit
- Calculate profit margin for Beverages category
```

### Inventory Value

**Thai:**
```
- คำนวณมูลค่าสต็อกรวมของแต่ละสาขา
- มูลค่าสต็อกทั้งหมดเท่าไหร่
- สาขาไหนมีมูลค่าสต็อกสูงสุด
- คำนวณมูลค่าสต็อกของหมวด Dairy
```

**English:**
```
- Calculate total inventory value by store
- What is the total inventory value?
- Which store has the highest inventory value?
- Calculate inventory value for Dairy category
```

---

## 📈 Trend Analysis Queries

### Transaction History

**Thai:**
```
- แสดงธุรกรรมทั้งหมดของ SKU001
- มีการรับสินค้าเมื่อไหร่บ้าง
- แสดงการขายในช่วง 7 วันที่ผ่านมา
- สินค้าไหนที่ไม่มีการขายเลย
```

**English:**
```
- Show all transactions for SKU001
- When were products received?
- Show sales in the last 7 days
- Which products have no sales?
```

### Performance Trends

**Thai:**
```
- แสดงแนวโน้มการขายของแต่ละหมวด
- สินค้าไหนที่ยอดขายเพิ่มขึ้น
- เปรียบเทียบยอดขายเดือนนี้กับเดือนที่แล้ว
```

**English:**
```
- Show sales trends by category
- Which products have increasing sales?
- Compare this month's sales to last month
```

---

## 🔍 Complex Analytical Queries

### Multi-Criteria Analysis

**Thai:**
```
- แสดงสินค้าที่ขายดีแต่สต็อกต่ำ
- หาสินค้าที่มี profit margin สูงและขายดี
- สินค้าไหนที่มีสต็อกเกินความจำเป็น
- แสดงสินค้าที่ควรหยุดสั่งซื้อ
```

**English:**
```
- Show products with high sales but low stock
- Find products with high profit margin and good sales
- Which products have excess inventory?
- Show products that should stop ordering
```

### Store Performance

**Thai:**
```
- สาขาไหนมีประสิทธิภาพดีที่สุด
- เปรียบเทียบการจัดการสต็อกระหว่างสาขา
- สาขาไหนมีปัญหาสินค้าขาดบ่อย
```

**English:**
```
- Which store performs the best?
- Compare inventory management between stores
- Which store has frequent stockouts?
```

### Optimization Recommendations

**Thai:**
```
- แนะนำสินค้าที่ควรสั่งซื้อเพิ่ม
- สินค้าไหนที่ควรลดการสั่งซื้อ
- แนะนำการปรับ reorder point
- สินค้าไหนที่ควรโปรโมท
```

**English:**
```
- Recommend products to order more
- Which products should reduce ordering?
- Suggest reorder point adjustments
- Which products should be promoted?
```

---

## 🎯 Specific Use Cases

### Daily Operations

**Thai:**
```
- รายงานสต็อกประจำวัน
- สินค้าไหนต้องสั่งซื้อวันนี้
- เช็คสินค้าที่หมดอายุใกล้
- แสดงสินค้าที่ต้องตรวจนับ
```

**English:**
```
- Daily stock report
- What needs to be ordered today?
- Check products near expiration
- Show products needing inventory count
```

### Management Reports

**Thai:**
```
- สรุปยอดขายรายสัปดาห์
- รายงานประสิทธิภาพสาขา
- วิเคราะห์ความต้องการสินค้า
- แสดงสินค้าที่มีปัญหา
```

**English:**
```
- Weekly sales summary
- Store performance report
- Analyze product demand
- Show problematic products
```

### Strategic Planning

**Thai:**
```
- วิเคราะห์ portfolio สินค้า
- แนะนำสินค้าใหม่ที่ควรเพิ่ม
- ประเมินความเสี่ยงของสต็อก
- วางแผนการสั่งซื้อไตรมาสหน้า
```

**English:**
```
- Analyze product portfolio
- Recommend new products to add
- Assess inventory risk
- Plan next quarter's ordering
```

---

## 🧪 Testing Scenarios

### Edge Cases

**Thai:**
```
- แสดงสินค้าที่ไม่มีข้อมูล
- เช็คสินค้าที่มีข้อมูลผิดปกติ
- หาสินค้าที่มีสต็อกติดลบ
```

**English:**
```
- Show products with missing data
- Check products with anomalies
- Find products with negative stock
```

### Error Handling

**Thai:**
```
- แสดงข้อมูลสินค้าที่ไม่มีอยู่จริง
- เช็คสาขาที่ไม่มีในระบบ
- หาหมวดสินค้าที่ไม่ถูกต้อง
```

**English:**
```
- Show data for non-existent product
- Check non-existent store
- Find invalid product category
```

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

## 📝 Notes

- All queries support both Thai and English
- Results are formatted as Markdown tables
- Insights are automatically generated
- Follow-up questions are suggested
- Query timeout is 30 seconds
- Maximum 1000 rows per result

---

**Happy Querying! 🚀**