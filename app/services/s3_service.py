import os
from io import BytesIO
from typing import List

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client("s3", region_name=AWS_REGION)


def upload_file_to_s3(file_name: str, content: bytes, content_type: str = "text/plain") -> str:
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=BytesIO(content),
        ContentType=content_type,
    )
    return file_name


def list_s3_documents() -> List[str]:
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
    contents = response.get("Contents", [])
    return [obj["Key"] for obj in contents]


def get_s3_document_text(key: str) -> str:
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
    return response["Body"].read().decode("utf-8", errors="ignore")