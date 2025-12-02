# Version 2.1.0 Backup

**Backup Date:** 2025-11-30

## Features in This Version

### Core Functionality
- ✅ SQL Server to RDS migration assessment
- ✅ 24 feature checks (100% PowerShell compatible)
- ✅ RDS compatibility logic (18 feature checks)
- ✅ Instance recommendations (db.m* family, no t3)
- ✅ SSIS/SSRS detection (informational only)
- ✅ Enterprise Features detection (informational only)
- ✅ Windows Authentication support (Trusted Connection)
- ✅ SQL Authentication support

### Modes
- ✅ CLI mode (standalone)
- ✅ MCP server mode (AI assistant integration)
- ✅ Batch processing (multiple servers from file)

### Output Formats
- ✅ CSV export (39 columns)
- ✅ JSON output
- ✅ Summary statistics

### Key Improvements Over PowerShell
1. Correct RDS Custom limit (16TB vs 14.5TB)
2. SSIS/SSRS as separate columns
3. Dynamic notes with SSIS/SSRS detection info
4. Better error handling with detailed capture
5. MCP integration for AI assistants

### Files Included
- core.py - Core assessment logic
- sql_queries.py - SQL Server queries (100% PowerShell match)
- recommendation.py - RDS instance recommendations
- batch.py - Batch processing logic
- cli.py - CLI interface
- server.py - MCP server
- AwsInstancescsv.csv - RDS instance data
- README.md - Documentation
- CHANGELOG.md - Version history
- COMPARISON.md - PowerShell vs Python comparison
- requirements.txt - Python dependencies

### Test Results
- ✅ 3 servers tested successfully
- ✅ RDS compatibility logic matches PowerShell
- ✅ Instance recommendations match PowerShell
- ✅ CSV output format compatible

### Known Limitations
- No business questions (L100) - requires manual input
- No Elasticache analysis
- No utilization-based scaling
- No Windows Authentication on Linux (requires Kerberos)

## Next Steps (v3.0)
- DBC.CSV output generation
- Database-level assessment
- Additional output formats
