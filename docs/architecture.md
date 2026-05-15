# CloudOps Assistant Architecture

The CloudOps Assistant is a containerized internal knowledge assistant. Users access a Streamlit frontend through an AWS Application Load Balancer. The load balancer serves the UI by default and routes API paths to a FastAPI backend running on ECS Fargate.

![CloudOps Assistant architecture](./cloudops-assistant-architecture.svg)

```mermaid
flowchart LR
  user["CloudOps user<br/>Browser"]
  github["GitHub repository<br/>Source + workflow"]
  actions["GitHub Actions<br/>OIDC, build, push, Terraform apply"]
  images["Docker images<br/>Backend and UI containers"]

  subgraph aws["AWS Cloud"]
    direction LR

    subgraph edge["Public access layer"]
      alb["Application Load Balancer<br/>HTTP :80"]
      uiRule["Default route<br/>/"]
      apiRule["API route<br/>/api/*, /health, /docs"]
    end

    subgraph compute["ECS Fargate cluster"]
      uiSvc["Streamlit UI service<br/>Container from UI ECR"]
      apiSvc["FastAPI service<br/>Container from API ECR"]
    end

    subgraph api["Application capabilities"]
      auth["Auth<br/>JWT login + bearer validation"]
      upload["Document upload<br/>.txt / .md / .log"]
      rag["RAG question answering<br/>Retrieve, chunk, rank, prompt"]
      feedback["Feedback capture<br/>Thumbs up/down"]
    end

    subgraph data["Data and AI services"]
      s3["Amazon S3 uploads bucket<br/>Encrypted document storage"]
      bedrock["Amazon Bedrock<br/>Claude model invocation"]
      dynamodb["Amazon DynamoDB<br/>Feedback table"]
      secrets["AWS Secrets Manager<br/>JWT secret + app password"]
      logs["Amazon CloudWatch Logs<br/>UI and API task logs"]
    end

    subgraph registry["Container registry"]
      apiEcr["Amazon ECR<br/>API image"]
      uiEcr["Amazon ECR<br/>UI image"]
    end

    iam["IAM roles and policies<br/>Task execution + app permissions"]
  end

  user -->|"Open app"| alb
  alb --> uiRule --> uiSvc
  alb --> apiRule --> apiSvc
  uiSvc -->|"Login, upload, chat, feedback"| apiSvc

  apiSvc --> auth
  apiSvc --> upload
  apiSvc --> rag
  apiSvc --> feedback

  auth -->|"Read credentials and signing key"| secrets
  upload -->|"PutObject / ListBucket"| s3
  rag -->|"List/Get documents"| s3
  rag -->|"InvokeModel"| bedrock
  feedback -->|"PutItem"| dynamodb

  uiSvc --> logs
  apiSvc --> logs
  iam -.-> uiSvc
  iam -.-> apiSvc
  iam -.-> s3
  iam -.-> bedrock
  iam -.-> secrets

  github --> actions
  actions --> images
  images -->|"Push API image"| apiEcr
  images -->|"Push UI image"| uiEcr
  apiEcr -->|"Task definition image"| apiSvc
  uiEcr -->|"Task definition image"| uiSvc

  classDef user fill:#f7f7f5,stroke:#4b5563,color:#111827,stroke-width:1px
  classDef edge fill:#e0f2fe,stroke:#0369a1,color:#082f49,stroke-width:1px
  classDef compute fill:#dcfce7,stroke:#15803d,color:#052e16,stroke-width:1px
  classDef app fill:#ede9fe,stroke:#6d28d9,color:#2e1065,stroke-width:1px
  classDef data fill:#fff7ed,stroke:#c2410c,color:#431407,stroke-width:1px
  classDef cicd fill:#fce7f3,stroke:#be185d,color:#500724,stroke-width:1px
  classDef iam fill:#fef9c3,stroke:#a16207,color:#422006,stroke-width:1px

  class user user
  class alb,uiRule,apiRule edge
  class uiSvc,apiSvc compute
  class auth,upload,rag,feedback app
  class s3,bedrock,dynamodb,secrets,logs data
  class github,actions,images,apiEcr,uiEcr cicd
  class iam iam
```

## Request Flow

1. The user opens the public ALB URL.
2. The ALB sends normal web traffic to the Streamlit UI service.
3. API paths are routed to the FastAPI service.
4. Users log in with app credentials and receive a JWT.
5. Uploaded documents are versioned by the API and stored in the encrypted S3 uploads bucket.
6. Chat requests retrieve document text from S3, chunk and rank candidate snippets, then invoke Amazon Bedrock.
7. Feedback is accepted by the API and written to DynamoDB.
8. UI and API task logs are shipped to CloudWatch Logs.

## Implementation Notes

- Terraform defines the ALB, ECS cluster, ECS services, task definitions, ECR repositories, S3 bucket, Secrets Manager secrets, IAM roles, and CloudWatch log group.
- The FastAPI application uses JWT authentication for `/api/upload`, `/api/documents`, `/api/chat`, and `/api/feedback`.
- The feedback code expects a DynamoDB table named `cloudops-feedback` by default, but the table is not currently declared in `terraform/main.tf`.
- The repository contains a GitHub Actions deployment workflow that authenticates to AWS with OIDC, builds and pushes backend and UI Docker images, applies Terraform, and forces ECS service deployments.
