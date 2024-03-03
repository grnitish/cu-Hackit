import json
import boto3

# Initialize the AWS Boto3 client for bedrock-runtime
client = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    # Extract the prompt from the event that triggered the Lambda function
    prompt = event.get('prompt', 'Give me a fun fact about Clemson')

    # Define the payload to send to the model, using the prompt and other parameters
    payload = {
        "prompt": f"Human: {prompt}\n\nAssistant:",
        "temperature": 0.9,
        "max_tokens_to_sample": 4096
    }

    payload_json = json.dumps(payload)

    # Specify the model ID for the Claude model
    model_id = 'anthropic.claude-v2'

    try:
        # Invoke the Claude model with the payload
        response = client.invoke_model(
            body=payload_json,
            contentType='application/json',
            accept='application/json',
            modelId=model_id
        )

        response_content = response['body'].read()
        response_data = json.loads(response_content)
        completion_text = response_data.get('completion', 'No completion text found')

        # Return the completion text and the input event as the response
        return {
            'statusCode': 200,
            'body': completion_text,
            'input_event': event  # Return the input event for debugging purposes
        }

    except Exception as e:
        # Log and return the error information
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': str(e)
        }