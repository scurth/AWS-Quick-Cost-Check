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

def get_unattached_eips(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2_client = session.client('ec2')

    addresses_dict = ec2_client.describe_addresses()
    return [address for address in addresses_dict['Addresses'] if 'InstanceId' not in address]

def main():
    parser = argparse.ArgumentParser(description='Find unattached EIPs.')
    parser.add_argument('--profile', required=True, help='AWS profile to use')
    args = parser.parse_args()

    account_id, account_alias = get_account_info(args.profile)
    print(f'Account ID: {account_id}, Account Alias: {account_alias}\n')

    regions = get_all_regions(args.profile)

    all_eips = {}

    for region in regions:
        eips = get_unattached_eips(args.profile, region)
        all_eips[region] = eips

    for region, eips in all_eips.items():
        print(f'Region: {region} ({len(eips)} unattached EIPs)')
        for eip in eips:
            print(f'  Public IP: {eip["PublicIp"]}, Allocation ID: {eip["AllocationId"]}')

if __name__ == '__main__':
    main()

