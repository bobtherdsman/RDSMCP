# RDS Discovery - SQL Server to RDS Migration Assessment

Python-based tool for assessing SQL Server instances for AWS RDS migration compatibility.

## Dual-Mode Operation

### 1. MCP Server Mode
Integrates with AI assistants via Model Context Protocol:

**Add to Kiro CLI config:**
```json
{
  "mcpServers": {
    "rds-discovery": {
      "command": "/home/bacrifai/rdsmcp/venv/bin/python",
      "args": ["/home/bacrifai/rdsmcp/server.py"]
    }
  }
}
```

**Available MCP Tools:**
- `analyze_sql_server` - Full compatibility assessment with RDS recommendation
- `recommend_rds_instance` - Get RDS instance recommendation based on resources

### 2. Standalone CLI Mode
```bash
# Analyze SQL Server
python cli.py analyze --host <sql-server-host> --username <username> --password <password>

# Get RDS recommendation
python cli.py recommend --cpu 32 --memory 128 --storage 500
```

## Installation

```bash
pip install -r requirements.txt
```

Requires ODBC Driver 18 for SQL Server.

## Features Checked (21 total)

- Linked Servers (non-SQL Server)
- FileStream
- Resource Governor
- Log Shipping
- Service Broker Endpoints
- Transaction Replication
- Extended Procedures
- PolyBase
- Buffer Pool Extension
- File Tables
- Stretch Database
- CLR Enabled
- Always On Availability Groups
- Always On Failover Cluster Instance
- Trustworthy Databases
- Server Triggers
- Machine Learning Services
- Data Quality Services
- Policy Based Management
- Database Count (>100)
- TSQL Endpoints

## RDS Recommendation Logic

Uses exact algorithm from AWS RDSDiscoveryGuide.ps1:
- CPU-based sizing (divides by 4, rounds up)
- Maps to instance size class (large, xlarge, 2xlarge, etc.)
- Filters by SQL Server edition (EE/SE) and version
- Optional utilization-based scaling
- Returns general purpose (db.m*/db.t*) or memory-optimized (db.r*/db.x*) instances

## Output

Returns compatibility assessment with:
- Server information (edition, version, clustering)
- Resource metrics (CPU, memory, storage)
- Feature compatibility flags (Y/N/Not Supported)
- RDS compatibility status
- RDS instance recommendation with alternatives

## Example Output

```
=== SQL Server Analysis: <sql-server-host> ===

Edition: Standard Edition (64-bit)
Version: 16.0.4095.4
CPU: 32
Memory: 221 MB
Database Size: 0.0 GB

RDS Compatible: No

Incompatible Features Found:
  - server_triggers
  - always_on_ag

Recommended RDS Instance: db.m6i.8xlarge
Alternative instances: db.m5d.8xlarge
```
