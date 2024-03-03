import json
import boto3

# Initialize the AWS Boto3 client for the Amazon Titan model
client = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    # Extract the prompt from the event that triggered the Lambda function
    prompt_data = f"Command: {event['prompt']}"

    # Define the payload with the input text and text generation configuration
    payload = {
        "inputText": prompt_data,
        "textGenerationConfig": {
            "maxTokenCount": 3999,
            "stopSequences": [],
            "temperature": 0,
            "topP": 0.9
        }
    }

    # Serialize the payload to JSON format
    payload_json = json.dumps(payload)

    # Specify the model ID for the Amazon Titan model
    model_id = 'amazon.titan-text-lite-v1'

    try:
        # Invoke the model with the payload
        response = client.invoke_model(
            body=payload_json,
            contentType='application/json',
            accept='application/json',
            modelId=model_id
        )

        # Read the binary response content
        response_content = response['body'].read()

        # Convert the binary content to a string and then load it as JSON
        response_data = json.loads(response_content)

        # You should tailor the next line to the structure of your specific response:
        # Extract the generated text from the response, if available
        outputText = response_data.get('results', 'No generated text found')[0]

        # Return the generated text and the input event as the response
        return {
            'statusCode': 200,
            'body': outputText['outputText'],
            'input_event': event  # Return the input event for debugging purposes
        }

    except Exception as e:
        # Log and return the error information
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': str(e)
        }