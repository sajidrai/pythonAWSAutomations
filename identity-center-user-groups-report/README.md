# AWS IAM Identity Center User & Groups Report Generator

This CloudFormation stack automates the generation and distribution of AWS IAM Identity Center (formerly AWS SSO) users and groups reports. The report is generated weekly and distributed via email through SNS.

## Features

- Weekly automated report generation
- Report includes:
  - User details (username, email)
  - Group memberships
  - Total user and group counts
- CSV file stored in S3
- Email notification with:
  - Formatted table of users and groups
  - Link to download CSV report
  - Summary statistics

## Prerequisites

- AWS Account with IAM Identity Center configured
- Permissions to create:
  - Lambda functions
  - S3 buckets
  - SNS topics
  - IAM roles
  - CloudWatch Events rules

## Deployment

1. Clone this repository
2. Deploy the CloudFormation stack:

```bash
aws cloudformation create-stack \
  --stack-name iam-identity-center-report \
  --template-body file://iam-report-stack.yaml \
  --parameters \
    ParameterKey=S3BucketName,ParameterValue=your-bucket-name \
    ParameterKey=SNSTopicName,ParameterValue=your-topic-name \
    ParameterKey=ScheduleExpression,ParameterValue="cron(0 0 ? * MON *)" \
  --capabilities CAPABILITY_IAM
```

3. After stack creation, set up email subscription:
   - Go to the AWS SNS console
   - Find the topic created by the stack (name specified in `SNSTopicName` parameter)
   - Click "Create subscription"
   - Protocol: Email
   - Enter the email address where you want to receive reports
   - Click "Create subscription"
   - **Important:** Check your email and confirm the subscription by clicking the link in the confirmation email

## Stack Resources

The stack creates the following resources:

- **S3 Bucket**: Stores the CSV reports (auto-deleted after 90 days)
- **SNS Topic**: Handles email notifications
- **Lambda Function**: Generates and distributes the reports
- **IAM Role**: Provides necessary permissions to the Lambda function
- **CloudWatch Event Rule**: Triggers the Lambda function weekly

## Stack Outputs

The stack provides the following outputs:

- `S3Bucket`: Name of the S3 bucket storing reports
- `S3BucketArn`: ARN of the S3 bucket
- `SNSTopic`: ARN of the SNS topic
- `SNSTopicName`: Name of the SNS topic
- `LambdaFunction`: ARN of the Lambda function
- `LambdaFunctionName`: Name of the Lambda function
- `ScheduleExpression`: Schedule for report generation

## Report Schedule

By default, the report is generated weekly on Monday at midnight UTC. You can modify the schedule by changing the `ScheduleExpression` parameter during stack creation.

## Report Format

The email report includes:
1. CSV file download link
2. Report summary (total users, groups)
3. Formatted table with user details
4. Report retention information

## Cleanup

To remove all resources:

```bash
aws cloudformation delete-stack --stack-name iam-identity-center-report
```

## Note

- The CSV report link requires AWS Console access
- Reports are automatically deleted from S3 after 90 days
- Make sure to confirm the SNS email subscription to receive reports
