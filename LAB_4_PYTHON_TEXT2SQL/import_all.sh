#!/bin/bash

# Import script for LAB 6: Inventory Analytics Agent (SQLite Version)
# This script imports the Python tool and agent configuration to Watson Orchestrate

echo "========================================="
echo "LAB 6: Inventory Analytics Agent Import"
echo "Text-to-SQL with SQLite Database"
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

# Check if database exists
if [ ! -f "database/inventory.db" ]; then
    echo "⚠️  Database not found. Creating database..."
    cd database
    python3 create_database.py
    cd ..
    echo ""
fi

echo "✅ Database ready: database/inventory.db"
echo ""

# Confirm before proceeding
echo "This script will import:"
echo "  1. Python Tool: inventory_query_tool (Text-to-SQL)"
echo "  2. Agent: inventory_analytics_agent"
echo "  3. Database: inventory.db (SQLite)"
echo ""
read -p "Do you want to continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Import cancelled"
    exit 0
fi

echo ""
echo "========================================="
echo "Step 1: Installing Dependencies"
echo "========================================="
echo ""

# Install Python dependencies
echo "Installing Watson Orchestrate SDK and dependencies..."
cd tools
pip install -r requirements.txt
cd ..

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  Dependency installation may have failed"
    echo "Please run: pip install -r tools/requirements.txt"
fi

echo ""
echo "========================================="
echo "Step 2: Preparing Tool Package"
echo "========================================="
echo ""

# Copy database to tools directory for package upload
echo "Copying database to tools directory..."
cp database/inventory.db tools/

if [ $? -eq 0 ]; then
    echo "✅ Database copied to tools/"
else
    echo "❌ Error: Failed to copy database"
    exit 1
fi

echo ""
echo "========================================="
echo "Step 3: Importing Python Tool with Database"
echo "========================================="
echo ""

# Check if tool file exists
if [ ! -f "tools/inventory_query_tool.py" ]; then
    echo "❌ Error: tools/inventory_query_tool.py not found"
    exit 1
fi

echo "✅ Python tool found (with @tool decorator)"
echo "✅ Database package ready"
echo ""
echo "Importing tool with package root (includes database)..."

# Import the Python tool with package root
orchestrate tools import --kind python -f tools/inventory_query_tool.py --package-root tools/

if [ $? -eq 0 ]; then
    echo "✅ Tool and database imported successfully as package"
else
    echo "⚠️  Tool import may have failed"
    echo ""
    echo "Alternative: Manual UI Import"
    echo "  1. Go to Toolset → Add Tool → Python"
    echo "  2. Upload: tools/inventory_query_tool.py"
    echo "  3. Select 'Package Root': tools/"
    echo "  4. This will upload inventory.db automatically"
fi

echo ""
echo "========================================="
echo "Step 4: Importing Agent"
echo "========================================="
echo ""

# Import agent
echo "Importing inventory_analytics_agent..."

if [ -f "agent/inventory_analytics_agent.yaml" ]; then
    orchestrate agents import -f agent/inventory_analytics_agent.yaml
    
    if [ $? -eq 0 ]; then
        echo "✅ Agent imported successfully"
    else
        echo "⚠️  Agent import may have failed"
        echo "Please check the error message above"
    fi
else
    echo "❌ Error: agent/inventory_analytics_agent.yaml not found"
    exit 1
fi

echo ""
echo "========================================="
echo "Import Complete!"
echo "========================================="
echo ""
echo "✅ SQLite database created and populated"
echo "✅ Python Text-to-SQL tool ready"
echo "✅ Agent configured"
echo ""
echo "Next steps:"
echo "  1. Verify the tool is linked to the database"
echo "  2. Test the agent with sample queries from sample_queries.md"
echo "  3. Check agent behavior and adjust if needed"
echo ""
echo "Database Information:"
echo "  Location: database/inventory.db"
echo "  Tables: products, stores, inventory, transactions"
echo "  Records: 20 products, 3 stores, 60 inventory items, 50 transactions"
echo ""
echo "Sample test queries:"
echo "  Thai: แสดงสินค้าที่มีสต็อกต่ำกว่า reorder point"
echo "  English: Show products with stock below reorder point"
echo ""
echo "For more queries, see: sample_queries.md"
echo ""
echo "Happy querying with Text-to-SQL! 🚀"

# Made with Bob
