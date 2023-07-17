import boto3
import argparse
from datetime import datetime, timedelta

def get_all_regions(profile):
    session = boto3.Session(profile_name=profile, region_name='us-east-1')  # default region
    ec2_client = session.client('ec2')

    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    return regions

def get_account_info(profile):
    session = boto3.Session(profile_name=profile, region_name='us-east-1')  # default region
    sts_client = session.client('sts')
    iam_client = session.client('iam')

    account_id = sts_client.get_caller_identity()['Account']
    account_aliases = iam_client.list_account_aliases()['AccountAliases']
    account_alias = account_aliases[0] if account_aliases else 'No alias'

    return account_id, account_alias

def get_unused_elbs(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    elbv2_client = session.client('elbv2')
    cloudwatch_client = session.client('cloudwatch')

    all_elbs = elbv2_client.describe_load_balancers()['LoadBalancers']
    unused_elbs = []

    for elb in all_elbs:
        response = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/ApplicationELB',
            MetricName='RequestCount',
            Dimensions=[
                {
                    'Name': 'LoadBalancer',
                    'Value': elb['LoadBalancerName']
                },
            ],
            StartTime=datetime.utcnow() - timedelta(days=7),
            EndTime=datetime.utcnow(),
            Period=3600,
            Statistics=['Sum'],
        )
        if not response['Datapoints']:
            unused_elbs.append(elb)

    return unused_elbs

def main():
    parser = argparse.ArgumentParser(description='Find unused ELBs.')
    parser.add_argument('--profile', required=True, help='AWS profile to use')
    args = parser.parse_args()

    account_id, account_alias = get_account_info(args.profile)
    print(f'Account ID: {account_id}, Account Alias: {account_alias}\n')

    regions = get_all_regions(args.profile)

    all_unused_elbs = {}

    for region in regions:
        unused_elbs = get_unused_elbs(args.profile, region)
        all_unused_elbs[region] = unused_elbs

    for region, unused_elbs in all_unused_elbs.items():
        print(f'Region: {region} ({len(unused_elbs)} unused ELBs)')
        for elb in unused_elbs:
            print(f'  Load Balancer ARN: {elb["LoadBalancerArn"]}, Name: {elb["LoadBalancerName"]}')

if __name__ == '__main__':
    main()

