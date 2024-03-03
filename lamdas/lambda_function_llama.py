import json
import boto3

# Initialize the bedrock-runtime client
client = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    # Retrieve the prompt from the event
    prompt = event.get('prompt', 'Give me a fun fact about Clemson')
    prompt_data = f"Command: {event['prompt']}"

    # Set the model ID for llama
    model_id = 'meta.llama2-13b-chat-v1'
    
    # Prepare the payload with the prompt and generation settings
    payload = json.dumps({
        'prompt': prompt_data,
        'max_gen_len': 512,
        'top_p': 0.9,
        'temperature': 0.2
    })

    try:
        # Invoke the llama model
        response = client.invoke_model(
            body=payload,
            contentType='application/json',
            accept='application/json',
            modelId=model_id
        )

        # Read and decode the response
        response_byte = response['body'].read()
        response_string = json.loads(response_byte)
        generation = response_string.get('generation', '')  # Assuming 'completion' key in response

        # Return the generated text and the input event as a part of the response
        return {
            'statusCode': 200,
            'body': generation,
            'test': event
        }

    except Exception as e:
        # Print and return the error if any occurs
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': str(e)
        }