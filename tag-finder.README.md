# Tag Finder

The `tag-finder.py` script is a utility to find AWS resources based on tags.
It can be used to find resources that either have a specific tag key or are missing a specific tag key. Additionally, it provides an option to exclude default AWS resources such as VPCs, subnets, security groups, and network insights access scopes.

## Prerequisites

- Python 3.x
- Boto3 library (can be installed via pip)

## Usage

```bash
python tag-finder.py [-p PROFILE] [--missing-tag MISSING_TAG] [--with-tag WITH_TAG] [--exclude-defaults]
```

### Arguments

- `-p`, `--profile`: Specify the AWS profile to use (default is "default").
- `--missing-tag`: Find resources that do NOT have the specified tag key.
- `--with-tag`: Find resources that HAVE the specified tag key and group them by its value.
- `--exclude-defaults`: Exclude default AWS resources like VPCs, subnets, security groups, and network insights access scopes.

## IAM Permissions

To run the script, the following IAM permissions are required:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "tag:GetResources",
                "ec2:DescribeInstances",
                "s3:ListAllMyBuckets",
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
        }
    ]
}
```

## Example

To find all resources that do not have the tag "billing" and exclude default AWS resources:

```bash
python tag-finder.py --missing-tag billing --exclude-defaults
```

To find all resources that have the tag "billing":

```bash
python tag-finder.py --with-tag billing
```

## Notes

- The script provides output grouped by region and then by the tag value (if the `--with-tag` option is used).
- It's essential to ensure the AWS profile used has the necessary permissions to retrieve the desired resources.

## Sample Outputs

### Using `--with-tag`

When searching for resources with a specific tag, the script will group results by region and then by the value of the specified tag.

Command:
```bash
python tag-finder.py --with-tag billing
```

Sample Output:
```
Region: us-east-1

Resources with the tag: billing

Tag Value: ProjectA
Resource ARN: arn:aws:s3:::projecta-bucket
Resource ARN: arn:aws:ec2:us-east-1:123456789012:instance/i-0abcd1234efgh5678

Tag Value: ProjectB
Resource ARN: arn:aws:ec2:us-east-1:123456789012:instance/i-0abcd1234ijklm9012

Region: us-west-1

Resources with the tag: billing

Tag Value: ProjectA
Resource ARN: arn:aws:s3:::projecta-archive-bucket
```

### Using `--missing-tag`

When searching for resources missing a specific tag, the script will group results by region.

Command:
```bash
python tag-finder.py --missing-tag billing --exclude-defaults
```

Sample Output:
```
Region: us-east-1

Resources missing the tag: billing
Resource ARN: arn:aws:rds:us-east-1:123456789012:db:mysql-db
Resource ARN: arn:aws:s3:::unlabeled-bucket

Region: us-west-2

Resources missing the tag: billing
Resource ARN: arn:aws:lambda:us-west-2:123456789012:function:my-function
```
