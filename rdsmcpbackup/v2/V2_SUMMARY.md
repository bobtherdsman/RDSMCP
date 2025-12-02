# V2 Release Summary - Batch Processing with Enhanced Features

## What's New in V2

Added batch processing capability to analyze multiple SQL Servers from a single input file, matching PowerShell RDSDiscoveryGuide.ps1 behavior with additional enhancements.

## New Features

### 1. Batch CLI Command
```bash
python cli.py batch --input servers.txt --username sa --password 'Pass123'
```

### 2. Batch MCP Tool
```
analyze_sql_servers_batch
- Processes multiple servers from file
- Same credentials applied to all servers
- Returns JSON results AND creates CSV file
- Default output: batch_results.csv
```

### 3. New Feature Checks Added
- **Enterprise Level Feature Used** - Detects Enterprise-only features in use (e.g., ChangeCapture, Partitioning)
- **isSSIS** - Detects user-created SSIS packages (excludes system Data Collector packages)
- **isSSRS** - Detects SSRS installations (ReportServer databases)

## Key Design Decisions

### 1. Enterprise Features Detection
- Checks `sys.dm_db_persisted_sku_features` across all databases
- Returns comma-separated list of features (e.g., "ChangeCapture, Partitioning")
- Empty string if no Enterprise features detected
- Wrapped in TRY/CATCH for permission handling

### 2. SSIS Detection
- **SQL 2012+:** Checks SSISDB database first, then msdb.dbo.sysssispackages
- **SQL 2008/2008R2:** Checks msdb.dbo.sysssispackages only
- **Filters out system packages:** Excludes packages in "Data Collector" folder
- **Informational only:** Does NOT affect RDS compatibility

### 3. SSRS Detection
- Checks for ReportServer databases (ReportServer, ReportServerTempDB)
- **Informational only:** Does NOT affect RDS compatibility

### 4. RDS Compatibility Logic
- Checks all 21 feature flags
- Excludes from check: `server_role`, `ssis`, `ssrs`, `enterprise_features` (empty string allowed)
- Compatible if all checked features are 'N', 'Not Supported', 'N/A', or ''

### 5. Dynamic Notes
- Base: "Assessment completed successfully"
- If SSIS detected: Adds "SSIS detected - informational only, does not affect RDS compatibility"
- If SSRS detected: Adds "SSRS detected - informational only, does not affect RDS compatibility"
- If both: "SSIS and SSRS detected - informational only, does not affect RDS compatibility"

## Output Format (38 Columns)

**Columns 1-4:** Server info (Name, Edition, Version, Source)
**Columns 5-25:** 21 Feature compatibility checks
**Columns 26-28:** DB Size, Always ON checks, Server Role
**Columns 29-33:** RDS/RDS Custom/EC2 Compatible, Elasticache, Enterprise Features
**Columns 34-36:** Memory, CPU, Instance Type (Recommendation)
**Columns 37-38:** isSSIS, isSSRS (informational only)
**Column 39:** Note (dynamic based on SSIS/SSRS detection)

## Files Modified

1. **batch.py** - Added dynamic notes for SSIS/SSRS
2. **cli.py** - Batch command
3. **server.py** - Batch MCP tool with CSV export
4. **core.py** - Added Enterprise Features/SSIS/SSRS, updated RDS compatibility logic
5. **sql_queries.py** - Added Enterprise Features, SSIS, SSRS checks with error handling
6. **README.md** - Updated documentation
7. **V2_SUMMARY.md** - This file

## Testing Results

Tested with 3 servers:
- ✅ All 21 feature checks working
- ✅ Enterprise Features detection (ChangeCapture detected on 3.81.26.46)
- ✅ SSIS/SSRS detection (system packages filtered)
- ✅ RDS compatibility logic correct (SSIS/SSRS don't affect it)
- ✅ Dynamic notes working
- ✅ CSV format matches PowerShell (38 columns)

## Backward Compatibility

✅ All V1 functionality preserved
