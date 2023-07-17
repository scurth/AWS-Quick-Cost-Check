import boto3
import argparse

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

def get_unattached_volumes(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')

    volumes = ec2.volumes.filter(
        Filters=[
            {'Name': 'status', 'Values': ['available']}
        ]
    )

    return list(volumes)

def main():
    parser = argparse.ArgumentParser(description='Find unattached EBS volumes.')
    parser.add_argument('--profile', required=True, help='AWS profile to use')
    args = parser.parse_args()

    account_id, account_alias = get_account_info(args.profile)
    print(f'Account ID: {account_id}, Account Alias: {account_alias}\n')

    regions = get_all_regions(args.profile)

    all_volumes = {}

    for region in regions:
        volumes = get_unattached_volumes(args.profile, region)
        all_volumes[region] = sorted(volumes, key=lambda v: v.size, reverse=True)  # assuming size as a proxy for price

    for region, volumes in all_volumes.items():
        print(f'Region: {region} ({len(volumes)} unattached volumes)')
        for volume in volumes:
            print(f'  Volume ID: {volume.id}, Size: {volume.size} GB')

if __name__ == '__main__':
    main()

