# RDS MCP - SQL Server to RDS Migration Assessment Tool

A Python-based tool for assessing SQL Server instances for migration to AWS RDS. Functionally equivalent to PowerShell RDSDiscoveryGuide for automated technical discovery. Available as both a CLI tool and an MCP (Model Context Protocol) server for integration with AI assistants.

## Features

- **100% PowerShell Compatibility**: Identical SQL queries and RDS compatibility logic
- **Comprehensive Assessment**: Analyzes 24 SQL Server features for RDS compatibility
- **Dual Modes**: Use as standalone CLI or MCP server
- **Batch Processing**: Analyze multiple servers from a file
- **Instance Recommendations**: Get RDS instance type recommendations (db.m* family, no t3)
- **CSV Export**: 39-column format matching PowerShell technical output
- **DBC Export**: 23-column Database Consolidation format for migration planning
- **SSIS/SSRS Detection**: Identifies Integration/Reporting Services (informational only)
- **Enterprise Features**: Detects Enterprise-only features without blocking RDS migration
- **Automated Technical Focus**: Excludes business survey questions

## Installation

### Prerequisites

**Python:**
- Python 3.8 or higher
- pip package manager

**ODBC Driver for SQL Server:**

The tool requires Microsoft ODBC Driver 18 for SQL Server.

**Linux (Ubuntu/Debian):**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

**Linux (RHEL/CentOS):**
```bash
curl https://packages.microsoft.com/config/rhel/8/prod.repo | sudo tee /etc/yum.repos.d/mssql-release.repo
sudo yum remove unixODBC-utf16 unixODBC-utf16-devel
sudo ACCEPT_EULA=Y yum install -y msodbcsql18
```

**macOS:**
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18
```

**Windows:**
- Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Run installer and follow prompts

### Install RDS MCP Tool

```bash
# Clone repository
git clone <repo-url>
cd rdsmcp

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test CLI
python3 cli.py --help

# Test connection to SQL Server
python3 cli.py analyze --host <your-server> --username <user> --password <password>
```

## Usage

### CLI Mode

#### Single Server Analysis

**SQL Authentication:**
```bash
python cli.py analyze --host <hostname> --username <user> --password <pass> [--port 1433]
```

**Windows Authentication:**
```bash
python cli.py analyze --host <hostname> --windows-auth [--port 1433]
```

#### Batch Analysis

**SQL Authentication:**
```bash
python cli.py batch --input servers.txt --username <user> --password <pass> --output results.csv
```

**Windows Authentication:**
```bash
python cli.py batch --input servers.txt --windows-auth --output results.csv
```

**With DBC.CSV output:**
```bash
python cli.py batch --input servers.txt --username <user> --password <pass> --output results.csv --dbc
```
This generates both `results.csv` (39 columns) and `results_DBC.csv` (23 columns)

Input file format (one server per line):
```
server1.example.com
server2.example.com
10.0.1.100
```

#### Instance Recommendation
```bash
python cli.py recommend --cpu 16 --memory 64 --edition SE --version 15
```

### MCP Server Mode

Configure in your MCP client (e.g., Kiro CLI):

```json
{
  "mcpServers": {
    "rds-discovery": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/rdsmcp/server.py"]
    }
  }
}
```

Available MCP tools:
- `analyze_sql_server` - Analyze single SQL Server instance
- `recommend_rds_instance` - Get RDS instance recommendations
- `analyze_sql_servers_batch` - Batch analyze multiple servers with CSV export

## Assessment Checks

The tool evaluates the following features for RDS compatibility (matches PowerShell logic exactly):

### Blocking Features (RDS Incompatible)
1. Database Count > 100
2. Linked Servers (heterogeneous - non-SQL Server/Oracle)
3. Log Shipping
4. FILESTREAM
5. Resource Governor
6. Transaction Replication
7. Extended Procedures (non-standard)
8. TSQL Endpoints
9. PolyBase
10. File Tables
11. Buffer Pool Extension
12. Stretch Database
13. Trustworthy Databases
14. Server Triggers
15. Machine Learning Services (R/Python)
16. Policy-Based Management
17. Data Quality Services
18. CLR Enabled (SQL 2017+)

### Informational Only (Not Blocking)
- **Always On Availability Groups** - Current state, not a blocker
- **Always On Failover Cluster Instances** - Current state, not a blocker
- **Server Role** (Primary/Secondary/Readable/Standalone) - Informational
- **Enterprise Edition Features** (Partitioning, Compression, CDC, etc.) - Supported in RDS EE
- **SSIS** (SQL Server Integration Services) - Separate service, migrate to AWS Glue/EC2
- **SSRS** (SQL Server Reporting Services) - Separate service, migrate to EC2/QuickSight
- **Read Only Replica** - Configuration detail

## RDS Custom Compatibility

- **RDS Standard**: Up to 16 TB database size
- **RDS Custom**: Up to 16 TB (same limit)
- **Above 16 TB**: EC2 recommended

## Output Format

### Standard CSV (39 columns)
Full technical assessment with all feature checks, compatibility status, and recommendations.

### DBC CSV (23 columns)
Simplified Database Consolidation format for migration planning:
- ServerName, VCPU, Memory, Edition
- Cluster/Always On status
- Instance recommendations
- Placeholders for manual input (CPU/Memory utilization, storage, IOPS, throughput)
- Optimized for infrastructure planning and capacity estimation

Generate with `--dbc` flag: `python cli.py batch --input servers.txt --username user --password pass --dbc`

### CSV Columns (39 total)
1. Server Name
2. SQL Server Current Edition
3. SQL Server current Version
4. Sql server Source (RDS/EC2/OnPrem)
5. SQL Server Replication
6. Heterogeneous linked server
7. Database Log Shipping
8. FILESTREAM
9. Resource Governor
10. Service Broker Endpoints
11. Non Standard Extended Proc
12. TSQL Endpoints
13. PolyBase
14. File Table
15. buffer Pool Extension
16. Stretch DB
17. Trust Worthy On
18. Server Side Trigger
19. R & Machine Learning
20. Data Quality Services
21. Policy Based Management
22. CLR Enabled
23. DB count Over 100
24. Total DB Size in GB
25. Always ON AG enabled
26. Always ON FCI enabled
27. Read Only Replica
28. Server Role Desc
29. RDS Compatible
30. RDS Custom Compatible
31. EC2 Compatible
32. Elasticache
33. Enterprise Level Feature Used
34. Memory
35. CPU
36. Instance Type
37. isSSIS
38. isSSRS
39. Note

### JSON Output (MCP/CLI)
```json
{
  "server_info": {
    "edition": "Standard Edition (64-bit)",
    "version": "16.0.4095.4",
    "is_clustered": false,
    "source": "EC2/OnPrem"
  },
  "resources": {
    "cpu": 16,
    "max_memory_mb": 32768,
    "total_db_size_gb": 100.5
  },
  "features": {
    "linked_servers": "N",
    "filestream": "N",
    "server_triggers": "N",
    "always_on_ag": "N",
    "enterprise_features": "",
    "ssis": "N",
    "ssrs": "N"
  },
  "rds_compatible": true,
  "recommendation": {
    "primary_recommendation": "db.m6i.4xlarge",
    "recommended_instances": ["db.m6i.4xlarge", "db.m5d.4xlarge"],
    "type": "G"
  }
}
```

## Instance Recommendations

- **General Purpose (G)**: db.m5d.*, db.m6i.* (no t3 burstable instances)
- **Memory Optimized (M)**: db.r*, db.x*, db.z1d.* (excludes db.m*, db.r3*, db.r4*, db.t3*, db.x1*, db.x1e*)
- **High Memory (>1TB)**: db.x* family
- **Sizing**: Based on CPU/4 ratio, matches PowerShell logic

## Requirements

- Python 3.8+
- pyodbc
- ODBC Driver 18 for SQL Server
- SQL Server credentials with appropriate permissions OR Windows Authentication
- AwsInstancescsv.csv (RDS instance data)

## Authentication Methods

### SQL Authentication
- Requires username and password
- Works on Windows and Linux
- Example: `--username sa --password MyPassword123`

### Windows Authentication (Trusted Connection)
- Uses current Windows user credentials
- Requires `--windows-auth` flag
- No username/password needed
- Windows only (or Linux with Kerberos configured)
- Example: `--windows-auth`

## Permissions Required

The tool requires the following SQL Server permissions:
- VIEW SERVER STATE
- VIEW ANY DEFINITION
- Access to system databases (master, msdb)
- sp_MSforeachdb execution (for Enterprise Features, File Tables, SSIS detection)

## Differences from PowerShell

### Not Included (Intentional)
- **Business Questions (L100)**: 9 manual input questions excluded (requires human input)
- **Elasticache Analysis**: Read/write pattern analysis not implemented
- **Utilization-Based Scaling**: CPU/Memory utilization adjustments not implemented

### Improvements Over PowerShell
- **Windows Authentication Support**: Added Trusted Connection support (PowerShell has this)
- **More Accurate RDS Compatibility**: Correctly excludes SSIS/SSRS/Enterprise Features/Always On from blocking
- **Correct RDS Custom Limit**: 16TB (PowerShell uses 14.5TB)
- **SSIS/SSRS Columns**: Added to CSV output (PowerShell doesn't include)
- **Dynamic Notes**: Adds SSIS/SSRS detection info to notes field
- **Better Error Handling**: Detailed error capture with summary statistics
- **JSON Output**: Available in addition to CSV
- **MCP Integration**: Can be used as tool by AI assistants

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
