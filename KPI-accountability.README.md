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
python3 KPI-accountability.py --profile myProfile --tag billing
Active Cost Allocation Tags: ['aws:createdBy', 'aws:ecs:clusterName', 'aws:ecs:serviceName', 'billing', 'generated']
Overall cost for the period 2023-09-01 to 2023-10-01: $10,927.41

Costs grouped by linked account:

Linked account '123456789012 (Production-Env)': $7,134.21 (65.31%)
  Tag value 'billing$core-services': $1,900.32 (26.64%)
  Tag value 'billing$analytics': $2,211.40 (31.00%)
  Tag value 'billing$team-a': $1,223.15 (17.15%)
  Tag value 'billing$team-b': $902.41 (12.65%)
  Undefined: 12.56%

Linked account '234567890123 (Staging-Env)': $2,750.81 (25.17%)
  Tag value 'billing$core-services': $1,125.40 (40.92%)
  Tag value 'billing$analytics': $750.23 (27.27%)
  Tag value 'billing$team-a': $350.10 (12.73%)
  Undefined: 19.08%

Linked account '345678901234 (Dev-Env)': $890.30 (8.15%)
  Tag value 'billing$core-services': $350.12 (39.32%)
  Tag value 'billing$analytics': $310.11 (34.83%)
  Tag value 'billing$team-b': $110.09 (12.36%)
  Undefined: 13.49%

Linked account '456789012345 (Backup-Env)': $152.09 (1.39%)
  Tag value 'billing$core-services': $92.09 (60.56%)
  Undefined: 39.44%
```
