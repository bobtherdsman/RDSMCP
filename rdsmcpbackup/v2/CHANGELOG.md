# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-11-30

### Added
- **Windows Authentication support** - Use `--windows-auth` flag for Trusted Connection
- Works on Windows (automatic) and Linux (with Kerberos)
- No username/password required when using Windows auth

### Changed
- Username and password are now optional (not required for Windows auth)
- MCP tool `analyze_sql_server` now accepts `use_windows_auth` parameter
- MCP tool `analyze_sql_servers_batch` now accepts `use_windows_auth` parameter

## [2.0.0] - 2025-11-29

### Added
- SSIS (SQL Server Integration Services) detection with Data Collector filtering
- SSRS (SQL Server Reporting Services) detection
- Enterprise Features detection (sys.dm_db_persisted_sku_features)
- Read Only Replica detection
- Source detection (RDS/EC2/OnPrem)
- isSSIS and isSSRS columns in CSV output
- Dynamic notes field with SSIS/SSRS detection info
- Batch processing with CSV export
- MCP server mode for AI assistant integration

### Changed
- **BREAKING**: RDS compatibility logic now matches PowerShell exactly (18 feature checks)
- **BREAKING**: SSIS, SSRS, Enterprise Features, Always On AG/FCI, and Server Role are now informational only (don't block RDS)
- Instance recommendations now exclude t3 burstable instances
- General Purpose (G) type now only includes db.m* instances
- Memory Optimized (M) type now excludes db.m*, db.r3*, db.r4*, db.t3*, db.x1*, db.x1e*
- RDS Custom limit corrected to 16TB (was 14.5TB)
- CSV output expanded to 39 columns (from 38)

### Fixed
- SSIS detection now filters out Data Collector system packages
- Instance recommendation primary selection now consistent
- ODBC type converter added for SQL_VARIANT columns
- Empty string handling for Enterprise Features in compatibility check

### Validated
- SQL queries 100% match PowerShell RDSDiscoveryGuidev5.ps1
- RDS compatibility logic matches PowerShell (excludes informational features)
- Instance sizing matches PowerShell (CPU/4 ratio, no t3)
- CSV format compatible with PowerShell (minus 9 business question columns)

## [1.0.0] - 2025-11-25

### Added
- Initial release
- Single server analysis
- Basic RDS compatibility checks
- Instance recommendations
- CLI interface
- JSON output format
