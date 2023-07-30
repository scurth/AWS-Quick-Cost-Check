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

## AWS CloudWatch Log Groups Script

This script uses the AWS SDK for Python (Boto3) to interact with the AWS CloudWatch Logs API.
It retrieves information about AWS CloudWatch Log Groups and has the ability to filter and format the output based on command-line arguments.

### Usage
The script supports the following command-line arguments:

-p or --profile: The AWS profile to use. Default is 'default'.  
--show-last-log-entry: Show the date of the last log entry in each log group.  
--show-without-retention: Only show log groups without a retention policy.

Here's how to run the script:

```bash
python script.py --profile your_profile --show-last-log-entry --show-without-retention
```

This will output information about AWS CloudWatch Log Groups that don't have a retention policy set and will include the date of the last log entry in each log group.

### Sample Output
```bash
Log Group: /aws/lambda/myLambdaFunction
Number of Log Streams: 8
Last Log Entry: 2023-07-22 13:14:15.123456

Log Group: /aws/lambda/anotherLambdaFunction
Number of Log Streams: 3
Last Log Entry: 2023-07-21 18:20:30.123456
```

### IAM Permissions
The script uses the following AWS CloudWatch Logs API actions, so your IAM policy should allow these:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams"
            ],
            "Resource": "*"
        }
    ]
}
```

## Sure, here's a `README.md` file for the provided Python script:

## Unattached Elastic IPs Finder

This Python script helps you find unattached Elastic IPs (EIPs) in your AWS account. It uses the Boto3 library to interact with AWS services, so you need to have the Boto3 library installed. Make sure you have configured your AWS credentials properly using either environment variables or AWS CLI.

### Prerequisites

- Python 3.x
- Boto3 library (can be installed via `pip install boto3`)

### Usage

1. Clone this repository or download the `eip-unattached.py` script.

2. Install the required dependencies using pip:

   ```bash
   pip install boto3
   ```

3. Run the script:

   ```bash
   python eip-unattached.py --profile YOUR_AWS_PROFILE_NAME
   ```

   Replace `YOUR_AWS_PROFILE_NAME` with the AWS CLI profile you want to use for the AWS API calls. The profile should have the necessary permissions to list EC2 instances and Elastic IPs.

### How it works

The script performs the following actions:

1. Retrieves your AWS account ID and account alias using the provided AWS CLI profile.

2. Fetches all available AWS regions using the EC2 client from the `us-east-1` region (the default region).

3. Iterates through each region to find unattached Elastic IPs.

4. Prints the details of all unattached Elastic IPs found, including the public IP and allocation ID.

### IAM Permissions
The script uses the following AWS CloudWatch Logs API actions, so your IAM policy should allow these:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRegions",
                "ec2:DescribeAddresses",
                "sts:GetCallerIdentity",
                "iam:ListAccountAliases"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        }
    ]
}
```
### New AWS IPAM Service
AWS has introduced a new service called IP Address Management (IPAM), which aims to help you better manage your IP address allocations in AWS.
You can read more about the service in the following links:

- [AWS IP Address Management (IPAM) Blog Post](https://aws.amazon.com/de/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)
- [AWS IPAM Documentation](https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html)

With the IPAM service, you can gain insights into your IP allocations and identify any unattached Elastic IPs more efficiently.

### Note

The script uses the `describe_addresses` method from the EC2 client to get information about Elastic IPs in each region.
It filters out the Elastic IPs that are not attached to any EC2 instance.

Remember to configure your AWS CLI profile correctly before running the script.
The profile should have the necessary permissions to list Elastic IPs and EC2 instances in all the regions of your AWS account.

## License

[MIT License](LICENSE)
