import boto3
import datetime
from collections import defaultdict
import argparse

# Add command line argument parsing
parser = argparse.ArgumentParser(description='Get the number of days, ignore-credits option, and AWS profile')
parser.add_argument('-d', '--days', type=int, help='Number of days to go back', default=1)
parser.add_argument('-ic', '--ignore-credits', action='store_true', help='Ignore credits')
parser.add_argument('-p', '--profile', type=str, help='AWS profile', default='default')
args = parser.parse_args()

# Set AWS profile and region
session = boto3.Session(profile_name=args.profile, region_name='us-east-1')

# Initialize Cost Explorer client
ce = session.client('ce')
organizations = session.client('organizations')

def get_account_name(account_id):
    response = organizations.describe_account(AccountId=account_id)
    return response['Account']['Name']

def get_cost_and_usage(num_days, ignore_credits):
    # Get current date and previous day
    end = datetime.datetime.now().date()
    start = end - datetime.timedelta(days=num_days)

    print(end)
    print(start)

    # Convert dates to strings
    start_str = start.isoformat()
    end_str = end.isoformat()

    # Get cost and usage data
    if ignore_credits:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_str,
                'End': end_str
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}
            ],
            Filter={
                "Not": {
                    "Dimensions": {
                        "Key": "RECORD_TYPE",
                        "Values": ["Credit"]
                    }
                }
            }
        )
    else:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_str,
                'End': end_str
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}
            ]
        )

    # Initialize results
    results = defaultdict(lambda: defaultdict(float))

    # Iterate over all elements in 'ResultsByTime'
    for day in response['ResultsByTime']:
        for group in day['Groups']:
            service_name = group['Keys'][0]
            linked_account = group['Keys'][1]
            account_name = get_account_name(linked_account)
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            
            # Aggregate costs
            results[(linked_account, account_name)][service_name] += cost

    # Print results
    for (linked_account, account_name), services in results.items():
        print(f"Linked Account: {linked_account} ({account_name})")
        for service, cost in services.items():
            print(f"  Service: {service}")
            print(f"  Blended Cost: {cost:.5f}")

# Calling the function with the specified number of days and ignore credits option
get_cost_and_usage(args.days, args.ignore_credits)
