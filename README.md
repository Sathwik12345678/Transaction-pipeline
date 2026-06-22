# AI-Powered Transaction Processing Pipeline

## Project Overview

This project is an AI-powered backend system that processes raw financial transaction CSV files asynchronously. The system cleans transaction data, detects anomalies, stores processed transactions in a PostgreSQL database, generates AI-powered spending summaries using Groq LLM, and exposes results through REST APIs.

The application is built using FastAPI, PostgreSQL, Redis, Celery, Pandas, and Groq LLM.

---

## Features

### CSV Upload & Processing

* Upload transaction CSV files
* Create asynchronous processing jobs
* Track processing status

### Data Cleaning

* Normalize transaction dates
* Remove duplicate records
* Clean currency values
* Convert amounts to numeric values
* Standardize status and currency fields
* Handle missing categories

### Anomaly Detection

The system flags suspicious transactions using:

#### Rule 1

Transactions whose amount exceeds 3× the account's median transaction value.

#### Rule 2

USD transactions made with domestic merchants:

* Swiggy
* Ola
* IRCTC

### Transaction Storage

* Stores cleaned transactions in PostgreSQL
* Maintains job-to-transaction relationships

### AI-Powered Summary Generation

Using Groq Llama 3.1:

* Spending analysis
* Transaction insights
* Risk assessment
* Financial narrative generation

### Job Summary Reporting

Stores:

* Total INR spend
* Total USD spend
* Top merchants
* Anomaly count
* AI-generated narrative
* Risk level

---

# Architecture

```text
                +------------------+
                |    CSV Upload    |
                +--------+---------+
                         |
                         v
                +------------------+
                |     FastAPI      |
                +--------+---------+
                         |
                         v
                +------------------+
                |      Celery      |
                +--------+---------+
                         |
         +---------------+---------------+
         |                               |
         v                               v
+------------------+         +------------------+
| Data Cleaning    |         | Anomaly Engine   |
+------------------+         +------------------+
         |                               |
         +---------------+---------------+
                         |
                         v
                +------------------+
                | PostgreSQL       |
                +--------+---------+
                         |
                         v
                +------------------+
                | Groq LLM         |
                | Summary Engine   |
                +--------+---------+
                         |
                         v
                +------------------+
                | Results API      |
                +------------------+
```

---

# Tech Stack

## Backend

* FastAPI
* Python

## Database

* PostgreSQL

## Task Queue

* Celery
* Redis

## Data Processing

* Pandas

## AI Integration

* Groq API
* Llama 3.1 8B Instant

## Containerization

* Docker
* Docker Compose

---

# Project Structure

```text
transaction-pipeline/
│
├── app/
│   ├── models.py
│   ├── database.py
│   ├── main.py
│   │
│   ├── routers/
│   │   └── jobs.py
│   │
│   ├── worker/
│   │   ├── celery_app.py
│   │   └── tasks.py
│   │
│   └── services/
│       └── llm_service.py
│
├── uploads/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .env
```

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd transaction-pipeline
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

## Start PostgreSQL

Ensure PostgreSQL is running.

Create database:

```sql
CREATE DATABASE transactions;
```

---

## Start Redis

```bash
docker run -p 6379:6379 redis
```

---

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Start Celery Worker

```bash
celery -A app.worker.tasks worker --pool=solo --loglevel=info
```

---

# API Endpoints

## Upload CSV

```http
POST /jobs/upload
```

Uploads transaction CSV and creates processing job.

---

## Get All Jobs

```http
GET /jobs
```

Returns all jobs.

---

## Get Job Status

```http
GET /jobs/{job_id}/status
```

Returns processing status.

---

## Get Job Results

```http
GET /jobs/{job_id}/results
```

Returns:

* Transaction count
* Anomaly count
* Total spend
* AI-generated summary
* Risk level
* Anomaly details

---

# Sample Output

```json
{
  "job_id": 15,
  "status": "Completed",
  "total_transactions": 85,
  "anomaly_count": 5,
  "total_spend_inr": 45000,
  "total_spend_usd": 100,
  "risk_level": "Generated by Groq",
  "summary": "AI generated spending analysis...",
  "anomalies": [
    {
      "txn_id": "TXN001",
      "merchant": "Swiggy",
      "amount": 15000,
      "reason": "Amount exceeds 3x account median"
    }
  ]
}
```

---

# Future Improvements

* Advanced anomaly detection models
* Fraud scoring system
* Multi-file batch processing
* User authentication
* Dashboard and analytics
* Real-time notifications

---

# Author

Ponnam Sathwik Goud
