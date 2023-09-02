import boto3
import argparse
from datetime import datetime, timedelta

def get_current_month_dates():
    today = datetime.today()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:  # If current month is December
        end_date = start_date.replace(year=start_date.year+1, month=1)
    else:
        end_date = start_date.replace(month=start_date.month+1)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def is_cost_allocation_tag(profile, tag_key, region):
    boto3.setup_default_session(profile_name=profile, region_name=region)
    client = boto3.client('ce')
    
    end_date = datetime.today().strftime('%Y-%m-%d')  # Get the current date
    start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')  # Get the date 24 hours ago
    
    # Retrieve a list of active Cost Allocation Tags for the last 24 hours
    response = client.get_tags(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        }
    )

    # Debugging line to print all Cost Allocation Tags
    print("Active Cost Allocation Tags:", response['Tags'])

    # Check if the provided tag_key is in the list of active tags
    return tag_key in response['Tags']

def get_overall_cost(profile, start_date, end_date, region):
    boto3.setup_default_session(profile_name=profile, region_name=region)
    client = boto3.client('ce')
    
    # Define the filter to exclude Refunds and Credits
    credit_refund_filter = {
        "And": [
            {
                "Not": {
                    "Dimensions": {
                        "Key": "RECORD_TYPE",
                        "Values": ["Credit"]
                    }
                }
            },
            {
                "Not": {
                    "Dimensions": {
                        "Key": "RECORD_TYPE",
                        "Values": ["Refund"]
                    }
                }
            }
        ]
    }
    
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Filter=credit_refund_filter,
        Metrics=['UnblendedCost']
    )
    
    return float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

def get_costs_grouped_by_dimension(profile, start_date, end_date, dimension_key, region):
    boto3.setup_default_session(profile_name=profile, region_name=region)
    client = boto3.client('ce')
    
    # Define the filter to exclude Refunds and Credits
    credit_refund_filter = {
        "And": [
            {
                "Not": {
                    "Dimensions": {
                        "Key": "RECORD_TYPE",
                        "Values": ["Credit"]
                    }
                }
            },
            {
                "Not": {
                    "Dimensions": {
                        "Key": "RECORD_TYPE",
                        "Values": ["Refund"]
                    }
                }
            }
        ]
    }
    
    # Query to get costs grouped by the specified dimension
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Filter=credit_refund_filter,
        Metrics=['UnblendedCost'],
        GroupBy=[{"Type": "DIMENSION", "Key": dimension_key}]
    )
    
    # Extracting and returning the grouped costs
    results = {}
    for group in response['ResultsByTime'][0]['Groups']:
        dimension_value = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        results[dimension_value] = cost
    return results

def get_unique_tag_values_for_key(profile, tag_key, region):
    boto3.setup_default_session(profile_name=profile, region_name=region)
    client = boto3.client('resourcegroupstaggingapi')
    
    unique_tag_values = set()
    pagination_token = ''
    while True:
        response = client.get_resources(
            TagFilters=[
                {
                    'Key': tag_key
                }
            ],
            IncludeComplianceDetails=False,
            PaginationToken=pagination_token
        )
        
        for resource_tag_mapping in response['ResourceTagMappingList']:
            for tag in resource_tag_mapping['Tags']:
                if tag['Key'] == tag_key:
                    unique_tag_values.add(tag['Value'])

        # Check if there's a next page of results.
        if 'PaginationToken' in response and response['PaginationToken']:
            pagination_token = response['PaginationToken']
        else:
            break
                
    return list(unique_tag_values)

def get_costs_grouped_by_tag_value(profile, start_date, end_date, tag_key, region):
    boto3.setup_default_session(profile_name=profile, region_name = region)
    client = boto3.client('ce')
    
    # Define the filter to exclude Refunds and Credits and only include the specified tag key
    tag_filter = {
    "And": [
        {
            "Not": {
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": ["Credit", "Refund"]
                }
            }
        },
        {
            "Tags": {
                "Key": tag_key,
                "Values": [tag_value]
            }
        },
        {
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "Values": [account]  # Ensure you're passing the account as an argument to the function
            }
        }
      ]
    }

    # Query to get costs grouped by the specified tag key
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Filter=tag_filter,
        Metrics=['UnblendedCost'],
        GroupBy=[{"Type": "TAG", "Key": tag_key}]
    )
    
    # Extracting and returning the grouped costs
    results = {}
    for group in response['ResultsByTime'][0]['Groups']:
        current_tag_value = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        results[current_tag_value] = cost
    return results

def get_account_alias(profile, account_id, region):
    boto3.setup_default_session(profile_name=profile, region_name=region)
    client = boto3.client('organizations')

    try:
        response = client.describe_account(AccountId=account_id)
        return response.get('Account', {}).get('Name', '')
    except Exception as e:
        return ''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWS Cost Explorer Script')
    parser.add_argument('--tag', type=str, required=True, help='Tag key to search for')
    parser.add_argument('--profile', type=str, required=True, help='AWS Profile Name')
    parser.add_argument('--region', type=str, default="us-east-1", help='AWS Region')
    parser.add_argument('--yesterday', action='store_true', help='Limit the timeframe to the day before')

    args = parser.parse_args()

    profile = args.profile
    region = args.region
    tag_key = args.tag

    if args.yesterday:
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        start = yesterday.strftime('%Y-%m-%d')
        end = today.strftime('%Y-%m-%d')
    else:
        start, end = get_current_month_dates()

    overall_cost = get_overall_cost(profile, start, end, region)
    linked_account_grouped_costs = get_costs_grouped_by_dimension(profile, start, end, "LINKED_ACCOUNT", region)

    if not is_cost_allocation_tag(profile, tag_key, region):
        print(f"Warning: The tag '{tag_key}' is not a Cost Allocation Tag. Costs might not be accurate or available.")
 
    print(f"Overall cost for the period {start} to {end}: ${overall_cost:.2f}\n")
    
    print("Costs grouped by linked account:")
    for account, account_cost in linked_account_grouped_costs.items():
        account_percentage = (account_cost / overall_cost) * 100 if overall_cost else 0
        account_alias = get_account_alias(profile, account, region)
        print(f"\nLinked account '{account} ({account_alias})': ${account_cost:.2f} ({account_percentage:.2f}%)")
        
        # Fetch unique tag values for the tag key
        unique_tag_values = get_unique_tag_values_for_key(profile, tag_key, region)
        
        sum_of_tag_percentages = 0
        for tag_value in unique_tag_values:
            tag_value_grouped_costs = get_costs_grouped_by_tag_value(profile, start, end, tag_key, tag_value)
            
            for tag_value, tag_cost in tag_value_grouped_costs.items():
                tag_percentage = (tag_cost / account_cost) * 100 if account_cost else 0
                sum_of_tag_percentages += tag_percentage
                print(f"  Tag value '{tag_value}': ${tag_cost:.2f} ({tag_percentage:.2f}%)") 
        
        # Check if there's a percentage that's undefined
        if sum_of_tag_percentages < 100:
            undefined_percentage = 100 - sum_of_tag_percentages
            print(f"  Undefined: {undefined_percentage:.2f}%")
