# README.md for KPI-accountability.py

## Overview

`KPI-accountability.py` is a Python script for AWS cost analysis. It utilizes AWS Cost Explorer and other AWS services to provide detailed cost reports. The script allows for cost breakdown by linked AWS accounts and specific cost allocation tags. Custom date ranges are supported, and credits and refunds can be excluded from the cost data.

## Requirements

- Python 3.x
- `boto3` library
- AWS account with appropriate IAM permissions

## IAM Permissions

The AWS IAM role used to run this script must have the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetTags"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "organizations:DescribeAccount"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "resourcegroupstaggingapi:GetResources"
            ],
            "Resource": "*"
        }
    ]
}
```

## Usage

To run the script, use the following command:

```
python KPI-accountability.py --tag <TAG_KEY> --profile <AWS_PROFILE> --region <AWS_REGION> [--yesterday]
```

### Parameters

- `--tag` (required): The tag key to filter costs by.
- `--profile` (required): AWS CLI profile to use.
- `--region`: AWS region (default is `us-east-1`).
- `--yesterday`: Use this flag to limit the timeframe to the day before yesterday.

## Functions

- `get_current_month_dates()`: Retrieves the start and end dates of the current month.
- `is_cost_allocation_tag()`: Checks if a given tag is a Cost Allocation Tag.
- `get_overall_cost()`: Obtains the total cost for a specified timeframe.
- `get_costs_grouped_by_dimension()`: Retrieves costs grouped by a specific dimension.
- `get_unique_tag_values_for_key()`: Finds unique tag values for a given tag key.
- `get_costs_grouped_by_tag_value()`: Obtains costs grouped by a specific tag value for a given timeframe.
- `get_account_alias()`: Retrieves the account alias for a specified AWS account ID.

## Example Output

```
Overall cost for the period 2023-09-01 to 2023-09-30: $450.84

Costs grouped by linked account:
Linked account '123456789012 (Account-1)': $250.45 (55.54%)
  Tag value 'productA': $120.22 (48.00%)
  Tag value 'productB': $100.23 (40.00%)
  Undefined: 12.00%

Linked account '987654321098 (Account-2)': $200.39 (44.46%)
  Tag value 'productA': $80.16 (40.00%)
  Tag value 'productB': $100.23 (50.00%)
  Undefined: 10.00%
```
