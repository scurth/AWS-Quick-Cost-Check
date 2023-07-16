# AWS-Quick-Cost-Check

**Script Description**: This script allows you to quickly retrieve on overview of the costs per AWS account

## Prerequisites

- Python 3.x
- AWS CLI installed and configured

## Usage

```
python usage.py [-h] [-d DAYS] [-ic] [-p PROFILE]
```

## Command-line Arguments

The script supports the following command-line arguments:

- `-h, --help`: Show the help message and exit.
- `-d DAYS, --days DAYS`: Number of days to go back (default: 1).
- `-ic, --ignore-credits`: Ignore credits (optional).
- `-p PROFILE, --profile PROFILE`: AWS profile to use (default: 'default').

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
Create a profile using the security credentials of that user.

## License

[MIT License](LICENSE)
