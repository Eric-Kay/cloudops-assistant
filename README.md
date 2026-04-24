# CloudOps Assistant

A production-style starter project for an internal CloudOps knowledge assistant.

## Features
- JWT authentication
- Upload documents
- Ask questions against uploaded documents
- Simple ranking of matching chunks
- Feedback logging
- Streamlit frontend
- Docker support
- GitHub Actions starter workflow

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload