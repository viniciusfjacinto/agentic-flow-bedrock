import boto3
import time
import os
from dotenv import load_dotenv
load_dotenv()

flow_alias_identifier = os.getenv('flow_alias_identificar')
flow_identifier = os.getenv('flow_identifier')
client = boto3.client('bedrock-agent-runtime',region_name = os.getenv('region_name'))

def invoke_flow(input_text, timeout=30):  # 5 minutes timeout
    response = client.invoke_flow(
        flowAliasIdentifier=flow_alias_identifier,
        flowIdentifier=flow_identifier,
        inputs=[
            {
                'content': {
                    'document': input_text
                },
                  'nodeName': 'FlowInputNode',
                'nodeOutputName': 'document'
            },
        ]
    )

    event_stream = response["responseStream"]
    result = ""
    start_time = time.time()
    for event in event_stream:
        if time.time() - start_time > timeout:
            print(f"Flow invocation timed out after {timeout} seconds.")
            return None
        if "flowOutputEvent" in event:
            result += event["flowOutputEvent"]["content"]["document"]

    return result
    