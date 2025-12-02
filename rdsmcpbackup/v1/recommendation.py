"""
RDS Instance Recommendation - Exact port from RDSDiscoveryGuide.ps1
"""
import csv
import math
from pathlib import Path


def get_rds_recommendation(cpu: int, memory_gb: float, edition: str = 'EE', version: int = 15, 
                          cpu_util: int = None, mem_util: int = None):
    """
    Recommend RDS instance based on on-prem specs
    Exact port of RDSDiscoveryGuide.ps1 RDSInstance function
    """
    
    # Cap memory at 1025 GB
    if memory_gb > 1025:
        memory_gb = 1025
    
    # Divide CPU by 4 and round up
    cpu = math.ceil(cpu / 4)
    
    # Determine size class based on CPU (only if memory < 1025)
    if memory_gb < 1025:
        if cpu >= 25:
            size = '32xlarge'
        elif cpu <= 24 and cpu > 16:
            size = '24xlarge'
        elif cpu <= 16 and cpu > 12:
            size = '16xlarge'
        elif cpu <= 12 and cpu > 8:
            size = '12xlarge'
        elif cpu <= 8 and cpu > 4:
            size = '8xlarge'
        elif cpu <= 4 and cpu > 2:
            size = '4xlarge'
        elif cpu <= 2 and cpu > 1:
            size = '2xlarge'
        elif cpu <= 1:
            size = 'xlarge'
        elif cpu == 0:
            size = 'large'
    else:
        size = '32xlarge'
    
    type_class = 'G'
    remark = ''
    
    # Handle utilization-based scaling (only if provided)
    if cpu_util is not None and mem_util is not None:
        if cpu_util >= 80 and mem_util >= 80:
            size_map = {
                '2xlarge': '4xlarge',
                '4xlarge': '8xlarge',
                '8xlarge': '12xlarge',
                '12xlarge': '16xlarge',
                '16xlarge': '24xlarge',
                '24xlarge': '32xlarge',
                '32xlarge': '32xlarge'
            }
            size = size_map.get(size.lower(), size)
            type_class = 'M'
            remark = 'Scaled up due to high CPU and memory utilization'
        elif cpu_util >= 80 and mem_util <= 80:
            size_map = {
                '2xlarge': '4xlarge',
                '4xlarge': '8xlarge',
                '8xlarge': '12xlarge',
                '12xlarge': '16xlarge',
                '16xlarge': '24xlarge',
                '24xlarge': '32xlarge',
                '32xlarge': '32xlarge'
            }
            size = size_map.get(size.lower(), size)
            type_class = 'G'
            remark = 'Scaled up due to high CPU utilization'
        elif cpu_util <= 80 and mem_util >= 80:
            type_class = 'M'
            remark = 'Memory-optimized due to high memory utilization'
        elif cpu_util < 50 and mem_util < 50:
            if size.lower() != 'xlarge':
                size_map = {
                    '2xlarge': 'xlarge',
                    '4xlarge': '2xlarge',
                    '8xlarge': '4xlarge',
                    '12xlarge': '8xlarge',
                    '16xlarge': '12xlarge',
                    '24xlarge': '16xlarge',
                    '32xlarge': '24xlarge'
                }
                size = size_map.get(size.lower(), size)
                remark = 'Scaled down due to low utilization'
            type_class = 'G'
    
    # Load CSV and find matching instances
    csv_path = Path(__file__).parent / 'AwsInstancescsv.csv'
    instances = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            instances.append(row)
    
    # Filter instances by size, edition, and version
    matches = [i for i in instances 
              if size in i['Instance Type'].lower()
              and i['Edition'] == edition
              and i['Version'] == str(version)]
    
    # Get unique instance types
    if matches:
        instance_types = list(set([m['Instance Type'].strip() for m in matches]))
        
        # Filter by type preference
        if type_class == 'M':
            filtered = [i for i in instance_types if any(x in i for x in ['db.r', 'db.x', 'db.z1d', 'db.x2iedn'])]
            if filtered:
                instance_types = filtered
        elif type_class == 'G':
            filtered = [i for i in instance_types if any(x in i for x in ['db.m', 'db.t'])]
            if filtered:
                instance_types = filtered
        
        return {
            'recommended_instances': instance_types,
            'primary_recommendation': instance_types[0] if instance_types else None,
            'type': type_class,
            'remark': remark
        }
    
    return {
        'recommended_instances': [],
        'primary_recommendation': None,
        'type': type_class,
        'remark': 'No matching instance found'
    }
