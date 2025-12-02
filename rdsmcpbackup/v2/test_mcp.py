#!/usr/bin/env python3
"""Test MCP server tools"""
import asyncio
import sys
sys.path.insert(0, '/home/bacrifai/rdsmcp')

from server import app

async def test():
    # Test list_tools
    tools = await app.list_tools()
    print(f"✓ Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Test recommend tool
    print("\n✓ Testing recommend_rds_instance:")
    result = await app.call_tool("recommend_rds_instance", {
        "cpu": 4,
        "memory_gb": 16,
        "storage_gb": 500
    })
    print(f"  {result[0].text}")

if __name__ == "__main__":
    asyncio.run(test())
