# AWS-Quick-Cost-Check

**Script Description**: This script allows you to quickly retrieve on overview of the costs per AWS account

## Prerequisites

- Python 3.x
- AWS CLI installed and configured

## Usage

```
python usage.py [-h] [-d DAYS] [-ic] [-p PROFILE] [-v]
```

## Command-line Arguments

The script supports the following command-line arguments:

- `-h, --help`: Show the help message and exit.
- `-d DAYS, --days DAYS`: Number of days to go back (default: 1).
- `-ic, --ignore-credits`: Ignore credits (optional).
- `-p PROFILE, --profile PROFILE`: AWS profile to use (default: 'default').
- `-v, --visualize`: If this flag is present, the script will display the cost data as a histogram-like visualization in the console.

### Histogram Visualization

When the `-v` or `--visualize` flag is used, the script will display an ASCII histogram in the console for each AWS account. Each bar in the histogram represents a different service, and the length of the bar is proportional to the cost of that service. Services are sorted by cost in descending order.

Here's an example of what the histogram might look like:

```
Linked Account: 123456789012 (My AWS Account)

AmazonEC2          | ========================== 120.00
AmazonRDS          | ============= 60.00
AmazonS3           | ====== 30.00
AWSCloudTrail      | === 15.00
```

In this example, the AWS account 'My AWS Account' has four services with costs. Amazon EC2 has the highest cost, followed by Amazon RDS, Amazon S3, and AWS CloudTrail. The length of each bar is proportional to the cost of the corresponding service.

## Examples

1. Run the script with default values:
```
python usage.py
```

2. Specify the number of days to go back:
```
python usage.py -d 7
```

3. Ignore credits:
```
python usage.py -ic
```

4. Specify the AWS profile:
```
python usage.py -p myprofile
```

## AWS IAM permissions
Create an IAM user with these permissions.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CostExplorerAndOrganizationsPermissions",
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "organizations:DescribeAccount"
            ],
            "Resource": [
                "arn:aws:ce:*:ACCOUNT_ID:*",
                "arn:aws:organizations::ACCOUNT_ID:account/*"
            ]
        }
    ]
}
```
## License

[MIT License](LICENSE)
