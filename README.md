# 📐 AWS Architecture Diagrams

The following diagrams show how the AWS services used by TicketDesk communicate with each other.

---

## 1. 🏗️ Complete AWS Architecture

```html
<svg width="100%" viewBox="0 0 1200 780" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>

    <style>
      .service {
        fill: #ffffff;
        stroke: #333333;
        stroke-width: 2;
        rx: 12;
      }

      .aws {
        fill: #fff7ed;
        stroke: #f97316;
        stroke-width: 2;
        rx: 12;
      }

      .security {
        fill: #f5f3ff;
        stroke: #7c3aed;
        stroke-width: 2;
        rx: 12;
      }

      .storage {
        fill: #eff6ff;
        stroke: #2563eb;
        stroke-width: 2;
        rx: 12;
      }

      .compute {
        fill: #ecfdf5;
        stroke: #059669;
        stroke-width: 2;
        rx: 12;
      }

      .text {
        font-family: Arial, sans-serif;
        fill: #111827;
        font-size: 16px;
      }

      .small {
        font-family: Arial, sans-serif;
        fill: #4b5563;
        font-size: 13px;
      }

      .title {
        font-family: Arial, sans-serif;
        font-weight: bold;
        fill: #111827;
        font-size: 20px;
      }

      .arrow {
        stroke: #374151;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrow);
      }

      .dashed {
        stroke-dasharray: 7 5;
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="600" y="35" text-anchor="middle" class="title">
    TicketDesk — AWS Cloud Architecture
  </text>

  <!-- Client -->
  <rect x="40" y="100" width="160" height="75" class="service"/>
  <text x="120" y="130" text-anchor="middle" class="text">🌐 Browser</text>
  <text x="120" y="153" text-anchor="middle" class="small">End User</text>

  <!-- CloudFront -->
  <rect x="270" y="100" width="190" height="75" class="aws"/>
  <text x="365" y="130" text-anchor="middle" class="text">☁️ CloudFront</text>
  <text x="365" y="153" text-anchor="middle" class="small">CDN / Routing</text>

  <!-- Frontend S3 -->
  <rect x="520" y="70" width="210" height="80" class="storage"/>
  <text x="625" y="103" text-anchor="middle" class="text">🪣 S3</text>
  <text x="625" y="125" text-anchor="middle" class="small">Private Frontend</text>
  <text x="625" y="142" text-anchor="middle" class="small">OAC Protected</text>

  <!-- ALB -->
  <rect x="520" y="190" width="210" height="80" class="aws"/>
  <text x="625" y="223" text-anchor="middle" class="text">⚖️ Application</text>
  <text x="625" y="244" text-anchor="middle" class="text">Load Balancer</text>
  <text x="625" y="261" text-anchor="middle" class="small">Public Subnets</text>

  <!-- ECS -->
  <rect x="800" y="190" width="210" height="80" class="compute"/>
  <text x="905" y="223" text-anchor="middle" class="text">🐳 ECS Fargate</text>
  <text x="905" y="245" text-anchor="middle" class="small">FastAPI Container</text>
  <text x="905" y="261" text-anchor="middle" class="small">Private Subnets</text>

  <!-- RDS -->
  <rect x="800" y="340" width="210" height="80" class="storage"/>
  <text x="905" y="373" text-anchor="middle" class="text">🗄️ RDS PostgreSQL</text>
  <text x="905" y="395" text-anchor="middle" class="small">Private Database</text>

  <!-- Secrets -->
  <rect x="520" y="340" width="210" height="80" class="security"/>
  <text x="625" y="373" text-anchor="middle" class="text">🔐 Secrets Manager</text>
  <text x="625" y="395" text-anchor="middle" class="small">DB Credentials</text>

  <!-- Parameter Store -->
  <rect x="520" y="470" width="210" height="80" class="security"/>
  <text x="625" y="503" text-anchor="middle" class="text">⚙️ Parameter Store</text>
  <text x="625" y="525" text-anchor="middle" class="small">Application Config</text>

  <!-- Upload S3 -->
  <rect x="800" y="470" width="210" height="80" class="storage"/>
  <text x="905" y="503" text-anchor="middle" class="text">🪣 S3 Uploads</text>
  <text x="905" y="525" text-anchor="middle" class="small">Attachments</text>

  <!-- Lambda -->
  <rect x="800" y="610" width="210" height="80" class="compute"/>
  <text x="905" y="643" text-anchor="middle" class="text">λ Lambda</text>
  <text x="905" y="665" text-anchor="middle" class="small">Thumbnail Generator</text>

  <!-- Arrows -->

  <!-- Browser -> CloudFront -->
  <path d="M200 137 L270 137" class="arrow"/>
  <text x="235" y="125" text-anchor="middle" class="small">HTTPS</text>

  <!-- CloudFront -> Frontend S3 -->
  <path d="M460 115 L520 110" class="arrow"/>
  <text x="490" y="98" text-anchor="middle" class="small">Static *</text>

  <!-- CloudFront -> ALB -->
  <path d="M460 160 L520 215" class="arrow"/>
  <text x="490" y="195" text-anchor="middle" class="small">/api/*</text>

  <!-- ALB -> ECS -->
  <path d="M730 230 L800 230" class="arrow"/>
  <text x="765" y="217" text-anchor="middle" class="small">HTTP</text>

  <!-- ECS -> RDS -->
  <path d="M905 270 L905 340" class="arrow"/>
  <text x="925" y="310" class="small">SQL</text>

  <!-- ECS -> Secrets -->
  <path d="M800 270 L730 350" class="arrow"/>
  <text x="750" y="310" text-anchor="middle" class="small">Read secret</text>

  <!-- ECS -> Parameter Store -->
  <path d="M850 270 L700 470" class="arrow"/>
  <text x="770" y="390" text-anchor="middle" class="small">Read config</text>

  <!-- ECS -> Upload S3 -->
  <path d="M950 270 L950 470" class="arrow dashed"/>
  <text x="970" y="375" class="small">Presigned URL</text>

  <!-- S3 -> Lambda -->
  <path d="M905 550 L905 610" class="arrow"/>
  <text x="940" y="585" class="small">ObjectCreated</text>

  <!-- Lambda -> S3 -->
  <path d="M800 650 L700 650 L700 510 L800 510" class="arrow dashed"/>
  <text x="750" y="630" text-anchor="middle" class="small">Write thumbnail</text>

  <!-- VPC boundary -->
  <rect x="480" y="175" width="580" height="255"
        fill="none"
        stroke="#9ca3af"
        stroke-width="2"
        stroke-dasharray="10 7"
        rx="15"/>

  <text x="500" y="200" class="small">
    AWS VPC — Public + Private Subnets
  </text>

</svg>
```

---

# 2. 🔀 CloudFront Routing

The application uses CloudFront as the single public entry point.

```html
<svg width="100%" viewBox="0 0 1100 500" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>

    <style>
      .box {
        fill: white;
        stroke: #333;
        stroke-width: 2;
        rx: 12;
      }

      .cdn {
        fill: #fff7ed;
        stroke: #f97316;
        stroke-width: 2;
        rx: 12;
      }

      .backend {
        fill: #ecfdf5;
        stroke: #059669;
        stroke-width: 2;
        rx: 12;
      }

      .storage {
        fill: #eff6ff;
        stroke: #2563eb;
        stroke-width: 2;
        rx: 12;
      }

      text {
        font-family: Arial, sans-serif;
        fill: #111827;
      }

      .title {
        font-size: 22px;
        font-weight: bold;
      }

      .label {
        font-size: 16px;
        font-weight: bold;
      }

      .small {
        font-size: 13px;
        fill: #4b5563;
      }

      .arrow {
        stroke: #374151;
        stroke-width: 2.5;
        fill: none;
        marker-end: url(#arrow2);
      }
    </style>
  </defs>

  <text x="550" y="35" text-anchor="middle" class="title">
    TicketDesk — CloudFront Routing
  </text>

  <!-- Browser -->
  <rect x="50" y="200" width="180" height="80" class="box"/>
  <text x="140" y="235" text-anchor="middle" class="label">
    Browser
  </text>
  <text x="140" y="258" text-anchor="middle" class="small">
    CloudFront URL
  </text>

  <!-- CloudFront -->
  <rect x="330" y="170" width="220" height="140" class="cdn"/>
  <text x="440" y="215" text-anchor="middle" class="label">
    CloudFront
  </text>
  <text x="440" y="240" text-anchor="middle" class="small">
    Single Public Entry Point
  </text>
  <text x="440" y="265" text-anchor="middle" class="small">
    Path Based Routing
  </text>

  <!-- S3 -->
  <rect x="700" y="80" width="230" height="90" class="storage"/>
  <text x="815" y="118" text-anchor="middle" class="label">
    S3 Frontend
  </text>
  <text x="815" y="142" text-anchor="middle" class="small">
    Private + OAC
  </text>

  <!-- ALB -->
  <rect x="700" y="300" width="230" height="90" class="backend"/>
  <text x="815" y="338" text-anchor="middle" class="label">
    Application Load Balancer
  </text>
  <text x="815" y="362" text-anchor="middle" class="small">
    Public Subnets
  </text>

  <!-- arrows -->
  <path d="M230 240 L330 240" class="arrow"/>
  <text x="280" y="225" text-anchor="middle" class="small">
    HTTPS
  </text>

  <path d="M550 205 L700 130" class="arrow"/>
  <text x="625" y="150" text-anchor="middle" class="small">
    /* Static
  </text>

  <path d="M550 275 L700 340" class="arrow"/>
  <text x="625" y="300" text-anchor="middle" class="small">
    /api/*
  </text>

</svg>
```

### Routing Rules

| Request  | CloudFront Origin          |
| -------- | -------------------------- |
| `/*`     | Private S3 Frontend Bucket |
| `/api/*` | Application Load Balancer  |

This allows users to access the complete application through one CloudFront URL.

---

# 3. 🚀 CI/CD Architecture

Terraform provisions the AWS infrastructure and GitHub Actions performs application deployment.

```html
<svg width="100%" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>

    <style>
      .dev {
        fill: #f3f4f6;
        stroke: #374151;
        stroke-width: 2;
        rx: 12;
      }

      .github {
        fill: #f5f3ff;
        stroke: #7c3aed;
        stroke-width: 2;
        rx: 12;
      }

      .aws {
        fill: #fff7ed;
        stroke: #f97316;
        stroke-width: 2;
        rx: 12;
      }

      .compute {
        fill: #ecfdf5;
        stroke: #059669;
        stroke-width: 2;
        rx: 12;
      }

      .storage {
        fill: #eff6ff;
        stroke: #2563eb;
        stroke-width: 2;
        rx: 12;
      }

      text {
        font-family: Arial, sans-serif;
        fill: #111827;
      }

      .title {
        font-size: 22px;
        font-weight: bold;
      }

      .label {
        font-size: 15px;
        font-weight: bold;
      }

      .small {
        font-size: 12px;
        fill: #4b5563;
      }

      .arrow {
        stroke: #374151;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrow3);
      }
    </style>
  </defs>

  <text x="600" y="35" text-anchor="middle" class="title">
    TicketDesk — CI/CD Deployment Pipeline
  </text>

  <!-- Developer -->
  <rect x="40" y="230" width="150" height="80" class="dev"/>
  <text x="115" y="265" text-anchor="middle" class="label">
    Developer
  </text>
  <text x="115" y="287" text-anchor="middle" class="small">
    git push main
  </text>

  <!-- GitHub -->
  <rect x="250" y="210" width="180" height="120" class="github"/>
  <text x="340" y="250" text-anchor="middle" class="label">
    GitHub
  </text>
  <text x="340" y="275" text-anchor="middle" class="small">
    Repository
  </text>
  <text x="340" y="295" text-anchor="middle" class="small">
    GitHub Actions
  </text>

  <!-- Secret scan -->
  <rect x="490" y="80" width="180" height="70" class="github"/>
  <text x="580" y="110" text-anchor="middle" class="label">
    Secret Scan
  </text>
  <text x="580" y="132" text-anchor="middle" class="small">
    TruffleHog
  </text>

  <!-- Tests -->
  <rect x="490" y="180" width="180" height="70" class="github"/>
  <text x="580" y="210" text-anchor="middle" class="label">
    Unit Tests
  </text>
  <text x="580" y="232" text-anchor="middle" class="small">
    pytest
  </text>

  <!-- OIDC -->
  <rect x="490" y="280" width="180" height="70" class="aws"/>
  <text x="580" y="310" text-anchor="middle" class="label">
    AWS OIDC
  </text>
  <text x="580" y="332" text-anchor="middle" class="small">
    IAM Role
  </text>

  <!-- ECR -->
  <rect x="740" y="80" width="180" height="70" class="storage"/>
  <text x="830" y="110" text-anchor="middle" class="label">
    Amazon ECR
  </text>
  <text x="830" y="132" text-anchor="middle" class="small">
    Docker Image
  </text>

  <!-- S3 -->
  <rect x="740" y="180" width="180" height="70" class="storage"/>
  <text x="830" y="210" text-anchor="middle" class="label">
    Amazon S3
  </text>
  <text x="830" y="232" text-anchor="middle" class="small">
    Frontend
  </text>

  <!-- ECS -->
  <rect x="740" y="280" width="180" height="70" class="compute"/>
  <text x="830" y="310" text-anchor="middle" class="label">
    ECS Fargate
  </text>
  <text x="830" y="332" text-anchor="middle" class="small">
    Rolling Deployment
  </text>

  <!-- Smoke -->
  <rect x="980" y="180" width="170" height="100" class="dev"/>
  <text x="1065" y="215" text-anchor="middle" class="label">
    Smoke Test
  </text>
  <text x="1065" y="240" text-anchor="middle" class="small">
    CloudFront
  </text>
  <text x="1065" y="258" text-anchor="middle" class="small">
    HTTP 200
  </text>

  <!-- arrows -->
  <path d="M190 270 L250 270" class="arrow"/>

  <path d="M430 240 L490 115" class="arrow"/>
  <path d="M430 260 L490 215" class="arrow"/>
  <path d="M430 290 L490 315" class="arrow"/>

  <path d="M670 115 L740 115" class="arrow"/>
  <path d="M670 215 L740 215" class="arrow"/>
  <path d="M670 315 L740 315" class="arrow"/>

  <path d="M920 315 L980 235" class="arrow"/>

</svg>
```

---

# 4. 📎 File Attachment Architecture

TicketDesk uses an event-driven architecture for attachments.

```html
<svg width="100%" viewBox="0 0 1100 500" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>

    <style>
      .box {
        fill: white;
        stroke: #333;
        stroke-width: 2;
        rx: 12;
      }

      .api {
        fill: #ecfdf5;
        stroke: #059669;
        stroke-width: 2;
        rx: 12;
      }

      .s3 {
        fill: #eff6ff;
        stroke: #2563eb;
        stroke-width: 2;
        rx: 12;
      }

      .lambda {
        fill: #fff7ed;
        stroke: #f97316;
        stroke-width: 2;
        rx: 12;
      }

      text {
        font-family: Arial, sans-serif;
        fill: #111827;
      }

      .title {
        font-size: 22px;
        font-weight: bold;
      }

      .label {
        font-size: 15px;
        font-weight: bold;
      }

      .small {
        font-size: 12px;
        fill: #4b5563;
      }

      .arrow {
        stroke: #374151;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrow4);
      }
    </style>
  </defs>

  <text x="550" y="35" text-anchor="middle" class="title">
    TicketDesk — Serverless Attachment Processing
  </text>

  <!-- Browser -->
  <rect x="40" y="200" width="170" height="80" class="box"/>
  <text x="125" y="235" text-anchor="middle" class="label">
    Browser
  </text>
  <text x="125" y="257" text-anchor="middle" class="small">
    Upload File
  </text>

  <!-- API -->
  <rect x="280" y="170" width="200" height="140" class="api"/>
  <text x="380" y="215" text-anchor="middle" class="label">
    FastAPI
  </text>
  <text x="380" y="240" text-anchor="middle" class="small">
    Generate Presigned URL
  </text>
  <text x="380" y="262" text-anchor="middle" class="small">
    Store Attachment Metadata
  </text>

  <!-- S3 -->
  <rect x="560" y="100" width="210" height="100" class="s3"/>
  <text x="665" y="140" text-anchor="middle" class="label">
    S3 Upload Bucket
  </text>
  <text x="665" y="165" text-anchor="middle" class="small">
    Original File
  </text>

  <!-- Lambda -->
  <rect x="830" y="100" width="210" height="100" class="lambda"/>
  <text x="935" y="140" text-anchor="middle" class="label">
    AWS Lambda
  </text>
  <text x="935" y="165" text-anchor="middle" class="small">
    Pillow Thumbnail Generator
  </text>

  <!-- Thumbnail -->
  <rect x="830" y="300" width="210" height="90" class="s3"/>
  <text x="935" y="337" text-anchor="middle" class="label">
    S3 thumbnails/
  </text>
  <text x="935" y="360" text-anchor="middle" class="small">
    Generated Thumbnail
  </text>

  <!-- arrows -->
  <path d="M210 235 L280 235" class="arrow"/>
  <text x="245" y="220" text-anchor="middle" class="small">
    Request URL
  </text>

  <path d="M480 210 L560 155" class="arrow"/>
  <text x="520" y="170" text-anchor="middle" class="small">
    Presigned URL
  </text>

  <path d="M480 250 L560 155" class="arrow"/>
  <text x="520" y="255" text-anchor="middle" class="small">
    Direct PUT
  </text>

  <path d="M770 150 L830 150" class="arrow"/>
  <text x="800" y="135" text-anchor="middle" class="small">
    ObjectCreated
  </text>

  <path d="M935 200 L935 300" class="arrow"/>
  <text x="970" y="255" class="small">
    Resize
  </text>

</svg>
```

---

# 5. 🗺️ Terraform Infrastructure Relationship

Terraform is responsible for creating the infrastructure represented by the architecture.

```text
Terraform
    │
    ├── VPC
    │    ├── Public Subnets
    │    │     └── Application Load Balancer
    │    │
    │    └── Private Subnets
    │          ├── ECS Fargate
    │          └── RDS PostgreSQL
    │
    ├── Security Groups
    │
    ├── IAM
    │    └── GitHub OIDC Role
    │
    ├── ECR
    │
    ├── S3
    │    ├── Frontend Bucket
    │    └── Upload Bucket
    │
    ├── CloudFront
    │
    ├── Lambda
    │
    ├── Secrets Manager
    │
    └── Parameter Store
```

---

# 6. 🔐 Network Security Relationship

The network access model is intentionally restrictive.

```text
                        INTERNET
                            │
                            ▼
                 ┌────────────────────┐
                 │        ALB         │
                 │   Public Subnets   │
                 └─────────┬──────────┘
                           │
                    ALB Security Group
                           │
                           ▼
                 ┌────────────────────┐
                 │   ECS Fargate      │
                 │  Private Subnets   │
                 └───────┬─────┬──────┘
                         │     │
              ECS SG ────┘     └──── ECS IAM Role
                         │
                         ▼
                 ┌────────────────────┐
                 │   RDS PostgreSQL   │
                 │  Private Subnets   │
                 └────────────────────┘

RDS is NOT directly accessible from the Internet.
```

---

# 7. 📊 Service Responsibility Map

| Layer              | AWS Service     | Responsibility              |
| ------------------ | --------------- | --------------------------- |
| Edge               | CloudFront      | Public entry point/CDN      |
| Frontend           | S3              | Static application files    |
| Networking         | VPC             | Network isolation           |
| Networking         | ALB             | API traffic routing         |
| Compute            | ECS Fargate     | FastAPI application         |
| Container Registry | ECR             | Docker images               |
| Database           | RDS PostgreSQL  | Persistent data             |
| Storage            | S3              | Attachments                 |
| Serverless         | Lambda          | Thumbnail generation        |
| Secrets            | Secrets Manager | Database credentials        |
| Configuration      | Parameter Store | Runtime configuration       |
| Identity           | IAM             | Permissions                 |
| Monitoring         | CloudWatch      | Logs/metrics/alarms         |
| IaC                | Terraform       | Infrastructure provisioning |
| CI/CD              | GitHub Actions  | Automated deployment        |
| CI/CD Security     | GitHub OIDC     | Keyless AWS authentication  |

---

# 8. 🔗 End-to-End Architecture Summary

```text
                         USER
                           │
                           ▼
                     CLOUDFRONT
                      /        \
                     /          \
                  /*              /api/*
                   │                 │
                   ▼                 ▼
              PRIVATE S3           ALB
              FRONTEND              │
                                    ▼
                              ECS FARGATE
                              FASTAPI APP
                               /    |    \
                              /     |     \
                             ▼      ▼      ▼
                           RDS   SECRETS  PARAMETER
                                  MANAGER   STORE
                           
                           File Upload
                                │
                                ▼
                         PRESIGNED S3 URL
                                │
                                ▼
                           S3 UPLOADS
                                │
                         ObjectCreated
                                │
                                ▼
                            LAMBDA
                                │
                                ▼
                         THUMBNAILS/S3
```

This represents the complete TicketDesk AWS deployment from the user's browser through the frontend, API, database, secrets, file storage and serverless processing.

---
