#!/usr/bin/env python3
"""Test MCP server tools directly"""
import asyncio
import json
from recommendation import get_rds_recommendation
from core import analyze_sql_server

async def test_recommendation():
    print("Testing recommend_rds_instance tool:")
    result = get_rds_recommendation(32, 128, edition='SE', version=16)
    print(json.dumps(result, indent=2))
    print()

async def test_analyze():
    print("Testing analyze_sql_server tool:")
    print("Skipping - requires credentials")
    return
    try:
        result = analyze_sql_server(
            "<sql-server-host>",
            "<username>",
            "<password>"
        )
        
        # Add recommendation
        cpu = result['resources']['cpu']
        memory_gb = result['resources']['max_memory_mb'] / 1024
        edition = 'EE' if 'Enterprise' in result['server_info']['edition'] else 'SE'
        version = int(result['server_info']['version'].split('.')[0])
        
        recommendation = get_rds_recommendation(cpu, memory_gb, edition=edition, version=version)
        result['recommendation'] = recommendation
        result['recommended_instance'] = recommendation['primary_recommendation']
        
        print(f"Server: {result['server_info']['edition']} {result['server_info']['version']}")
        print(f"Resources: {cpu} vCPU, {result['resources']['max_memory_mb']} MB")
        print(f"RDS Compatible: {result['rds_compatible']}")
        print(f"Recommended: {result['recommended_instance']}")
        print(f"Alternatives: {', '.join(result['recommendation']['recommended_instances'])}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    await test_recommendation()
    await test_analyze()

if __name__ == "__main__":
    asyncio.run(main())
