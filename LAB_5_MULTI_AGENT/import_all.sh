#!/bin/bash

# Import script for LAB 5: Business Operations Multi-Agent
# This script imports the Business Operations Orchestrator agent to Watson Orchestrate

echo "========================================="
echo "LAB 5: Business Operations Agent Import"
echo "Multi-Agent Orchestrator"
echo "========================================="
echo ""

# Check if orchestrate CLI is available
if ! command -v orchestrate &> /dev/null; then
    echo "❌ Error: 'orchestrate' CLI not found"
    echo "Please install Watson Orchestrate CLI first"
    echo "Run: pip install ibm-watsonx-orchestrate"
    exit 1
fi

echo "✅ Watson Orchestrate CLI found"
echo ""

# Check if environment is activated
echo "Checking Watson Orchestrate environment..."
ENV_STATUS=$(orchestrate env list 2>&1)

if echo "$ENV_STATUS" | grep -q "No environments configured"; then
    echo "❌ Error: No Watson Orchestrate environment configured"
    echo ""
    echo "Please configure your environment first:"
    echo "  orchestrate env add -n <env_name> -u <YOUR_URL>"
    echo "  orchestrate env activate <env_name> --api-key <YOUR_API_KEY>"
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Confirm before proceeding
echo "========================================="
echo "Ready to Import"
echo "========================================="
echo ""
echo "This script will import:"
echo "  - Business Operations Orchestrator Agent"
echo "  - Routes queries to 3 specialized sub-agents"
echo "  - Supports bilingual queries (Thai/English)"
echo ""
echo "Agent file: agent/Business_Operations_Agent.yaml"
echo ""
read -p "Do you want to continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Import cancelled"
    exit 0
fi

echo ""
echo "========================================="
echo "Importing Business Operations Agent"
echo "========================================="
echo ""

# Check if agent file exists
if [ ! -f "agent/Business_Operations_Agent.yaml" ]; then
    echo "❌ Error: agent/Business_Operations_Agent.yaml not found"
    echo "Please ensure you are in the LAB_5_MULTI_HR_AGENT directory"
    exit 1
fi

echo "✅ Agent configuration file found"
echo ""

# Display agent IDs for reference
echo "Current agent IDs in your environment:"
echo "--------------------------------------"
orchestrate agents list | grep -E "(general_agent|inventory_analytics_agent|Tavily_Search_agent)" || echo "No matching agents found"
echo ""
echo "⚠️  Important: Ensure the 'collaborators' section in the YAML file"
echo "    matches the actual agent IDs shown above."
echo ""
read -p "Press Enter to continue with import..."
echo ""

# Import the agent
echo "Importing agent..."
orchestrate agents import -f agent/Business_Operations_Agent.yaml

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "Import Complete!"
    echo "========================================="
    echo ""
    echo "✅ Business Operations Agent imported successfully"
    echo ""
    echo "Next steps:"
    echo "  1. Verify the agent in Watson Orchestrate UI"
    echo "  2. Test with sample queries from sample_queries.md"
    echo "  3. Review routing logs to ensure correct sub-agent selection"
    echo ""
    echo "Sample test queries:"
    echo "  Thai:"
    echo "    - แสดงสินค้าที่สต็อกต่ำกว่า reorder point"
    echo "    - ระบบการควบคุมเครดิตคืออะไร"
    echo "    - แนวโน้มการค้าปลีกในประเทศไทยล่าสุด"
    echo ""
    echo "  English:"
    echo "    - Show products with stock below reorder point"
    echo "    - What is the credit control system?"
    echo "    - Latest retail trends in Thailand"
    echo ""
    echo "For more test queries, see: sample_queries.md"
    echo ""
    echo "Happy orchestrating! 🚀"
else
    echo ""
    echo "========================================="
    echo "Import Failed"
    echo "========================================="
    echo ""
    echo "❌ Agent import failed"
    echo ""
    echo "Common issues:"
    echo "  1. YAML syntax errors - Check the file format"
    echo "  2. Invalid agent IDs in collaborators section"
    echo "  3. Authentication issues - Re-activate your environment"
    echo "  4. Network connectivity problems"
    echo ""
    echo "Troubleshooting steps:"
    echo "  1. Verify YAML syntax: cat agent/Business_Operations_Agent.yaml"
    echo "  2. Check agent IDs: orchestrate agents list"
    echo "  3. Update collaborators in YAML with correct IDs"
    echo "  4. Re-authenticate: orchestrate env activate <env_name>"
    echo ""
    echo "For detailed troubleshooting, see README.md"
    exit 1
fi

# Made with Bob