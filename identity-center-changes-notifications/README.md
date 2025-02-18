# AWS Identity Center Change Monitor

This CloudFormation stack deploys a solution to monitor changes in AWS Identity Center (formerly AWS SSO) and send real-time notifications via SNS.

## 🎯 Features

- Real-time monitoring of AWS Identity Center changes
- Comprehensive event tracking including:
  - User management (create, update, delete)
  - Group management (create, update, delete)
  - Permission set changes
  - Group membership modifications
  - Account assignments
- Detailed notifications with:
  - Action performed
  - Who performed it
  - Source IP address
  - Timestamp
  - Complete request parameters

## 🏗 Architecture

The solution consists of:
- **EventBridge Rule**: Monitors AWS Identity Center API calls
- **Lambda Function**: Processes events and formats notifications
- **SNS Topic**: Delivers notifications to subscribers
- **IAM Role**: Provides necessary permissions

## 📋 Prerequisites

- AWS Account with Identity Center configured
- Permissions to create:
  - Lambda functions
  - SNS topics
  - IAM roles
  - EventBridge rules
- List of email addresses that should receive notifications

## 🚀 Deployment

### Option 1: AWS Console Deployment

1. Download the CloudFormation template (`identity-center-changes-notifications.yaml`) to your local machine

2. Navigate to AWS CloudFormation:
   - Log into the AWS Management Console
   - Go to CloudFormation service
   - Click "Create stack" (with new resources)

3. Upload the template:
   - Choose "Upload a template file"
   - Click "Choose file"
   - Select the downloaded `identity-center-changes-notifications.yaml`
   - Click "Next"

4. Configure stack:
   - Stack name: `identity-center-monitor` (or your preferred name)
   - Click "Next"

5. Configure stack options:
   - Leave defaults or configure as needed
   - Click "Next"

6. Review:
   - Check the "I acknowledge that AWS CloudFormation might create IAM resources" box
   - Click "Create stack"
   - Wait for stack creation to complete (Status: CREATE_COMPLETE)

### Option 2: AWS CLI Deployment

1. Clone this repository
2. Deploy using CLI:

```bash
aws cloudformation create-stack \
  --stack-name identity-center-monitor \
  --template-body file://identity-center-changes-notifications.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

3. **Required Post-Deployment Steps for Email Notifications**:
   
   a. Navigate to SNS Topic:
   - Go to the AWS SNS console
   - Find the topic named "IdentityCenterAlerts"

   b. Add Email Subscribers:
   - Click "Create subscription"
   - Protocol: Choose "Email"
   - Endpoint: Enter the email address
   - Click "Create subscription"
   - Repeat for each email address that should receive notifications

   c. Confirm Subscriptions:
   - Each subscriber will receive a confirmation email
   - **Important**: Recipients MUST click the "Confirm subscription" link in the email
   - Without confirmation, subscribers will not receive notifications
   - The confirmation link expires after 3 days

   d. Verify Subscriptions:
   - Return to the SNS topic in AWS Console
   - Check that subscriptions status shows as "Confirmed"
   - Test the notification system by making a small change in Identity Center

## 🎯 Monitored Events

The solution monitors the following Identity Center operations:

### User Management
- CreateUser
- UpdateUser
- DeleteUser

### Group Management
- CreateGroup
- UpdateGroup
- DeleteGroup
- AddMemberToGroup
- RemoveMemberFromGroup

### Permission Sets
- CreatePermissionSet
- UpdatePermissionSet
- DeletePermissionSet
- AttachManagedPolicyToPermissionSet
- DetachManagedPolicyFromPermissionSet

### Account Assignments
- CreateAccountAssignment
- DeleteAccountAssignment

## 📬 Notification Format

Notifications will be sent to all confirmed email subscribers and include:
```
🔹 AWS Identity Center Change Detected
--------------------------------------------
🛠 Action: [Event Name]
🔍 Event Source: [Service Name]
⏰ Time: [Timestamp]
👤 Performed By: [IAM User/Role]
🌐 IP Address: [Source IP]
📝 Request Parameters: [Detailed Changes]
--------------------------------------------
```

## 🔍 Stack Outputs

The stack provides these outputs:
- `SNSTopicARN`: ARN of the SNS topic for alerts
- `LambdaFunctionName`: Name of the monitoring Lambda function
- `EventBridgeRuleName`: Name of the EventBridge rule

## 🧹 Cleanup

To remove all resources:

```bash
aws cloudformation delete-stack --stack-name identity-center-monitor
```

## ⚠️ Important Notes

- **Email Subscription Requirements**:
  - Each recipient must confirm their subscription
  - Unconfirmed subscriptions will not receive notifications
  - Confirmation links expire after 3 days
  - You can resubscribe if confirmation expires
- The Lambda function has a 10-second timeout
- Events are processed in real-time
- All Identity Center API calls are logged and monitored
- Notifications include the IP address of the user making changes

## 🔒 Security Considerations

- All resources use least-privilege permissions
- Lambda function logs are stored in CloudWatch Logs
- SNS topic only allows authorized publishers
- EventBridge rule filters for specific Identity Center events
- Email notifications are not encrypted; sensitive data should be accessed in AWS Console

## 📚 Additional Resources

- [AWS Identity Center Documentation](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [AWS EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/what-is-amazon-eventbridge.html)
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
