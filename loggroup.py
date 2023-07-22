import boto3
import argparse
from datetime import datetime

# Add command line argument parsing
parser = argparse.ArgumentParser(description='AWS profile')
parser.add_argument('-p', '--profile', type=str, help='AWS profile', default='default')
parser.add_argument('--show-last-log-entry', action='store_true', help='Show the date of the last log entry in each log group')
parser.add_argument('--show-without-retention', action='store_true', help='Only show log groups without a retention policy')
args = parser.parse_args()

# Set AWS profile and region
session = boto3.Session(profile_name=args.profile, region_name='us-east-1')

# Create CloudWatch client
cw = session.client('logs')

# Get all log groups
paginator = cw.get_paginator('describe_log_groups')

for page in paginator.paginate():
    for log_group in page['logGroups']:
        # Check if retention is not set
        if args.show_without_retention and 'retentionInDays' in log_group:
            continue

        log_group_name = log_group['logGroupName']

        # Get all log streams in the log group
        log_streams_paginator = cw.get_paginator('describe_log_streams')

        log_streams = []
        last_timestamps = []
        for log_streams_page in log_streams_paginator.paginate(logGroupName=log_group_name):
            log_streams.extend(log_streams_page['logStreams'])
            for log_stream in log_streams_page['logStreams']:
                if 'lastEventTimestamp' in log_stream:
                    last_timestamps.append(log_stream['lastEventTimestamp'])

        # Print the log group name and number of log streams
        print(f"\nLog Group: {log_group_name}")
        print(f"Number of Log Streams: {len(log_streams)}")

        # If the --show-last-log-entry flag is present and there are log entries, print the last log entry
        if args.show_last_log_entry and last_timestamps:
            # Convert the timestamps to readable dates and sort them
            last_dates = sorted([datetime.fromtimestamp(ts / 1000) for ts in last_timestamps])
            print(f"Last Log Entry: {last_dates[-1]}")
