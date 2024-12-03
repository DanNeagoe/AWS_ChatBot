import boto3
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.titan-text-premier-v1:0"

class ConversationMemory:
    def __init__(self, max_token_limit=1024):
        self.max_token_limit = max_token_limit
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": [{"text": content}]})

    def get_summary(self):
        summary = []
        for msg in self.messages:
            for content in msg["content"]:
                summary.append(f"{msg['role'].capitalize()}: {content['text']}")
        return "\n".join(summary)

def create_memory(max_token_limit=1024):
    return ConversationMemory(max_token_limit=max_token_limit)

def get_chat_response(user_message, memory):
    try:
        memory.add_message("user", user_message)
        conversation = memory.messages
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": memory.max_token_limit,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9
            },
            additionalModelRequestFields={}
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        memory.add_message("assistant", response_text)
        return response_text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return None

