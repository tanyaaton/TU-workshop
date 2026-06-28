# Business Operations Agent - Routing Guide

This document explains the routing logic and decision-making process of the Business Operations Orchestrator Agent.

---

## 🎯 Routing Overview

The Business Operations Agent acts as a **central router** that:
- Routes information queries to specialized sub-agents
- Uses email tools directly for communication tasks

### Core Principle
**One Query → One Action**
- Information queries → Route to ONE sub-agent
- Email requests → Use sendEmail tool directly

---

## 🗺️ Routing Decision Tree

```
User Query
    │
    ├─ Action Type Analysis
    │  ├─ Send/Email → sendEmail tool (direct)
    │  └─ Information Query → Route to sub-agent
    │
    ├─ Keywords Analysis (for information queries)
    │  ├─ Policy/Procedure/Credit/Procurement → general_agent
    │  ├─ Stock/Inventory/Sales/Product → inventory_analytics_agent
    │  └─ Market/Trend/Competitor/News → Tavily_Search_agent
    │
    └─ Domain Analysis
       ├─ Communication → sendEmail tool
       ├─ Internal Policies → general_agent
       ├─ Data Analytics → inventory_analytics_agent
       └─ External Research → Tavily_Search_agent
```

---

## 📋 Sub-Agent Routing Map
### 0. sendEmail Tool (Direct Communication)

**Use directly for:**
- Sending email notifications
- Communicating alerts or reports
- Forwarding information to stakeholders
- Automated email responses

**Keywords (Thai):**
```
ส่ง, อีเมล, แจ้ง, แจ้งเตือน, ส่งข้อความ, ติดต่อ, 
รายงาน, แจ้งผล, แจ้งสถานะ
```

**Keywords (English):**
```
send, email, notify, alert, message, contact, 
report, inform, communicate, forward
```

**Required Parameters:**
- `to`: Recipient email address (required)
- `subject`: Email subject line (required)
- `body`: Email content/message (required)

**Routing Logic:**
```
IF query contains ["send", "email", "ส่งอีเมล", "แจ้ง", "notify"]
THEN use sendEmail tool directly
ELSE continue to sub-agent routing
```

**Example Queries:**
- "Send an email to manager@company.com about low stock items"
- "ส่งอีเมลแจ้งเตือนสินค้าใกล้หมดไปที่ inventory@company.com"
- "Email the sales report to team@company.com"
- "แจ้งผลการวิเคราะห์ไปที่ boss@company.com"

**Important Notes:**
- Email tool is used DIRECTLY by the orchestrator
- Does NOT route to a sub-agent
- Requires all three parameters (to, subject, body)
- Can be combined with data from sub-agents (e.g., get low stock data, then email it)

---


### 1. general_agent (Credit Control & Procurement Policies)

**Route queries about:**
- Credit control policies and procedures
- Payment terms and conditions
- Procurement processes and guidelines
- Vendor/supplier management
- Purchase order workflows
- Credit risk assessment
- Collection procedures
- Trade discounts and payment periods

**Keywords (Thai):**
```
นโยบาย, ขั้นตอน, เครดิต, การจัดซื้อ, ซัพพลายเออร์, ผู้ขาย, 
การชำระเงิน, ใบสั่งซื้อ, การอนุมัติ, เงื่อนไข, ระเบียบ, 
การควบคุม, หนี้, การเก็บเงิน, ส่วนลด
```

**Keywords (English):**
```
policy, procedure, credit, procurement, supplier, vendor, 
payment, purchase order, approval, terms, regulation, 
control, debt, collection, discount
```

**Example Queries:**
- "ระบบการควบคุมเครดิตคืออะไร"
- "What are the payment terms?"
- "ขั้นตอนการสั่งซื้อสินค้า"
- "Vendor selection criteria"

---

### 2. inventory_analytics_agent (Inventory & Sales Analytics)

**Route queries about:**
- Stock levels and availability
- Inventory management
- Sales data and analysis
- Product information
- Store comparisons
- Profit margins
- Inventory value calculations
- Reorder recommendations
- Product categories
- Transaction history

**Keywords (Thai):**
```
สต็อก, สินค้า, ยอดขาย, คงคลัง, สาขา, ร้าน, ขาย, 
ราคา, กำไร, มูลค่า, จำนวน, เหลือ, ใกล้หมด, 
reorder point, SKU, หมวด, ประเภท
```

**Keywords (English):**
```
stock, inventory, sales, product, store, branch, sold, 
price, profit, value, quantity, remaining, low stock, 
reorder point, SKU, category, analytics
```

**Example Queries:**
- "แสดงสินค้าที่สต็อกต่ำกว่า reorder point"
- "Top 10 best-selling products"
- "Compare sales between stores"
- "Calculate inventory value"

---

### 3. Tavily_Search_agent (External Information & Market Research)

**Route queries about:**
- Market trends and analysis
- Competitor information
- Industry news and updates
- External business intelligence
- General knowledge
- Current events
- World facts
- Interview questions
- Economic indicators

**Keywords (Thai):**
```
ตลาด, แนวโน้ม, คู่แข่ง, ข่าว, วิเคราะห์, ภายนอก, 
ทั่วไป, เมืองหลวง, ประธานาธิบดี, สัมภาษณ์, 
เศรษฐกิจ, อุตสาหกรรม, ทั่วโลก
```

**Keywords (English):**
```
market, trend, competitor, news, analysis, external, 
general, capital, president, interview, economy, 
industry, global, world
```

**Example Queries:**
- "Latest retail trends in Thailand"
- "Competitor pricing analysis"
- "เมืองหลวงของประเทศไทย"
- "List of interview questions"

---

## 🔍 Routing Decision Logic

### Step 1: Action Type Detection
First, determine if this is a communication action or information query:
- Contains "send", "email", "ส่งอีเมล", "แจ้ง" → Use sendEmail tool directly
- Otherwise → Continue to sub-agent routing

### Step 2: Keyword Matching
For information queries, analyze keywords to identify the primary domain:
- Policy/procedure keywords → general_agent
- Inventory/sales keywords → inventory_analytics_agent
- Market/trend keywords → Tavily_Search_agent

### Step 3: Context Analysis
If keywords are ambiguous, consider the broader context:
- Is this about internal operations or external information?
- Does this require database queries or web search?
- Is this about policies/procedures or data analytics?

### Step 4: Primary Domain Selection
For queries spanning multiple domains, route to the PRIMARY domain:
- "สินค้าขายดีและมีสต็อกต่ำ" → inventory_analytics_agent (primary: analytics)
- "นโยบายการสั่งซื้อสินค้า" → general_agent (primary: policy)
- "แนวโน้มยอดขายในตลาด" → Tavily_Search_agent (primary: external trends)

### Step 5: Fallback Logic
If the query doesn't clearly match any domain:
1. Check if it's a general knowledge question → Tavily_Search_agent
2. Check if it mentions specific products/stores → inventory_analytics_agent
3. Default to general_agent for policy-related ambiguity

---

## 📊 Routing Examples

### Clear Routing Cases

| Query | Route To | Reason |
|-------|----------|--------|
| "Send email to manager@company.com" | sendEmail tool | Communication action |
| "ส่งอีเมลแจ้งสต็อกต่ำ" | sendEmail tool | Email notification |
| "ระบบการควบคุมเครดิตคืออะไร" | general_agent | Policy question |
| "แสดงสินค้าที่สต็อกต่ำ" | inventory_analytics_agent | Stock query |
| "แนวโน้มการค้าปลีก" | Tavily_Search_agent | Market trends |
| "What are payment terms?" | general_agent | Policy question |
| "Top 10 best-selling products" | inventory_analytics_agent | Sales analytics |
| "Latest economic news" | Tavily_Search_agent | External news |

### Ambiguous Cases

| Query | Route To | Reasoning |
|-------|----------|-----------|
| "สินค้าขายดีและมีสต็อกต่ำ" | inventory_analytics_agent | Primary domain is analytics (can query both) |
| "นโยบายการสั่งซื้อสินค้า" | general_agent | Primary domain is policy |
| "วิเคราะห์ยอดขายและแนวโน้มตลาด" | inventory_analytics_agent first | Start with internal data, then suggest external research |
| "เปรียบเทียบนโยบายกับคู่แข่ง" | general_agent first | Start with internal policy, then suggest competitor research |

---

## 🎨 Routing Best Practices

### For the Agent

1. **Be Explicit**: Clearly state which sub-agent is being used
2. **Explain Why**: Briefly explain the routing decision
3. **Set Expectations**: Tell the user what kind of response to expect
4. **Suggest Alternatives**: If query is ambiguous, suggest clarification

### Example Good Routing Response:
```
"ฉันจะตรวจสอบข้อมูลสินค้าคงคลังให้คุณ โดยใช้ระบบวิเคราะห์ข้อมูล 
(inventory_analytics_agent) ซึ่งจะค้นหาสินค้าที่มีสต็อกต่ำกว่า reorder point..."
```

### For Users

1. **Be Specific**: Include relevant details (store ID, product name, category)
2. **Use Clear Language**: Avoid overly complex or multi-part questions
3. **One Topic**: Focus on one domain per query
4. **Follow Up**: Ask related questions to explore deeper

---

## 🚫 What NOT to Route

The Business Operations Agent should NOT handle:
- Queries outside the four capabilities (policies, analytics, research, email)
- HR-specific queries (use HR agent instead)
- Customer service queries (use customer service agent instead)
- Queries requiring real-time transaction processing
- Queries requiring authentication or sensitive data access
- File uploads or downloads
- Calendar management or scheduling

For these cases, the agent should:
1. Politely explain it's outside its scope
2. Suggest the appropriate resource or agent
3. Offer to help with related queries within its domain

**Note:** Email functionality IS supported via the sendEmail tool.

---

## 🔄 Multi-Turn Conversations

### Context Preservation
The agent should maintain context across turns:
- Remember which sub-agent was used
- Allow follow-up questions to the same sub-agent
- Switch sub-agents when the topic changes

### Example Flow:
```
User: "แสดงสินค้าที่สต็อกต่ำ"
Agent: [Routes to inventory_analytics_agent] → Shows low stock items

User: "สาขาไหนมีปัญหามากที่สุด"
Agent: [Continues with inventory_analytics_agent] → Analyzes by store

User: "นโยบายการสั่งซื้อเพิ่มเป็นอย่างไร"
Agent: [Switches to general_agent] → Explains procurement policy
```

---

## 📈 Routing Performance Metrics

### Success Indicators
- ✅ Query routed to correct sub-agent
- ✅ User receives relevant response
- ✅ No need for re-routing
- ✅ Follow-up questions handled smoothly

### Failure Indicators
- ❌ Wrong sub-agent selected
- ❌ User needs to rephrase query
- ❌ Response doesn't match query intent
- ❌ Multiple routing attempts needed

---

## 🛠️ Troubleshooting Routing Issues

### Issue: Wrong Sub-Agent Selected

**Symptoms:**
- Response doesn't match query
- Sub-agent returns "no data found"
- User confused by response

**Solutions:**
1. Review query keywords
2. Check routing logic in agent instructions
3. Add more specific keywords to routing map
4. Update agent behavior with clearer rules

### Issue: Ambiguous Queries

**Symptoms:**
- Agent hesitates or asks for clarification
- Multiple sub-agents seem appropriate
- User frustrated with routing

**Solutions:**
1. Improve primary domain detection
2. Add examples of ambiguous cases to instructions
3. Train agent to ask clarifying questions
4. Provide routing hints in welcome message

### Issue: Sub-Agent Not Responding

**Symptoms:**
- Routing successful but no response
- Error messages from sub-agent
- Timeout errors

**Solutions:**
1. Verify sub-agent is deployed and active
2. Check sub-agent credentials and connections
3. Test sub-agent independently
4. Review sub-agent logs for errors

---

## 📝 Routing Checklist

Before deploying, verify:

- [ ] All three sub-agents are deployed and active
- [ ] sendEmail tool is configured and accessible
- [ ] Agent IDs in YAML match actual deployed agents
- [ ] Email API endpoint is correct in OpenAPI spec
- [ ] Routing keywords cover common query patterns
- [ ] Email keywords trigger direct tool usage
- [ ] Ambiguous cases have clear routing rules
- [ ] Agent provides clear routing explanations
- [ ] Bilingual routing works (Thai and English)
- [ ] Follow-up questions maintain context
- [ ] Error handling is graceful
- [ ] Routing logs are accessible for debugging

---

## 🎓 Advanced Routing Scenarios

### Scenario 1: Data Retrieval + Email
Combine sub-agent data with email tool:
1. Query data from sub-agent (e.g., inventory_analytics_agent)
2. Format the results
3. Use sendEmail tool to send the report

**Example:** "Get low stock items and email the list to manager@company.com"
- Step 1: Route to inventory_analytics_agent for low stock data
- Step 2: Use sendEmail tool with the results

### Scenario 2: Sequential Routing
Some queries may benefit from sequential routing:
1. Query internal data first (inventory_analytics_agent)
2. Then query external trends (Tavily_Search_agent)
3. Finally check policies (general_agent)

**Example:** "Analyze our sales performance compared to market trends"

### Scenario 3: Parallel Information
For comprehensive answers, suggest parallel queries:
- "Check our stock levels" (inventory_analytics_agent)
- "AND review reorder policy" (general_agent)

### Scenario 4: Conditional Routing
Route based on query results:
- IF low stock found → Suggest checking procurement policy OR sending email alert
- IF high sales found → Suggest market trend analysis
- IF policy unclear → Suggest specific examples from data

---

## 🚀 Future Enhancements

Potential routing improvements:
1. **Machine Learning**: Learn from routing decisions and user feedback
2. **Confidence Scores**: Show routing confidence level
3. **Multi-Agent Responses**: Combine responses from multiple agents
4. **Smart Suggestions**: Proactively suggest related queries
5. **Routing Analytics**: Track routing patterns and optimize

---

*This routing guide ensures consistent, accurate, and efficient query handling across all business operations domains.*