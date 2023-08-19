import boto3
import argparse
from collections import defaultdict

# Add command line argument parsing
parser = argparse.ArgumentParser(description='Find AWS resources based on tags')
parser.add_argument('-p', '--profile', type=str, help='AWS profile', default='default')
parser.add_argument('--missing-tag', type=str, help='Find resources that do NOT have this tag key')
parser.add_argument('--with-tag', type=str, help='Find resources that HAVE this tag key and group by its value')
parser.add_argument('--exclude-defaults', action='store_true', help='Exclude default resources like VPCs and subnets')
args = parser.parse_args()

# Constants for default resources
DEFAULT_RESOURCES = ['vpc', 'subnet', 'security-group', 'network-insights-access-scope']

# Set AWS profile
session = boto3.Session(profile_name=args.profile, region_name='us-east-1')

# Get all AWS regions
ec2 = session.client('ec2', region_name='us-east-1')
all_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

grouped_by_region = defaultdict(lambda: defaultdict(list))

for region_name in all_regions:
    # Create the Resource Groups Tagging API client for the current region
    tagging = session.client('resourcegroupstaggingapi', region_name=region_name)

    # Use a paginator to get all resources
    paginator = tagging.get_paginator('get_resources')

    # This will hold all the resources for the current region
    regional_resources = []

    # Iterate over all pages of resources
    for page in paginator.paginate():
        regional_resources.extend(page['ResourceTagMappingList'])

    for resource in regional_resources:
        resource_type = resource['ResourceARN'].split(":")[2].lower()  # Extract resource type from ARN
        
        # Skip default resources if exclude-defaults is set
        if args.exclude_defaults and resource_type in DEFAULT_RESOURCES:
            continue
        
        tags = {tag['Key']: tag['Value'] for tag in resource['Tags']}
        region_parts = resource['ResourceARN'].split(":")
        region = region_parts[3] if (len(region_parts) > 3 and region_parts[3]) else "Global"
        
        if args.missing_tag and args.missing_tag not in tags:
            grouped_by_region[region]["missing"].append(resource['ResourceARN'])
        elif args.with_tag and args.with_tag in tags:
            grouped_by_region[region][tags[args.with_tag]].append(resource['ResourceARN'])

for region, data in grouped_by_region.items():
    print(f"\nRegion: {region}")
    if args.missing_tag:
        print(f"\nResources missing the tag: {args.missing_tag}")
        for arn in data["missing"]:
            print(f"Resource ARN: {arn}")
    elif args.with_tag:
        print(f"\nResources with the tag: {args.with_tag}")
        for tag_value, resource_arns in data.items():
            print(f"\nTag Value: {tag_value}")
            for arn in resource_arns:
                print(f"Resource ARN: {arn}")

