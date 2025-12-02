"""
Core SQL Server assessment logic shared between CLI and MCP server
"""
import pyodbc
from typing import Dict, Any
from sql_queries import FULL_ASSESSMENT_QUERY


def analyze_sql_server(host: str, username: str, password: str, port: int = 1433) -> Dict[str, Any]:
    """Analyze SQL Server instance for RDS compatibility"""
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host},{port};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes"
    
    with pyodbc.connect(conn_str, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute(FULL_ASSESSMENT_QUERY)
        row = cursor.fetchone()
        
        server_info = {
            "edition": row.Edition,
            "version": row.ProductVersion,
            "is_clustered": bool(row.IsClustered)
        }
        
        resources = {
            "cpu": row.CPU,
            "max_memory_mb": row.MaxMemory,
            "total_db_size_gb": float(row.UsedSpaceGB)
        }
        
        features = {
            "linked_servers": row.islinkedserver,
            "filestream": row.isFilestream,
            "resource_governor": row.isResouceGov,
            "log_shipping": row.issqlTLShipping,
            "service_broker": row.issqlServiceBroker,
            "database_count": row.dbcount,
            "transaction_replication": row.issqlTranRepl,
            "extended_procedures": row.isextendedproc,
            "tsql_endpoints": row.istsqlendpoint,
            "polybase": row.ispolybase,
            "buffer_pool_extension": row.isbufferpoolextension,
            "file_tables": row.isfiletable,
            "stretch_database": row.isstretchDB,
            "trustworthy_databases": row.istrustworthy,
            "server_triggers": row.Isservertrigger,
            "machine_learning": row.isRMachineLearning,
            "data_quality_services": row.ISDQS,
            "policy_based_management": row.ISPolicyBased,
            "clr_enabled": row.isCLREnabled,
            "always_on_ag": row.IsAlwaysOnAG,
            "always_on_fci": row.isalwaysonFCI,
            "server_role": row.DBRole
        }
        
        return {
            "server_info": server_info,
            "resources": resources,
            "features": features,
            "rds_compatible": all(v in ['N', 'Not Supported', 'N/A'] for v in features.values() if v != features['server_role'])
        }
