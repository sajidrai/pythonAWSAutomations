# run below script on my laptop
# export AWS_PROFILE=<<profile name>>
# python3 lambda-power-tuner.py

import boto3
import csv
import json
import time

# Initialize AWS clients
lambda_client = boto3.client("lambda")
sf_client = boto3.client("stepfunctions")

# Constants
LAMBDA_EXCLUDE_PREFIX = "serverlessrepo-aws-lambda-power-tuning"
STATE_MACHINE_PREFIX = "powerTuningStateMachine"
CSV_FILENAME = "lambda_power_tuner_results.csv"
POLL_INTERVAL = 10  # seconds between status checks
TIMEOUT = 600       # maximum wait time in seconds for each execution

def list_lambda_functions():
    """
    Read-only operation: Lists Lambda functions without any modifications
    Excludes only power tuner functions
    """
    functions = []
    paginator = lambda_client.get_paginator("list_functions")
    for page in paginator.paginate():
        for fn in page["Functions"]:
            # Skip only power tuner functions
            if not fn["FunctionName"].startswith(LAMBDA_EXCLUDE_PREFIX):
                functions.append(fn)
    
    return functions

def get_power_tuner_state_machine():
    """
    Read-only operation: Finds the Power Tuner state machine
    """
    paginator = sf_client.get_paginator("list_state_machines")
    for page in paginator.paginate():
        for sm in page["stateMachines"]:
            if sm["name"].startswith(STATE_MACHINE_PREFIX):
                return sm["stateMachineArn"]
    return None

def start_tuning_execution(state_machine_arn, lambda_function_arn):
    """
    Starts a safe tuning execution with limited scope
    """
    input_payload = {
        "lambdaARN": lambda_function_arn,
        "strategy": "cost",              
        "autoOptimize": False,           
        "payload": {},                   
        "powerValues": [128, 256, 512, 1024, 2048, 3008],  
        "num": 10,                        
        "parallelInvocation": True,      
        "output": {
            "data": "true",
            "visualization": "true"
        }
    }
    
    print(f"Starting safe power tuning for {lambda_function_arn}")
    print(f"Test configuration: {json.dumps(input_payload, indent=2)}")
    
    response = sf_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(input_payload)
    )
    return response["executionArn"]

def extract_visualization_url(output_json):
    """
    Extract visualization URL from the execution output
    """
    try:
        # Parse the output JSON
        if isinstance(output_json, str):
            output_data = json.loads(output_json)
        else:
            output_data = output_json

        # Try different possible paths to visualization URL
        if "visualization" in output_data:
            return output_data["visualization"]
        elif "stateMachine" in output_data and "visualization" in output_data["stateMachine"]:
            return output_data["stateMachine"]["visualization"]
        else:
            return "Visualization URL not found in output"
    except Exception as e:
        print(f"Error extracting visualization URL: {str(e)}")
        return "Error extracting visualization URL"

def wait_for_execution(execution_arn):
    """
    Read-only operation: Monitors execution status
    """
    elapsed = 0
    while elapsed < TIMEOUT:
        response = sf_client.describe_execution(executionArn=execution_arn)
        status = response["status"]
        if status in ["SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"]:
            return response
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
    raise TimeoutError(f"Execution {execution_arn} did not complete within timeout.")

def main():
    print("Starting Lambda Power Tuning Analysis (Read-Only Mode)")
    print("Note: This script will NOT modify any Lambda configurations")
    
    # List all relevant Lambda functions
    lambda_functions = list_lambda_functions()
    print(f"Found {len(lambda_functions)} Lambda functions to analyze.")

    # Get the state machine ARN for the Power Tuner
    state_machine_arn = get_power_tuner_state_machine()
    if not state_machine_arn:
        print(f"No state machine found with prefix '{STATE_MACHINE_PREFIX}'. Exiting.")
        return
    print(f"Using Power Tuner state machine: {state_machine_arn}")

    # Prepare CSV output
    results = []
    results.append([
        "LambdaFunctionName", 
        "CurrentMemory", 
        "PowerTunerVisualizationURL", 
        "Status"
    ])

    # Iterate over each Lambda function
    for fn in lambda_functions:
        function_name = fn["FunctionName"]
        lambda_arn = fn["FunctionArn"]
        current_memory = fn.get("MemorySize", "Unknown")
        
        print(f"\nAnalyzing {function_name} (Current Memory: {current_memory}MB)")

        try:
            execution_arn = start_tuning_execution(state_machine_arn, lambda_arn)
            print(f"  Execution started: {execution_arn}")
            execution_result = wait_for_execution(execution_arn)
            
            if execution_result["status"] == "SUCCEEDED":
                output = json.loads(execution_result["output"])
                visualization_url = extract_visualization_url(output)
                print(f"  Analysis succeeded. Visualization URL: {visualization_url}")
                status = "Success"
            else:
                visualization_url = f"Execution ended with status: {execution_result['status']}"
                print(f"  Analysis failed. {visualization_url}")
                status = f"Failed: {execution_result['status']}"

        except Exception as e:
            visualization_url = f"Error: {str(e)}"
            print(f"  Error analyzing function {function_name}: {str(e)}")
            status = f"Error: {str(e)}"

        results.append([
            function_name,
            current_memory,
            visualization_url,
            status
        ])

    # Write results to CSV
    with open(CSV_FILENAME, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)
    print(f"\nResults written to {CSV_FILENAME}")
    print("Note: No Lambda configurations were modified during this analysis")

if __name__ == "__main__":
    main()
