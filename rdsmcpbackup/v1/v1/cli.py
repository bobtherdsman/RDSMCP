#!/usr/bin/env python3
"""
Standalone CLI for SQL Server to RDS Migration Assessment
"""
import click
import json
from core import analyze_sql_server


@click.group()
def cli():
    """SQL Server to RDS Migration Assessment Tool"""
    pass


@cli.command()
@click.option('--host', required=True, help='SQL Server hostname or IP')
@click.option('--username', required=True, help='SQL Server username')
@click.option('--password', required=True, help='SQL Server password')
@click.option('--port', default=1433, help='SQL Server port')
@click.option('--output', type=click.Choice(['json', 'table']), default='table', help='Output format')
def analyze(host, username, password, port, output):
    """Analyze SQL Server instance for RDS compatibility"""
    try:
        from recommendation import get_rds_recommendation
        
        result = analyze_sql_server(host, username, password, port)
        
        # Add RDS recommendation using PowerShell logic
        cpu = result['resources']['cpu']
        memory_gb = result['resources']['max_memory_mb'] / 1024 if isinstance(result['resources']['max_memory_mb'], (int, float)) else 0
        
        # Determine edition from server info
        edition = 'EE' if 'Enterprise' in result['server_info']['edition'] else 'SE'
        version = int(result['server_info']['version'].split('.')[0])
        
        recommendation = get_rds_recommendation(cpu, memory_gb, edition=edition, version=version)
        result['recommendation'] = recommendation
        result['recommended_instance'] = recommendation['primary_recommendation']
        
        if output == 'json':
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"\n=== SQL Server Analysis: {host} ===\n")
            click.echo(f"Edition: {result['server_info']['edition']}")
            click.echo(f"Version: {result['server_info']['version']}")
            click.echo(f"CPU: {result['resources']['cpu']}")
            click.echo(f"Memory: {result['resources']['max_memory_mb']} MB")
            click.echo(f"Database Size: {result['resources']['total_db_size_gb']} GB")
            click.echo(f"\nRDS Compatible: {'Yes' if result['rds_compatible'] else 'No'}")
            
            incompatible = [k for k, v in result['features'].items() if v == 'Y']
            if incompatible:
                click.echo(f"\nIncompatible Features Found:")
                for feature in incompatible:
                    click.echo(f"  - {feature}")
            
            click.echo(f"\nRecommended RDS Instance: {recommendation['primary_recommendation']}")
            if recommendation['remark']:
                click.echo(f"Note: {recommendation['remark']}")
            if len(recommendation['recommended_instances']) > 1:
                click.echo(f"Alternative instances: {', '.join(recommendation['recommended_instances'][1:])}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--cpu', required=True, type=int, help='Number of CPUs')
@click.option('--memory', required=True, type=float, help='Memory in GB')
@click.option('--storage', required=True, type=float, help='Storage in GB')
def recommend(cpu, memory, storage):
    """Recommend RDS instance type"""
    if cpu <= 2 and memory <= 8:
        instance = "db.m5.large"
    elif cpu <= 4 and memory <= 16:
        instance = "db.m5.xlarge"
    elif cpu <= 8 and memory <= 32:
        instance = "db.m5.2xlarge"
    elif cpu <= 16 and memory <= 64:
        instance = "db.m5.4xlarge"
    else:
        instance = "db.m5.8xlarge"
    
    click.echo(f"\nRecommended Instance: {instance}")
    click.echo(f"Source: {cpu} vCPU, {memory} GB RAM, {storage} GB storage")


if __name__ == '__main__':
    cli()
