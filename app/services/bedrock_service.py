import os
import json
from typing import List, Dict

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "anthropic.claude-3-haiku-20240307-v1:0"
)

bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)


def call_bedrock(prompt: str) -> str:
    """
    Call Anthropic Claude 3 Haiku on Amazon Bedrock using the Messages API format.
    """

    print(f"[BEDROCK] AWS_REGION={AWS_REGION}", flush=True)
    print(f"[BEDROCK] BEDROCK_MODEL_ID={BEDROCK_MODEL_ID}", flush=True)

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 600,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response["body"].read())
        content = response_body.get("content", [])

        if not content:
            return "No response from model."

        text_blocks = [
            block.get("text", "")
            for block in content
            if block.get("type") == "text"
        ]

        final_text = "\n".join(text_blocks).strip()

        if not final_text:
            return "Model returned an empty text response."

        return final_text

    except ClientError as e:
        print("[BEDROCK ERROR]", e, flush=True)
        return f"Bedrock error: {str(e)}"
    except Exception as e:
        print("[UNEXPECTED ERROR]", e, flush=True)
        return f"Unexpected error calling Bedrock: {str(e)}"


def build_prompt(question: str, ranked_chunks: List[Dict[str, str]]) -> str:
    """
    Build a simple RAG prompt using retrieved document chunks.
    """

    context = "\n\n".join(
        f"Source: {item['filename']}\n\n{item['chunk']}"
        for item in ranked_chunks
    )

    return f"""
You are a senior CloudOps assistant.

Answer the question using ONLY the provided context.

If the context does not contain the answer, respond with:
"I could not find the answer in the uploaded documents."

Provide practical DevOps-focused answers.

Context:
{context}

Question:
{question}

Answer:
""".strip()