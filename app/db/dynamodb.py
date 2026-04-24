import os
import uuid
from datetime import datetime, timezone

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "cloudops-feedback")


def _get_table():
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    return dynamodb.Table(TABLE_NAME)


def save_feedback(question: str, answer: str, rating: str, username: str) -> dict:
    item = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "username": username,
        "question": question,
        "answer": answer,
        "rating": rating,
    }

    table = _get_table()
    table.put_item(Item=item)
    return item