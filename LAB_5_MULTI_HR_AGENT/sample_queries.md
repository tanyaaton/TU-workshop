# Business Operations Agent - Sample Test Queries

This document provides comprehensive test queries for the Business Operations Orchestrator Agent in both Thai and English.

---

## 📧 Email Communication (→ sendEmail tool)

These queries should use the **sendEmail tool** directly (not route to a sub-agent).

### Thai Queries
```
- ส่งอีเมลถึง supplier@example.com เรื่อง "สั่งซื้อสินค้า" ว่า "กรุณาจัดส่งสินค้า SKU001 จำนวน 100 ชิ้น"
- ส่งอีเมลหาทีมจัดซื้อที่ procurement@company.com หัวข้อ "ขอใบเสนอราคา" เนื้อหา "ต้องการใบเสนอราคาสินค้า"
- ส่งเมลถึง manager@company.com เรื่อง "รายงานสต็อก" บอกว่า "สินค้าใกล้หมดแล้ว"
```

### English Queries
```
- Send email to supplier@example.com subject "Order Request" body "Please deliver SKU001 quantity 100 units"
- Send email to procurement@company.com subject "Quote Request" body "Need quotation for products"
- Email manager@company.com subject "Stock Report" message "Low stock alert for multiple items"
```

**Note:** The sendEmail tool requires:
- `to`: Recipient email address
- `subject`: Email subject line
- `body`: Email message content

---

## 📋 Credit Control & Procurement Policies (→ general_agent)

These queries should be routed to the **general_agent** which has access to credit control and procurement policy documents via RAG.

### Thai Queries
```
- ระบบการควบคุมเครดิตคืออะไร
- เงื่อนไขการชำระเงินมีอะไรบ้าง
- วิธีการจัดการวงเงินเครดิตของลูกค้า
- ขั้นตอนการติดตามหนี้ค้างชำระ
- ขั้นตอนการสั่งซื้อสินค้าเป็นอย่างไร
- นโยบายการคัดเลือกผู้ขายมีอะไรบ้าง
- เอกสารที่ต้องใช้ในการจัดซื้อ
- กระบวนการอนุมัติใบสั่งซื้อ
- เกณฑ์การประเมินความเสี่ยงทางเครดิต
- มาตรการป้องกันหนี้สูญ
- การจัดการลูกค้าที่มีปัญหาการชำระเงิน
- นโยบายการให้ส่วนลดการค้า
- ระยะเวลาการชำระเงินมาตรฐาน
- ขั้นตอนการออกใบแจ้งหนี้และใบเสร็จรับเงิน
```

### English Queries
```
- What is the credit control system?
- What are the payment terms and conditions?
- How to manage customer credit limits?
- What is the debt collection procedure?
- What is the procurement process?
- What are the vendor selection policies?
- What documents are required for procurement?
- What is the purchase order approval process?
- What are the credit risk assessment criteria?
- What are the bad debt prevention measures?
- How to handle customers with payment issues?
- What is the trade discount policy?
- What is the standard payment period?
- What is the invoicing and receipt process?
```

---

## 📊 Inventory & Sales Analytics (→ inventory_analytics_agent)

These queries should be routed to the **inventory_analytics_agent** which performs Text-to-SQL queries on the SQLite inventory database.

### Stock Level Queries

**Thai:**
```
- แสดงสินค้าที่สต็อกต่ำกว่า reorder point
- สินค้าไหนใกล้หมดที่สาขา 1
- แสดงสินค้าที่ต้องสั่งซื้อเพิ่ม
- เช็คสต็อกของสาขา STORE001
- สินค้าไหนที่สต็อกต่ำกว่า 20 ชิ้น
- เช็คสินค้าที่ใกล้หมดทุกสาขา
- แสดงสต็อกของสินค้าในหมวด Beverages
```

**English:**
```
- Show products with stock below reorder point
- Which products are running low at store 1?
- Show products that need reordering
- Check stock at STORE001
- Which products have less than 20 units?
- Check low stock items across all stores
- Show stock for Beverages category
```

### Sales Analytics Queries

**Thai:**
```
- สินค้าขายดี 10 อันดับแรก
- แสดงยอดขายของแต่ละสินค้า
- สินค้าไหนขายได้มากที่สุดในเดือนนี้
- ยอดขายรวมทั้งหมด
- ยอดขายรวมของแต่ละหมวดสินค้า
- หมวดไหนขายดีที่สุด
- แสดงยอดขายของหมวด Beverages
- เปรียบเทียบยอดขายระหว่างหมวดสินค้า
- แสดงยอดขายของแต่ละสาขา
- สาขาไหนมียอดขายสูงสุด
- เปรียบเทียบยอดขายระหว่างสาขา
```

**English:**
```
- Top 10 best-selling products
- Show sales by product
- Which product sold the most this month?
- Total sales across all products
- Total sales by product category
- Which category sells the best?
- Show sales for Beverages category
- Compare sales between categories
- Show sales by store
- Which store has the highest sales?
- Compare sales between stores
```

### Product Information Queries

**Thai:**
```
- แสดงสินค้าทั้งหมดในหมวด Beverages
- ราคาขายของ Coca-Cola คือเท่าไหร่
- สินค้าไหนมีราคาแพงที่สุด
- แสดงข้อมูลสินค้า SKU001
- มีสินค้าอะไรบ้างในระบบ
- มีหมวดสินค้าอะไรบ้าง
- แสดงจำนวนสินค้าในแต่ละหมวด
```

**English:**
```
- Show all products in Beverages category
- What is the retail price of Coca-Cola?
- Which product is the most expensive?
- Show details for SKU001
- What products are in the system?
- What product categories exist?
- Show product count by category
```

### Financial Queries

**Thai:**
```
- สินค้าไหนมี profit margin สูงสุด
- คำนวณกำไรของแต่ละสินค้า
- คำนวณมูลค่าสต็อกรวมของแต่ละสาขา
- มูลค่าสต็อกทั้งหมดเท่าไหร่
- สาขาไหนมีมูลค่าสต็อกสูงสุด
```

**English:**
```
- Which products have the highest profit margin?
- Calculate profit for each product
- Calculate total inventory value by store
- What is the total inventory value?
- Which store has the highest inventory value?
```

---

## 🔍 Market Research & External Information (→ Tavily_Search_agent)

These queries should be routed to the **Tavily_Search_agent** which performs real-time web searches via MCP.

### Market Trends

**Thai:**
```
- แนวโน้มการค้าปลีกในประเทศไทยล่าสุด
- ตลาดเครื่องดื่มในประเทศไทยเป็นอย่างไร
- แนวโน้มการบริโภคสินค้าอุปโภคบริโภค
- ตลาดสินค้า FMCG ในเอเชียตะวันออกเฉียงใต้
```

**English:**
```
- Latest retail trends in Thailand
- What is the beverage market like in Thailand?
- Consumer goods consumption trends
- FMCG market in Southeast Asia
```

### Competitor Analysis

**Thai:**
```
- วิเคราะห์ราคาคู่แข่ง
- คู่แข่งหลักในตลาดค้าปลีกไทยมีใครบ้าง
- กลยุทธ์ของคู่แข่งในตลาด
```

**English:**
```
- Competitor pricing analysis
- Who are the main competitors in Thai retail market?
- Competitor strategies in the market
```

### General Knowledge & External Information

**Thai:**
```
- เมืองหลวงของประเทศไทยคืออะไร
- ช่วยลิสคำถามที่มักถูกถามตอนสัมภาษณ์งานหน่อย
- ข่าวเศรษฐกิจล่าสุด
- อัตราเงินเฟ้อปัจจุบัน
- GDP ของประเทศไทยปีนี้
```

**English:**
```
- What is the capital of Thailand?
- List of frequently asked interview questions
- Latest economic news
- Current inflation rate
- Thailand's GDP this year
```

### Industry News

**Thai:**
```
- ข่าวอุตสาหกรรมค้าปลีกล่าสุด
- มีอะไรใหม่ในวงการค้าปลีก
- เทคโนโลยีใหม่ในการจัดการสินค้าคงคลัง
```

**English:**
```
- Latest retail industry news
- What's new in retail?
- New technology in inventory management
```

---

## 🧪 Edge Cases & Routing Tests

### Ambiguous Queries (Test Routing Logic)

**Thai:**
```
- สินค้าขายดีและมีสต็อกต่ำ (Should route to inventory_analytics_agent - primary domain)
- นโยบายการสั่งซื้อสินค้า (Should route to general_agent - policies)
- แนวโน้มยอดขายในตลาด (Should route to Tavily_Search_agent - external trends)
```

**English:**
```
- Best-selling products with low stock (Should route to inventory_analytics_agent)
- Product ordering policy (Should route to general_agent)
- Sales trends in the market (Should route to Tavily_Search_agent)
```

### Multi-Domain Queries

**Thai:**
```
- เปรียบเทียบนโยบายเครดิตกับคู่แข่ง (Policies + External research)
- วิเคราะห์ยอดขายและแนวโน้มตลาด (Analytics + Market research)
```

**English:**
```
- Compare credit policy with competitors (Policies + External research)
- Analyze sales and market trends (Analytics + Market research)
```

---

## 📝 Testing Checklist

Use this checklist to verify the agent is working correctly:

### Routing Tests
- [ ] Credit control queries route to general_agent
- [ ] Procurement queries route to general_agent
- [ ] Stock level queries route to inventory_analytics_agent
- [ ] Sales analytics queries route to inventory_analytics_agent
- [ ] Market research queries route to Tavily_Search_agent
- [ ] General knowledge queries route to Tavily_Search_agent

### Language Tests
- [ ] Thai queries are understood and routed correctly
- [ ] English queries are understood and routed correctly
- [ ] Responses are in the same language as the query

### Functionality Tests
- [ ] Agent provides clear routing explanations
- [ ] Sub-agents return appropriate responses
- [ ] Data is formatted in Markdown tables
- [ ] Insights and recommendations are provided
- [ ] Follow-up questions are suggested

### Error Handling
- [ ] Handles queries outside domain gracefully
- [ ] Provides helpful error messages
- [ ] Suggests alternative queries when appropriate

---

## 💡 Tips for Effective Testing

1. **Start Simple**: Begin with clear, single-domain queries
2. **Test Each Sub-Agent**: Verify each sub-agent works independently
3. **Test Routing**: Ensure queries go to the correct sub-agent
4. **Test Bilingual**: Try both Thai and English versions
5. **Test Edge Cases**: Try ambiguous or multi-domain queries
6. **Check Responses**: Verify data accuracy and formatting
7. **Review Logs**: Check routing decisions in agent logs

---

## 🎯 Expected Behavior

### Successful Routing
When a query is successfully routed, you should see:
1. Brief acknowledgment of the query
2. Indication of which sub-agent is being used
3. Response from the sub-agent
4. Formatted data (tables, lists, etc.)
5. Insights or recommendations
6. Suggested follow-up questions

### Example Flow
```
User: "แสดงสินค้าที่สต็อกต่ำกว่า reorder point"

Agent: "ฉันจะตรวจสอบข้อมูลสินค้าคงคลังให้คุณ โดยใช้ระบบวิเคราะห์ข้อมูล..."

[Routes to inventory_analytics_agent]

[Returns formatted table with low stock items]

Agent: "พบสินค้า 15 รายการที่มีสต็อกต่ำกว่า reorder point 
แนะนำให้สั่งซื้อเพิ่มโดยเร็ว โดยเฉพาะ SKU018 (Popcorn) ที่ต้องเติม 25 หน่วย"
```

---

*Happy Testing! 🚀*