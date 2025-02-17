
# AWS Lambda Power Tuner Automation

## Overview
AWS Lambda Power Tuner is a powerful tool that helps optimize Lambda functions by automatically evaluating different memory configurations. This automation script helps you find the optimal memory settings for your Lambda functions based on performance and cost metrics.

The tool analyzes each Lambda function's performance across various memory settings and generates recommendations to help you:
- Optimize cost efficiency
- Improve execution time
- Find the best balance between cost and performance

## Prerequisites

1. AWS Lambda Power Tuner must be deployed in your AWS account. Follow the deployment instructions in our [detailed runbook](https://docs.google.com/document/d/15K2z7k28cuqq4N7m9-IDtIAL-WQsicv4fOu3Otjxgzg/edit?usp=sharing).

2. AWS CLI configured with appropriate permissions
3. Python 3.x installed

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate to the project directory:
```bash
cd lambda-power-tuner
```

## Configuration

Configure your AWS profile by setting the environment variable:
```bash
export AWS_PROFILE=<your-profile-name>
```

## Usage

Run the power tuner script:
```bash
python3 lambda-power-tuner.py
```

## Output

The script generates a CSV file containing memory optimization recommendations for each Lambda function in your AWS account. File contains
- lambda function name 
- power tuner memory recommendation link

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

