# Lab 1: Knowledge Base - Credit Control & Procurement System

This lab demonstrates how to import a knowledge base agent with built-in Milvus vector database for procurement and business operations policy documents.

### Prerequisites
- Complete Lab_0 (setup the lab environment).
- Have the `orchestrate` CLI installed and configured.
- Complete LAB_0 to activate orchestrate environment. If not, run the following command:

```bash
orchestrate env list
orchestrate env activate trial-env -a <YOUR_API_KEY>
```

## Overview

This lab uses the ADK (Agent Development Kit) to create and configure a **Procurement & Credit Control Assistant**. This agent allows users to chat and ask questions about credit control policies, procurement procedures, and business operations guidelines stored in a knowledge base within watsonx Orchestrate's embedded vector database.

The agent is designed to help procurement and business operations teams quickly access information about:
- Credit control policies and procedures
- Payment terms and conditions
- Vendor management guidelines
- Purchase order processes
- Credit limit management
- Collection procedures
- Risk assessment criteria

---

## Installation

Run the following commands to import the knowledge base and agent:

```bash
orchestrate knowledge-bases import -f policy/general_knowledge_base.yaml
orchestrate agents import -f agents/general_agent.yaml
```

Or use the convenience script:
```bash
bash import_all.sh
```

---

## Testing Knowledge Base Queries

You can test the agent with the following sample questions related to procurement and credit control:

### Credit Control & Payment Terms
- ระบบการควบคุมเครดิตคืออะไร
- เงื่อนไขการชำระเงินมีอะไรบ้าง
- วิธีการจัดการวงเงินเครดิตของลูกค้า
- ขั้นตอนการติดตามหนี้ค้างชำระ

### Procurement & Vendor Management
- ขั้นตอนการสั่งซื้อสินค้าเป็นอย่างไร
- นโยบายการคัดเลือกผู้ขายมีอะไรบ้าง
- เอกสารที่ต้องใช้ในการจัดซื้อ
- กระบวนการอนุมัติใบสั่งซื้อ

### Risk Management
- เกณฑ์การประเมินความเสี่ยงทางเครดิต
- มาตรการป้องกันหนี้สูญ
- การจัดการลูกค้าที่มีปัญหาการชำระเงิน

### General Business Operations
- นโยบายการให้ส่วนลดการค้า
- ระยะเวลาการชำระเงินมาตรฐาน
- ขั้นตอนการออกใบแจ้งหนี้และใบเสร็จรับเงิน