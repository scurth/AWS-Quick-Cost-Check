# AWS-Quick-Cost-Check

**Script Description**: This script allows you to quickly retrieve on overview of the costs per AWS account

## Prerequisites

- Python 3.x
- AWS CLI installed and configured

## Get a general Usage Overview

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

### AWS IAM permissions
Create an IAM user with these permissions.

```json
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

## AWS Unattached EBS Volumes Finder

This Python script uses the Boto3 AWS SDK to find all unattached EBS volumes in your AWS account. It groups these volumes by region and sorts them within each group by size (as a proxy for price) in descending order. The script also outputs the AWS account number and account alias.

### Requirements

- Python 3.6 or later
- Boto3 library (`pip install boto3`)

### AWS Permissions

The script requires the following AWS IAM permissions:

- `ec2:DescribeVolumes`
- `ec2:DescribeRegions`
- `iam:ListAccountAliases`
- `sts:GetCallerIdentity`

Here is an example of the IAM policy in JSON format:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeRegions",
                "iam:ListAccountAliases",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

### Usage

You can run this script from the command line with your AWS profile name as an argument:

```bash
python ebs-unattached.py --profile myprofile
```

Replace `myprofile` with your AWS profile name.

### Output

The script will output the AWS account number and alias, followed by the unattached EBS volumes grouped by region. For each region, it will also output the number of unattached volumes. Within each region group, the volumes are sorted by size in descending order.

```
Account ID: 123456789012, Account Alias: my-account-alias

Region: us-east-1 (2 unattached volumes)
  Volume ID: vol-0abcd1234efgh5678, Size: 100 GB
  Volume ID: vol-0ijkl9012mnop3456, Size: 50 GB

Region: us-west-1 (1 unattached volumes)
  Volume ID: vol-0qrst7890uvwx1234, Size: 200 GB

Region: eu-west-1 (0 unattached volumes)

Region: ap-southeast-1 (3 unattached volumes)
  Volume ID: vol-0cdef4567opqr8910, Size: 150 GB
  Volume ID: vol-0stuv1121wxyz3434, Size: 100 GB
  Volume ID: vol-0abcd1234efgh5678, Size: 50 GB
```

## License

[MIT License](LICENSE)
