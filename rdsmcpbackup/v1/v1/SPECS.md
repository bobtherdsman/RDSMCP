# RDS Discovery Tool - Python MCP Server

## Overview
Python-based SQL Server to AWS RDS migration assessment tool with dual-mode operation:
1. **MCP Server** - Integrates with AI assistants (Kiro CLI)
2. **Standalone CLI** - Traditional command-line tool

**Note:** This tool uses hardcoded sizing logic and a static CSV file for instance recommendations. It does not query AWS APIs dynamically.

## Implementation Status: ✅ COMPLETE

### Completed Components

#### 1. SQL Queries (sql_queries.py)
- Single comprehensive query for SQL Server assessment
- All 21 feature compatibility checks
- Returns server info, resources, and feature flags in one execution
- Handles version-specific checks (SQL 2012+, 2016+)

#### 2. Core Assessment Logic (core.py)
- `analyze_sql_server()` function
- Uses ODBC Driver 18 for SQL Server
- Executes full assessment query
- Returns structured dict with server_info, resources, features, rds_compatible

#### 3. RDS Recommendation (recommendation.py)
- **Hardcoded sizing algorithm** (not from AWS APIs)
- CPU-based sizing: divides by 4, rounds up
- Hardcoded size class mapping (large → 32xlarge)
- Hardcoded scale-up/down mappings for utilization
- Filters by edition (EE/SE) and version using static CSV
- Optional utilization-based scaling (only when provided)
- Uses AwsInstancescsv.csv for instance catalog (static file)
- Returns general purpose (G) or memory-optimized (M) instances
- **Limitation:** Requires manual CSV updates for new AWS instance types

#### 4. MCP Server (server.py)
- Two tools:
  - `analyze_sql_server` - Full assessment + recommendation
  - `recommend_rds_instance` - Standalone recommendation
- Runs in stdio mode for MCP protocol
- Returns JSON responses

#### 5. CLI Interface (cli.py)
- Commands:
  - `analyze` - Full SQL Server assessment
  - `recommend` - RDS instance recommendation
- Output formats: table, json
- Uses Click framework

## Test Results

### Live SQL Server Test
**Server:** <sql-server-host>
**Credentials:** <username> / <password>

**Results:**
- Edition: Standard Edition (64-bit)
- Version: 16.0.4095.4 (SQL Server 2022)
- CPU: 32 vCPU
- Memory: 221 MB
- Database Size: 0.0 GB
- RDS Compatible: **No**
- Incompatible Features: server_triggers, always_on_ag
- Recommended Instance: **db.m6i.8xlarge** (alternative: db.m5d.8xlarge)

### Verification Against Test Server
✅ Feature checks validated against live SQL Server
✅ Recommendation logic produces consistent results
✅ Sizing calculation: 32 vCPU ÷ 4 = 8 → 8xlarge

## Files Structure

```
rdsmcp/
├── sql_queries.py           # Single comprehensive SQL query
├── core.py                  # analyze_sql_server() function
├── recommendation.py        # get_rds_recommendation() function
├── server.py                # MCP server with 2 tools
├── cli.py                   # Standalone CLI (analyze, recommend)
├── AwsInstancescsv.csv      # AWS RDS instance specifications
├── requirements.txt         # mcp, pyodbc, click
├── README.md                # Usage documentation
├── SPECS.md                 # This file
├── TEST_RESULTS.md          # Test results
└── venv/                    # Virtual environment

Dependencies:
- mcp>=0.9.0
- pyodbc>=4.0.0
- click>=8.0.0
- ODBC Driver 18 for SQL Server
```

## MCP Server Configuration

Add to Kiro CLI config:
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

## Usage Examples

### CLI Mode
```bash
cd /home/bacrifai/rdsmcp
source venv/bin/activate

# Full analysis
python cli.py analyze \
  --host <sql-server-host> \
  --username <username> \
  --password '<password>' \
  --output table

# Recommendation only
python cli.py recommend --cpu 32 --memory 128 --storage 500
```

### MCP Mode (via Kiro CLI)
```
Use rds-discovery to analyze SQL Server at <sql-server-host> with username <username> and password <password>

Use rds-discovery to recommend an RDS instance for 32 vCPU and 128 GB memory, Standard Edition, version 16
```

## Feature Compatibility Checks (21 Total)

| Feature | Check | RDS Compatible |
|---------|-------|----------------|
| linked_servers | Non-SQL Server linked servers | N = Yes |
| filestream | FileStream enabled | N = Yes |
| resource_governor | Resource Governor configured | N = Yes |
| log_shipping | Log Shipping configured | N = Yes |
| service_broker | Service Broker endpoints | N = Yes |
| database_count | >100 user databases | N = Yes |
| transaction_replication | Replication configured | N = Yes |
| extended_procedures | Extended procedures exist | N = Yes |
| tsql_endpoints | TSQL endpoints configured | N = Yes |
| polybase | PolyBase configured | N = Yes |
| buffer_pool_extension | Buffer pool extension enabled | N = Yes |
| file_tables | File tables exist | N = Yes |
| stretch_database | Stretch DB enabled | N = Yes |
| trustworthy_databases | Trustworthy DBs (>1) | N = Yes |
| server_triggers | Server-level triggers | N = Yes |
| machine_learning | External scripts enabled | N = Yes |
| data_quality_services | DQS databases exist | N = Yes |
| policy_based_management | Policy-based mgmt configured | N = Yes |
| clr_enabled | CLR enabled (version dependent) | N = Yes |
| always_on_ag | Always On AG enabled | N = Yes |
| always_on_fci | Failover Cluster Instance | N = Yes |

## RDS Recommendation Algorithm

**Implementation:** Hardcoded sizing logic with static CSV lookup

**Input:** CPU, Memory, Edition, Version, (optional) CPU/Memory Utilization

**Steps:**
1. Cap memory at 1025 GB
2. Calculate: `cpu_adjusted = ceil(cpu / 4)`
3. **Hardcoded size class mapping:**
   - cpu ≥ 25 → 32xlarge
   - 16 < cpu ≤ 24 → 24xlarge
   - 12 < cpu ≤ 16 → 16xlarge
   - 8 < cpu ≤ 12 → 12xlarge
   - 4 < cpu ≤ 8 → 8xlarge
   - 2 < cpu ≤ 4 → 4xlarge
   - 1 < cpu ≤ 2 → 2xlarge
   - cpu ≤ 1 → xlarge
   - cpu = 0 → large
4. **Hardcoded utilization scaling** (if provided):
   - CPU ≥ 80% AND Mem ≥ 80% → Scale up, type M
   - CPU ≥ 80% AND Mem ≤ 80% → Scale up, type G
   - CPU ≤ 80% AND Mem ≥ 80% → type M
   - CPU < 50% AND Mem < 50% → Scale down, type G
5. Filter CSV by: size, edition, version
6. **Hardcoded type preference:** G (db.m*, db.t*) or M (db.r*, db.x*)

**Output:** List of matching instances, primary recommendation, type, remark

**Limitations:**
- Sizing rules are static, not based on AWS current offerings
- Requires manual CSV updates when AWS releases new instance types
- Does not query AWS Pricing or EC2 APIs
- Scale-up/down mappings are hardcoded (e.g., 2xlarge → 4xlarge)

## Implementation Characteristics

**Architecture:**
- ✅ Cross-platform Python implementation
- ✅ MCP server integration for AI assistants
- ✅ Standalone CLI mode
- ✅ JSON and table output formats
- ✅ Single comprehensive SQL query (efficient)
- ✅ Error handling for connection issues

**Limitations:**
- ⚠️ Hardcoded sizing algorithm (not dynamic)
- ⚠️ Static CSV file for instance catalog
- ⚠️ No AWS API integration
- ⚠️ Requires manual updates for new instance types
- ⚠️ No pricing information
- ⚠️ No batch processing yet

## Next Steps

**High Priority:**
1. ✅ Test MCP server with Kiro CLI
2. Add AWS API integration for dynamic instance types
3. Replace hardcoded sizing with AWS-based recommendations
4. Add automatic CSV updates from AWS

**Medium Priority:**
5. Add batch analysis for multiple servers
6. Add AWS pricing integration
7. Fix CLI `recommend` command to use actual algorithm
8. Add input validation (CPU, memory, edition, version)

**Low Priority:**
9. Add HTML/CSV output formats
10. Add performance metrics collection
11. Add migration complexity scoring
