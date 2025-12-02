"""
Core SQL Server assessment logic shared between CLI and MCP server
"""
import pyodbc
from typing import Dict, Any
from sql_queries import FULL_ASSESSMENT_QUERY


def analyze_sql_server(host: str, username: str = None, password: str = None, port: int = 1433, use_windows_auth: bool = False) -> Dict[str, Any]:
    """Analyze SQL Server instance for RDS compatibility"""
    if use_windows_auth:
        # Windows Authentication (Kerberos/NTLM)
        conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host},{port};Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes"
    else:
        # SQL Authentication
        conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host},{port};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes"
    
    with pyodbc.connect(conn_str, timeout=30) as conn:
        # Add output converter for SQL_VARIANT and other types
        conn.add_output_converter(-150, lambda x: x.decode('utf-16le') if isinstance(x, bytes) else str(x))
        
        cursor = conn.cursor()
        cursor.execute(FULL_ASSESSMENT_QUERY)
        row = cursor.fetchone()
        
        server_info = {
            "edition": str(row.Edition) if row.Edition else "",
            "version": str(row.ProductVersion) if row.ProductVersion else "",
            "is_clustered": bool(row.IsClustered) if row.IsClustered else False,
            "source": str(row.Source).strip() if row.Source else "EC2/OnPrem"
        }
        
        resources = {
            "cpu": int(row.CPU) if row.CPU else 0,
            "max_memory_mb": int(row.MaxMemory) if row.MaxMemory else 0,
            "total_db_size_gb": float(row.UsedSpaceGB) if row.UsedSpaceGB else 0.0
        }
        
        features = {
            "linked_servers": str(row.islinkedserver).strip() if row.islinkedserver else "N",
            "filestream": str(row.isFilestream).strip() if row.isFilestream else "N",
            "resource_governor": str(row.isResouceGov).strip() if row.isResouceGov else "N",
            "log_shipping": str(row.issqlTLShipping).strip() if row.issqlTLShipping else "N",
            "service_broker": str(row.issqlServiceBroker).strip() if row.issqlServiceBroker else "N",
            "database_count": str(row.dbcount).strip() if row.dbcount else "N",
            "transaction_replication": str(row.issqlTranRepl).strip() if row.issqlTranRepl else "N",
            "extended_procedures": str(row.isextendedproc).strip() if row.isextendedproc else "N",
            "tsql_endpoints": str(row.istsqlendpoint).strip() if row.istsqlendpoint else "N",
            "polybase": str(row.ispolybase).strip() if row.ispolybase else "N",
            "buffer_pool_extension": str(row.isbufferpoolextension).strip() if row.isbufferpoolextension else "N",
            "file_tables": str(row.isfiletable).strip() if row.isfiletable else "N",
            "stretch_database": str(row.isstretchDB).strip() if row.isstretchDB else "N",
            "trustworthy_databases": str(row.istrustworthy).strip() if row.istrustworthy else "N",
            "server_triggers": str(row.Isservertrigger).strip() if row.Isservertrigger else "N",
            "machine_learning": str(row.isRMachineLearning).strip() if row.isRMachineLearning else "N",
            "data_quality_services": str(row.ISDQS).strip() if row.ISDQS else "N",
            "policy_based_management": str(row.ISPolicyBased).strip() if row.ISPolicyBased else "N",
            "clr_enabled": str(row.isCLREnabled).strip() if row.isCLREnabled else "N",
            "always_on_ag": str(row.IsAlwaysOnAG).strip() if row.IsAlwaysOnAG else "N",
            "always_on_fci": str(row.isalwaysonFCI).strip() if row.isalwaysonFCI else "N",
            "read_only_replica": str(row.IsReadReplica).strip() if row.IsReadReplica else "N",
            "server_role": str(row.DBRole).strip() if row.DBRole else "Standalone",
            "enterprise_features": str(row.isEEFeature).strip() if row.isEEFeature and str(row.isEEFeature).strip() else "",
            "ssis": str(row.isSSSIS).strip() if row.isSSSIS else "N",
            "ssrs": str(row.isSSRS).strip() if row.isSSRS else "N"
        }
        
        # RDS Compatibility - match PowerShell logic exactly
        # Check only these features (exclude: always_on_ag, always_on_fci, server_role, ssis, ssrs, enterprise_features)
        blockers = [
            features['database_count'],
            features['linked_servers'],
            features['log_shipping'],
            features['filestream'],
            features['resource_governor'],
            features['transaction_replication'],
            features['extended_procedures'],
            features['tsql_endpoints'],
            features['polybase'],
            features['file_tables'],
            features['buffer_pool_extension'],
            features['stretch_database'],
            features['trustworthy_databases'],
            features['server_triggers'],
            features['machine_learning'],
            features['policy_based_management'],
            features['data_quality_services'],
            features['clr_enabled']
        ]
        
        rds_compatible = all(v in ['N', 'Not Supported', 'N/A', ''] for v in blockers)
        
        return {
            "server_info": server_info,
            "resources": resources,
            "features": features,
            "rds_compatible": rds_compatible
        }
