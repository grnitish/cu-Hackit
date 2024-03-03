import json
import boto3

# Initialize the client for Lambda outside the handler
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Define the ARNs and corresponding function names you want to invoke
    function_details = {
        'claude': 'arn:aws:lambda:us-west-2:611478881374:function:claude',
        'llama': 'arn:aws:lambda:us-west-2:611478881374:function:llama',
        'titan': 'arn:aws:lambda:us-west-2:611478881374:function:titan'
        # Add more functions if needed
    }

    # Define the payload you want to send
    payload = {
        "prompt": event.get('prompt', 'Give me a Fun fact about Clemson')
    }

    responses = {}

    # Iterate over the function details and invoke each one synchronously
    for function_name, function_arn in function_details.items():
        try:
            response = lambda_client.invoke(
                FunctionName=function_arn,
                InvocationType='RequestResponse',  # Invoke synchronously
                Payload=json.dumps(payload)
            )
            
            # Read the response (since it's synchronous invocation)
            response_payload = json.loads(response['Payload'].read())
            
            # You might want to adjust the following line if the response structure is different
            responses[function_name] = response_payload
            
        except Exception as e:
            print(f"Error invoking {function_name}: {str(e)}")
            responses[function_name] = {'error': str(e)}

    # Return the responses from the invoked functions
    return {
        'statusCode': 200,
        'body': json.dumps(responses)
    }
