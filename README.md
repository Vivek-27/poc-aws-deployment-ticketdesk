# 🎫 TicketDesk — Cloud-Native AWS Deployment POC

> **Capstone POC — Deploy a Real Application on AWS**
> **Level:** Foundation
> **Stream:** Python / FastAPI
> **Application:** TicketDesk IT Support Ticket Tracker
> **Infrastructure:** AWS + Terraform
> **CI/CD:** GitHub Actions + AWS OIDC
> **Deployment Model:** Containerized, private ECS Fargate backend with CloudFront frontend

---

# 1. 📌 POC Overview

TicketDesk is an IT support ticket tracking application used as a practical AWS deployment project.

The purpose of this POC is **not to develop application features**. The application is provided as a working FastAPI application. The objective is to learn how to take an existing application and deploy it on AWS in a secure, repeatable, production-style architecture.

The POC covers:

* Containerization with Docker
* Amazon ECR
* Amazon ECS Fargate
* Application Load Balancer
* VPC and subnet design
* Public and private subnets
* Amazon RDS PostgreSQL
* AWS Secrets Manager
* AWS Systems Manager Parameter Store
* Amazon S3
* Amazon CloudFront
* AWS Lambda
* IAM roles and least privilege
* GitHub Actions CI/CD
* GitHub OIDC authentication
* CloudWatch logging and monitoring
* Terraform Infrastructure as Code
* Automated deployment
* Smoke testing
* Security and deployment readiness
* Cost management
* Complete infrastructure teardown and rebuild

The target outcome is:

> **A working application that can be deployed to AWS from code, without manually creating AWS resources, and can be destroyed and rebuilt from zero.**

---

# 2. 🎯 POC Objectives

The original POC is divided into two phases.

## Individual Phase — M0 to M5

Each developer independently deploys the application and builds the AWS foundation.

| Milestone | Objective                                                      |
| --------- | -------------------------------------------------------------- |
| M0        | Deploy application manually using AWS Console                  |
| M1        | Containerize application and push image to ECR                 |
| M2        | Recreate infrastructure completely using Terraform             |
| M3        | Add RDS database and secure configuration                      |
| M4        | Deploy frontend using S3 + CloudFront                          |
| M5        | Implement S3 presigned uploads and Lambda thumbnail generation |

## Pod Phase — M6 to M8

The team adds production-style operational capabilities.

| Milestone | Objective                                            |
| --------- | ---------------------------------------------------- |
| M6        | Build automated CI/CD pipeline                       |
| M7        | Add CloudWatch observability and alarms              |
| M8        | Harden, test, tag, measure cost, destroy and rebuild |

---

# 3. 🏗️ Final AWS Architecture

```text
                              ┌──────────────────────┐
                              │       Browser        │
                              └──────────┬───────────┘
                                         │
                                         │ HTTPS
                                         ▼
                              ┌──────────────────────┐
                              │     CloudFront       │
                              │       CDN            │
                              └──────────┬───────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │                               │
                         │ /api/*                        │ /*
                         ▼                               ▼
              ┌────────────────────┐          ┌────────────────────┐
              │ Application Load   │          │ Private S3         │
              │ Balancer           │          │ Frontend Bucket    │
              │ Public Subnets     │          │ OAC Protected      │
              └─────────┬──────────┘          └────────────────────┘
                        │
                        │ HTTP
                        ▼
              ┌────────────────────┐
              │   ECS Fargate      │
              │   FastAPI API      │
              │   Private Subnets  │
              └──────┬─────┬───────┘
                     │     │
              ┌──────┘     └────────────────┐
              │                             │
              ▼                             ▼
      ┌─────────────────┐          ┌────────────────────┐
      │ RDS PostgreSQL  │          │ Secrets Manager    │
      │ Private Subnet  │          │ DB Credentials     │
      └─────────────────┘          └────────────────────┘


Browser
   │
   │ Presigned URL
   ▼
┌────────────────────┐
│ S3 Upload Bucket   │
└─────────┬──────────┘
          │
          │ ObjectCreated
          ▼
┌────────────────────┐
│ Lambda             │
│ Thumbnail Generator│
│ Pillow             │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ thumbnails/        │
│ prefix in S3       │
└────────────────────┘
```

---

# 4. 🔄 Application Request Flow

## 4.1 Frontend Request

1. User opens the CloudFront URL.
2. CloudFront receives the request.
3. Static frontend files are served from the private S3 frontend bucket.
4. S3 is not publicly accessible.
5. CloudFront uses Origin Access Control to access the bucket.

---

## 4.2 API Request

For requests beginning with:

```text
/api/*
```

the request follows:

```text
Browser
   ↓
CloudFront
   ↓
Application Load Balancer
   ↓
ECS Fargate
   ↓
FastAPI
```

The ECS application runs inside private subnets.

The ALB is the public entry point for the backend.

---

## 4.3 Database Request

The application communicates with:

```text
ECS Fargate
      ↓
RDS PostgreSQL
```

The database is deployed inside private subnets and is not publicly accessible.

Database credentials are not stored in the source code.

The application retrieves the credentials at runtime using AWS Secrets Manager.

---

## 4.4 File Upload Flow

Attachments do not pass through the API server.

Instead:

```text
Browser
   │
   │ Request presigned URL
   ▼
FastAPI
   │
   │ Presigned URL
   ▼
Browser
   │
   │ Direct upload
   ▼
S3 Upload Bucket
   │
   │ ObjectCreated event
   ▼
Lambda
   │
   │ Resize using Pillow
   ▼
S3 thumbnails/
```

This reduces API bandwidth and CPU usage because the application never receives the file bytes.

The backend exposes:

```text
GET /api/tickets/{id}/presigned-url
```

for generating the temporary upload URL.

---

# 5. ☁️ AWS Services Used

The POC intentionally uses a focused set of AWS services.

| Service                   | Purpose                                  |
| ------------------------- | ---------------------------------------- |
| Amazon VPC                | Network isolation                        |
| Subnets                   | Public/private network separation        |
| Security Groups           | Network access control                   |
| Application Load Balancer | Public API entry point                   |
| Amazon ECS Fargate        | Runs FastAPI container                   |
| Amazon ECR                | Stores Docker images                     |
| Amazon RDS PostgreSQL     | Persistent database                      |
| Amazon S3                 | Frontend and attachments                 |
| Amazon CloudFront         | Global frontend delivery and API routing |
| AWS Lambda                | Thumbnail generation                     |
| AWS Secrets Manager       | Database credentials                     |
| Parameter Store           | Application configuration                |
| IAM                       | Permissions and roles                    |
| CloudWatch                | Logs, metrics, dashboards and alarms     |
| Terraform                 | Infrastructure as Code                   |
| GitHub Actions            | CI/CD                                    |
| GitHub OIDC               | Keyless GitHub-to-AWS authentication     |

---

# 6. 📅 POC Milestones

# M0 — Manual AWS Deployment

### Objective

Understand the AWS components before automating them.

The application is deployed manually using the AWS Console.

### Expected resources

* VPC
* Public subnets
* Private subnets
* Security groups
* Application Load Balancer
* ECS cluster
* ECS task definition
* ECS service
* Container

### Verification

The ALB URL should return a valid application response.

### Learning

M0 demonstrates why manual deployment is difficult to maintain and why Infrastructure as Code is required.

---

# M1 — Containerization

## Objective

Create a production-ready Docker image for the FastAPI application.

### Requirements

* Multi-stage Docker build
* Non-root container user
* No build tools in final image
* Image tagged with Git commit SHA
* Image stored in Amazon ECR

Example image tag:

```text
<git-commit-sha>
```

instead of:

```text
latest
```

This makes every deployment traceable to a specific source-code version.

### Dockerfile

The project contains:

```text
Dockerfile
```

which builds the FastAPI application into a production container.

---

# M2 — Infrastructure as Code

## Objective

Recreate the AWS infrastructure using Terraform.

The infrastructure includes:

* VPC
* Public subnets
* Private subnets
* Availability Zones
* Internet Gateway
* NAT Gateway
* Security Groups
* Application Load Balancer
* Target Group
* ECS Cluster
* ECS Task Definition
* ECS Service

### Important requirement

The application container runs in private subnets.

The ALB is the public-facing component.

```text
Internet
   ↓
ALB — Public
   ↓
ECS — Private
```

### Terraform principle

No infrastructure should need to be manually created after the Terraform implementation is complete.

The expected workflow is:

```bash
terraform apply
```

and later:

```bash
terraform destroy
```

---

# M3 — Database and Secrets

## Objective

Add persistent storage and secure application configuration.

### Database

Amazon RDS PostgreSQL is used.

The database:

* Runs in private subnets
* Is not publicly accessible
* Uses encryption at rest
* Has automated backups
* Is reachable only from the application security group

### Secrets

Database credentials are stored in:

```text
AWS Secrets Manager
```

The application retrieves them at runtime.

Sensitive values must never be committed to Git.

### Parameter Store

Non-secret application configuration is stored in:

```text
AWS Systems Manager Parameter Store
```

The ECS task role allows the application to retrieve the required configuration.

### Persistence test

The application must satisfy:

```text
Create ticket
      ↓
Restart ECS task
      ↓
Ticket still exists
```

This proves the application is using RDS rather than temporary container storage.

---

# M4 — Frontend Deployment

## Objective

Deploy the static frontend securely.

The frontend is stored in:

```text
Amazon S3
```

and delivered through:

```text
Amazon CloudFront
```

The S3 bucket is private.

CloudFront accesses it using:

```text
Origin Access Control (OAC)
```

### Routing

CloudFront handles:

```text
/*
```

through the frontend S3 origin.

API requests:

```text
/api/*
```

are routed to the Application Load Balancer.

This gives the application a single CloudFront entry point.

---

# M5 — Serverless File Processing

## Objective

Implement direct S3 uploads and serverless thumbnail generation.

### Upload process

The API generates a presigned S3 URL.

The browser uploads directly to S3.

The API does not process the file bytes.

### Lambda

An S3 `ObjectCreated` event triggers the Lambda function.

The Lambda:

1. Receives the S3 event.
2. Downloads the image.
3. Opens the image using Pillow.
4. Resizes it to approximately 200x200.
5. Writes the thumbnail under:

```text
thumbnails/
```

### Expected result

When a screenshot is attached to a ticket:

```text
Original file
      ↓
S3
      ↓
Lambda
      ↓
Thumbnail
      ↓
S3 thumbnails/
```

---

# M6 — CI/CD Pipeline

## Objective

Remove manual deployment steps.

The deployment pipeline is implemented using:

```text
GitHub Actions
```

with:

```text
AWS OIDC
```

instead of static AWS access keys.

The current repository contains a workflow generated through Terraform:

```text
.github/workflows/deploy.yml
```

---

## Pipeline Flow

```text
git push origin main
        ↓
Secret Scan
        ↓
Unit Tests
        ↓
AWS OIDC Authentication
        ↓
Frontend Deployment
        ↓
Docker Build
        ↓
ECR Push
        ↓
ECS Task Definition Update
        ↓
ECS Deployment
        ↓
Smoke Test
```

---

## Secret Scanning

The pipeline uses TruffleHog to detect committed secrets.

A secret-scanning failure must block deployment.

---

## Unit Tests

The pipeline runs:

```bash
pytest tests/
```

The test suite uses an isolated/in-memory SQLite database for testing.

---

## Docker Image

The image is tagged using:

```text
Git commit SHA
```

This provides deployment traceability.

---

## ECS Deployment

The workflow:

1. Gets the current ECS task definition.
2. Replaces the container image with the new SHA-tagged ECR image.
3. Updates the ECS service.
4. Performs a rolling deployment.
5. Runs the smoke test.

---

# M7 — Observability

## Objective

Make failures visible without manually checking the application.

The production deployment should provide:

* CloudWatch application logs
* Finite log retention
* Request metrics
* Error metrics
* Response latency
* ECS CPU usage
* ECS memory usage
* Database connections
* CloudWatch dashboard
* CloudWatch alarms

### Required alarms

At minimum:

```text
1. High HTTP 5xx errors
2. Unhealthy ALB targets
3. High RDS CPU
```

The alarms should notify a configured notification target.

---

# M8 — Harden and Prove

The final stage verifies that the deployment is actually reproducible.

## Required activities

### 1. Deployment readiness

Verify all 34 checklist items.

### 2. Resource tagging

Resources should contain:

```text
Project
Owner
Environment
CostCenter
```

### 3. Smoke testing

Run the complete smoke test suite.

### 4. Load sanity check

Run:

```text
20 concurrent users
5 minutes
```

The objective is to verify that the application operates without errors.

### 5. Cost report

Document:

* Total estimated/actual spend
* AWS services generating cost
* Two most expensive resources/services
* Cost-control opportunities

### 6. Destroy and rebuild

The final test is:

```bash
terraform destroy
```

followed by:

```bash
terraform apply
```

The application must become operational again without relying on forgotten manual configuration.

---

# 7. 📂 Repository Structure

```text
poc-aws-deployment-ticketdesk/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── static/
│   └── index.html
│
├── tests/
│   └── test_main.py
│
├── ticketdesk-terraform/
│   ├── alb.tf
│   ├── cloudfront.tf
│   ├── ecs.tf
│   ├── github_actions.tf
│   ├── iam.tf
│   ├── lambda.tf
│   ├── lambda_src/
│   ├── networking.tf
│   ├── outputs.tf
│   ├── rds.tf
│   ├── s3.tf
│   ├── secrets.tf
│   ├── security_groups.tf
│   ├── versions.tf
│   └── terraform.tfvars
│
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

---

# 8. 🧩 Terraform Components

## `networking.tf`

Defines:

* VPC
* Public subnets
* Private subnets
* Availability Zones
* Internet Gateway
* NAT Gateway
* Route tables

---

## `security_groups.tf`

Defines network-level access controls between:

```text
Internet → ALB
ALB → ECS
ECS → RDS
```

Security groups should reference other security groups wherever possible instead of allowing unrestricted access.

---

## `alb.tf`

Creates:

* Application Load Balancer
* Target Group
* Listener
* Health check

The ALB provides the public entry point to the backend.

---

## `ecs.tf`

Creates:

* ECS Cluster
* Task Definition
* ECS Service
* Fargate configuration
* Container configuration

The ECS task runs in private subnets.

---

## `rds.tf`

Creates the PostgreSQL database.

The database is private and accessible only from the application layer.

---

## `s3.tf`

Creates:

1. Private frontend bucket
2. Private uploads bucket

The frontend bucket is accessed through CloudFront OAC.

The uploads bucket receives presigned uploads.

---

## `cloudfront.tf`

Creates the CloudFront distribution.

It provides:

* Global frontend delivery
* Private S3 access
* `/api/*` routing to the ALB

---

## `lambda.tf`

Creates:

* Lambda function
* S3 event notification
* Required IAM permissions

The Lambda generates thumbnails using Pillow.

---

## `secrets.tf`

Creates:

* Secrets Manager resources
* Parameter Store configuration

Sensitive database information is kept outside source control.

---

## `iam.tf`

Defines:

* ECS task roles
* ECS execution roles
* GitHub Actions OIDC role
* Required IAM policies

The objective is least-privilege access.

---

## `github_actions.tf`

Terraform generates the GitHub Actions deployment workflow using environment-specific infrastructure values.

This removes the requirement to manually edit deployment configuration after provisioning.

---

# 9. 🔐 Security Design

Security is a major part of the POC.

## No credentials in Git

The repository must not contain:

```text
AWS Access Key
AWS Secret Key
Database Password
Private Key
API Secret
```

Secret scanning is included in the CI/CD pipeline.

---

## GitHub OIDC

GitHub Actions authenticates to AWS using OIDC.

Therefore, static AWS credentials do not need to be stored in GitHub repository secrets.

```text
GitHub Actions
      ↓
GitHub OIDC
      ↓
AWS IAM Role
      ↓
AWS Resources
```

---

## Private ECS

The FastAPI container runs in private subnets.

The internet does not directly access the ECS task.

---

## Private RDS

RDS is configured as:

```text
Publicly Accessible = false
```

Only the application security group should be able to connect to the database.

---

## Private S3

The frontend S3 bucket is not public.

CloudFront uses OAC to access the bucket.

---

## Least Privilege IAM

IAM policies should provide only the permissions required by each component.

Avoid:

```json
{
  "Action": "*",
  "Resource": "*"
}
```

---

# 10. 🩺 Health Check

The backend provides:

```text
GET /api/health
```

The endpoint performs a database health check.

The endpoint is used by:

* ALB health checks
* Smoke tests
* Deployment verification

A healthy response confirms that the application and database are communicating correctly.

---

# 11. 🔌 API Reference

| Method | Endpoint                          | Purpose                       |
| ------ | --------------------------------- | ----------------------------- |
| GET    | `/`                               | Frontend/application entry    |
| GET    | `/api/health`                     | Application + database health |
| POST   | `/api/tickets/`                   | Create ticket                 |
| GET    | `/api/tickets/`                   | List/filter tickets           |
| PUT    | `/api/tickets/{id}/status`        | Update ticket status          |
| POST   | `/api/tickets/{id}/comments/`     | Add comment                   |
| GET    | `/api/tickets/{id}/presigned-url` | Generate S3 upload URL        |
| PUT    | `/api/tickets/{id}/attach`        | Attach uploaded file          |
| GET    | `/api/dashboard/`                 | Dashboard statistics          |

---

# 12. 🖥️ Local Development

The application can be tested locally without provisioning AWS infrastructure.

## Create virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
pip install pytest httpx
```

---

## Run tests

```bash
python -m pytest tests/
```

---

## Start application

```bash
uvicorn main:app --reload --port 8000
```

Open:

```text
http://localhost:8000
```

---

# 13. 🛠️ AWS Deployment From Scratch

## Prerequisites

Install:

```text
Git
AWS CLI v2
Terraform 1.7+
Python 3.11+
Docker Desktop
```

Verify:

```bash
git --version
aws --version
terraform --version
python --version
docker --version
```

Configure AWS CLI:

```bash
aws configure
```

The AWS identity used for initial Terraform provisioning requires sufficient permissions to create the required infrastructure.

---

# 14. 📥 Clone Repository

```bash
git clone https://github.com/Vivek-27/poc-aws-deployment-ticketdesk.git
cd poc-aws-deployment-ticketdesk
```

---

# 15. 🗄️ Terraform Remote State

Terraform state should be stored remotely rather than only on the local machine.

The backend uses:

```text
Amazon S3
```

with state locking configured according to the Terraform/AWS backend setup used by the project.

Example configuration:

```hcl
terraform {
  backend "s3" {
    bucket         = "YOUR-STATE-BUCKET-NAME"
    key            = "ticketdesk/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

Replace the placeholder values with the environment's actual state backend configuration.

---

# 16. ⚙️ Terraform Variables

Configure:

```text
ticketdesk-terraform/terraform.tfvars
```

Example:

```hcl
aws_region  = "us-east-1"
environment = "poc"

github_org  = "Vivek-27"
github_repo = "poc-aws-deployment-ticketdesk"
```

Do not place passwords, access keys or other secrets inside `terraform.tfvars`.

---

# 17. 🚀 Provision Infrastructure

Navigate to Terraform:

```bash
cd ticketdesk-terraform
```

Initialize:

```bash
terraform init
```

Review the plan:

```bash
terraform plan
```

Apply:

```bash
terraform apply
```

or:

```bash
terraform apply -auto-approve
```

Terraform provisions the AWS infrastructure required by the application.

---

# 18. 🔄 GitHub Actions Deployment

After infrastructure provisioning, the GitHub Actions workflow is configured with the environment-specific infrastructure values.

Return to the repository root:

```bash
cd ..
```

Commit changes:

```bash
git add .
git commit -m "feat: deploy ticketdesk infrastructure and workflow"
```

Push:

```bash
git push origin main
```

A push to `main` starts the deployment pipeline.

---

# 19. 🔁 CI/CD Pipeline in Detail

```text
Developer
    │
    │ git push
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Secret Scan
    │
    ├── Unit Tests
    │
    ├── AWS OIDC Authentication
    │
    ├── Deploy Frontend
    │
    ├── Docker Build
    │
    ├── Tag with Commit SHA
    │
    ├── Push Image to ECR
    │
    ├── Update ECS Task Definition
    │
    ├── Deploy ECS Service
    │
    └── Smoke Test
```

If any required validation step fails, deployment must stop.

---

# 20. 🧪 Smoke Test

The deployment pipeline performs a post-deployment health check against the deployed CloudFront application.

The basic validation is:

```text
CloudFront URL
      ↓
HTTP request
      ↓
Expected HTTP 200
```

The smoke test verifies that the deployed application is reachable after the ECS deployment.

---

# 21. 📊 Observability

Application logs should be available through:

```text
Amazon CloudWatch Logs
```

The production monitoring layer should include a CloudWatch dashboard covering:

```text
Request count
Error rate
Response latency
ECS CPU
ECS memory
Database connections
```

Required alarms:

```text
HTTP 5xx errors
Unhealthy ALB targets
High RDS CPU
```

The alarms must have an actual notification destination.

---

# 22. 💰 Cost Management

The POC requires a cost report covering:

* AWS services used
* Approximate/actual spend
* Most expensive resources
* Cost-control opportunities

Particular attention should be given to resources that can continue generating charges after testing.

Before finishing work, run:

```bash
terraform destroy
```

and verify that no unexpected billable infrastructure remains.

---

# 23. 🧹 Teardown

To remove the complete Terraform-managed stack:

```bash
cd ticketdesk-terraform
terraform destroy
```

or:

```bash
terraform destroy -auto-approve
```

The final POC test is:

```text
terraform destroy
        ↓
AWS resources removed
        ↓
terraform apply
        ↓
Infrastructure recreated
        ↓
GitHub Actions deployment
        ↓
Application available again
```

This proves that the environment is reproducible.

---

# 24. ✅ Deployment Readiness Checklist

The POC defines 34 deployment-readiness requirements.

## Container

* [ ] 1. Multi-stage Dockerfile
* [ ] 2. Container runs as a non-root user
* [ ] 3. No SDK/compiler/build tools in final image
* [ ] 4. Docker image tagged with Git commit SHA
* [ ] 5. ECR image scanning enabled

## Infrastructure as Code

* [ ] 6. All infrastructure defined in Terraform
* [ ] 7. Terraform state uses remote backend with locking
* [ ] 8. Environment-specific values are variables
* [ ] 9. `terraform destroy` followed by `terraform apply` rebuilds the stack

## Network and Compute

* [ ] 10. ECS container runs in private subnet
* [ ] 11. Only the load balancer is publicly exposed
* [ ] 12. Security groups use restricted references instead of unrestricted access
* [ ] 13. Health check endpoint configured
* [ ] 14. At least two Availability Zones used
* [ ] 15. Application reachable through ALB/CloudFront URL

## Database and Configuration

* [ ] 16. RDS is private
* [ ] 17. Database password stored in Secrets Manager
* [ ] 18. Application configuration stored in Parameter Store
* [ ] 19. No credentials committed to repository
* [ ] 20. Encryption at rest enabled
* [ ] 21. Automated database backups enabled

## Frontend and Serverless

* [ ] 22. Frontend served through CloudFront
* [ ] 23. Frontend S3 bucket is private
* [ ] 24. Attachments uploaded using presigned S3 URLs
* [ ] 25. Lambda triggered by S3 upload
* [ ] 26. Thumbnail generation works end to end

## Pipeline

* [ ] 27. Push to `main` automatically deploys
* [ ] 28. Failing tests block deployment
* [ ] 29. Secret scanning failure blocks deployment
* [ ] 30. Smoke test runs after deployment

## Operations

* [ ] 31. Logs available in CloudWatch with finite retention
* [ ] 32. Dashboard shows requests/errors/latency/CPU/memory/database metrics
* [ ] 33. Three alarms notify a configured notification target

## Housekeeping

* [ ] 34. Resources are tagged and cost/reporting requirements are documented
* [ ] IAM follows least privilege
* [ ] Cost remains within the assigned budget
* [ ] README allows a new joiner to reproduce the deployment

> **Note:** The official POC checklist contains 34 numbered requirements; the exact verification status should be confirmed during the final demo rather than assuming implementation from Terraform code alone.

---

# 25. 🚨 Five Pass/Fail Security Requirements

These requirements are critical.

## 1. No credentials in repository

No AWS keys, database passwords or other secrets may be committed.

---

## 2. No unrestricted IAM policy

Avoid:

```json
{
  "Action": "*",
  "Resource": "*"
}
```

IAM must follow least privilege.

---

## 3. Database must not be internet accessible

RDS must have:

```text
Publicly Accessible = false
```

---

## 4. Stack must rebuild from zero

The documented deployment process must work from a clean environment.

---

## 5. Terraform destroy must remove billable infrastructure

After:

```bash
terraform destroy
```

the environment should not leave unexpected billable resources behind.

---

# 26. 🧪 Functional Verification

The final application should be tested end to end.

## Ticket creation

```text
Create ticket
      ↓
Ticket stored in RDS
      ↓
Ticket appears in application
```

## Ticket status

Verify:

```text
OPEN
 ↓
IN_PROGRESS
 ↓
RESOLVED
 ↓
CLOSED
```

## Comments

Create a ticket comment and verify persistence.

## Filtering

Verify filtering by:

```text
Status
Priority
Category
```

## Dashboard

Verify dashboard counts by:

```text
Status
Priority
```

## Attachment

Verify:

```text
Create ticket
      ↓
Generate presigned URL
      ↓
Upload directly to S3
      ↓
S3 event
      ↓
Lambda
      ↓
Thumbnail
```

## Persistence

Restart/redeploy ECS and confirm that existing tickets remain available.

---

# 27. 🐳 Docker Verification

Build locally:

```bash
docker build -t ticketdesk:test .
```

Run:

```bash
docker run -p 8000:8000 ticketdesk:test
```

Verify:

```text
http://localhost:8000
```

Check that the container runs as the configured non-root user.

---

# 28. 🐛 Troubleshooting

## S3 Presigned Upload Returns 403

Possible causes:

* Content-Type mismatch
* S3 CORS configuration
* Corporate proxy/Zscaler modifying request headers
* Invalid/expired presigned URL

Verify that the frontend uses the expected content type and that the S3 bucket CORS configuration permits the required upload method.

---

## Lambda `Runtime.ImportModuleError`

If Pillow reports an error involving:

```text
_imaging
```

the dependency may have been built for the wrong operating system.

For Python 3.11 Lambda compatibility, install the Linux-compatible wheel:

```bash
pip install \
  --platform manylinux2014_x86_64 \
  --target lambda_src \
  --implementation cp \
  --python-version 3.11 \
  --only-binary=:all: \
  --upgrade Pillow
```

---

## GitHub Actions OIDC Failure

If GitHub Actions is stuck while assuming the AWS role, verify:

```text
github_org
github_repo
```

in:

```text
terraform.tfvars
```

The values must exactly match the GitHub repository referenced by the IAM trust policy.

---

## ECS Task Fails

The first debugging step should be checking:

```text
ECS Task Logs
ECS Stopped Task Reason
CloudWatch Logs
```

Do not immediately change Terraform configuration.

First determine what the application or ECS platform is reporting.

---

# 29. 📚 What This POC Demonstrates

After completing the POC, the developer should be able to explain and demonstrate:

### Containerization

How to package a FastAPI application into a production Docker image.

### AWS Networking

How public and private subnets separate internet-facing and internal components.

### ECS Fargate

How containerized applications run without managing EC2 servers.

### Load Balancing

How an ALB distributes requests to ECS tasks.

### RDS

How persistent application data is stored outside the container.

### Secrets Manager

How sensitive credentials are retrieved at runtime.

### Parameter Store

How application configuration can be separated from application code.

### S3

How static assets and user uploads can be stored independently.

### CloudFront

How a global CDN can securely deliver the frontend and route API requests.

### Lambda

How an event-driven serverless function can process uploaded files.

### IAM

How AWS permissions are controlled using roles and least privilege.

### Terraform

How AWS infrastructure can be represented as code and recreated consistently.

### GitHub Actions

How application changes can automatically reach AWS after a Git push.

### OIDC

How GitHub Actions can authenticate to AWS without storing long-lived AWS access keys.

### CloudWatch

How application and infrastructure health can be monitored.

---

# 30. 🏁 Definition of Done

The TicketDesk POC is considered complete when:

```text
                    ┌──────────────────────┐
                    │   Git Push to main   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   GitHub Actions     │
                    └──────────┬───────────┘
                               ↓
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
          Unit Tests                  Secret Scan
                 │                           │
                 └─────────────┬─────────────┘
                               ↓
                         Docker Build
                               ↓
                              ECR
                               ↓
                        ECS Fargate
                               ↓
                              ALB
                               ↓
                          CloudFront
                               ↓
                           Browser
```

At the same time:

```text
ECS
 │
 ├── RDS PostgreSQL
 │
 ├── Secrets Manager
 │
 └── Parameter Store

Browser
 │
 └── Presigned S3 Upload
          ↓
       S3 Event
          ↓
       Lambda
          ↓
      Thumbnail
```

The final deployment must be:

* Automated
* Repeatable
* Secure
* Containerized
* Infrastructure-as-Code driven
* Observable
* Cost-conscious
* Rebuildable from zero

---

# 31. 🚀 Stretch Goals

Only attempt these after all mandatory requirements pass.

| Stretch Goal                                  | Points |
| --------------------------------------------- | -----: |
| HTTPS with ACM certificate and real domain    |     +2 |
| ECS Auto Scaling demonstrated under load      |     +2 |
| Cognito authentication                        |     +2 |
| Blue/green deployment with rollback           |     +3 |
| Scheduled shutdown/startup for cost reduction |     +1 |
| DynamoDB alternative implementation           |     +2 |

Stretch goals should not be prioritized over the mandatory deployment-readiness requirements.

---

# 32. 📝 Final Project Summary

TicketDesk demonstrates a complete cloud deployment lifecycle for a real application.

The application starts as a FastAPI service and is transformed into a cloud-native AWS deployment:

```text
FastAPI
   ↓
Docker
   ↓
ECR
   ↓
ECS Fargate
   ↓
ALB
   ↓
CloudFront
   ↓
Users
```

Persistent data is handled by:

```text
ECS
 ↓
RDS PostgreSQL
```

Secrets are handled by:

```text
Secrets Manager
```

Configuration is handled by:

```text
Parameter Store
```

File processing is handled by:

```text
S3
 ↓
Lambda
 ↓
Thumbnail
```

Infrastructure is managed using:

```text
Terraform
```

Application deployment is automated using:

```text
GitHub Actions
 ↓
OIDC
 ↓
AWS
```

The final objective is not simply to make TicketDesk work once.

The objective is to be able to say:

> **"I can deploy, operate, monitor, destroy, and rebuild a real application on AWS using Infrastructure as Code and CI/CD."**
