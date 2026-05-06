# LAB 5 — Business Operations Multi-Agent

A centralized orchestrator that routes business queries to specialized agents and tools.

## What It Does

Routes your questions to the right place:
- **Policies & Procedures** → general_agent (LAB 1)
- **Inventory & Sales Data** → inventory_analytics_agent (LAB 4)  
- **Market Research** → Tavily_Search_agent (LAB 2)
- **Send Emails** → Email API tool (LAB 3)

## Quick Start

### Prerequisites
Complete these labs first:
- LAB 1 (Policies)
- LAB 2 (Search)
- LAB 3 (Email - optional)
- LAB 4 (Analytics)

### Import the Agent

**Option 1: Automated**
```bash
cd TH-wxo-askHR-enablement-workshop/LAB_5_MULTI_HR_AGENT
./import_all.sh
```

**Option 2: Manual**
```bash
# 1. Get your agent IDs
orchestrate agents list

# 2. Update agent/Business_Operations_Agent.yaml with your IDs

# 3. Import
orchestrate agents import -f agent/Business_Operations_Agent.yaml
```

### Add Email Tool (Optional)

1. Go to Watson Orchestrate UI → Toolset
2. Click **Add tool** → **OpenAPI**
3. Upload: `../LAB_3_API_EMAIL/openapi_sendemail.json`
4. In your agent, go to Toolset section
5. Add the `sendEmail` tool

---

## Test Queries

### Policies (→ general_agent)
```
Thai:
- ระบบการควบคุมเครดิตคืออะไร
- ขั้นตอนการสั่งซื้อสินค้า

English:
- What is the credit control system?
- What is the procurement process?
```

### Analytics (→ inventory_analytics_agent)
```
Thai:
- แสดงสินค้าที่สต็อกต่ำกว่า reorder point
- สินค้าขายดี 10 อันดับแรก

English:
- Show products with stock below reorder point
- Top 10 best-selling products
```

### Research (→ Tavily_Search_agent)
```
Thai:
- แนวโน้มการค้าปลีกในประเทศไทย
- วิเคราะห์ราคาคู่แข่ง

English:
- Latest retail trends in Thailand
- Competitor pricing analysis
```

### Email (→ sendEmail tool)
```
Thai:
- ส่งอีเมลถึง supplier@example.com เรื่อง "สั่งซื้อสินค้า" ว่า "กรุณาจัดส่งสินค้า SKU001"

English:
- Send email to supplier@example.com subject "Order Request" body "Please deliver SKU001"
```

---

## Architecture

```
User Query
    ↓
Business Operations Agent (Router)
    ↓
    ├─→ general_agent (Policies)
    ├─→ inventory_analytics_agent (Data)
    ├─→ Tavily_Search_agent (Research)
    └─→ sendEmail tool (Communication)
```

---

## Configuration

### Update Agent IDs

Edit `agent/Business_Operations_Agent.yaml`:

```yaml
collaborators:
- general_agent                    # Your LAB 1 agent ID
- inventory_analytics_agent        # Your LAB 4 agent ID  
- Tavily_Search_agent_XXXXX       # Your LAB 2 agent ID (replace XXXXX)
```

### Add Email Tool

In the YAML, add to the `tools` section:
```yaml
tools:
- sendEmail  # After importing from LAB 3 OpenAPI
```

Or add via UI:
1. Open agent in Watson Orchestrate
2. Go to **Toolset** section
3. Click **Add tool**
4. Select `sendEmail`

---

## Troubleshooting

**Agent not found**
- Run `orchestrate agents list` to get correct IDs
- Update YAML with actual IDs

**Wrong routing**
- Check query keywords
- See `ROUTING_GUIDE.md` for details

**Email not working**
- Ensure LAB 3 OpenAPI is imported
- Add `sendEmail` tool to agent
- Check email API is running

**Import fails**
- Verify YAML syntax
- Check orchestrate CLI is authenticated
- Ensure all prerequisite agents exist

---

## Files

- `README.md` - This file
- `agent/Business_Operations_Agent.yaml` - Agent configuration
- `sample_queries.md` - Comprehensive test queries
- `ROUTING_GUIDE.md` - Detailed routing logic
- `import_all.sh` - Automated import script

---

## Next Steps

1. Import the agent
2. Test with sample queries
3. Add email tool (optional)
4. Review routing in logs
5. Customize for your needs

---

*For detailed documentation, see `ROUTING_GUIDE.md` and `sample_queries.md`*