# Data Ingestion and Aggregation Service

A lightweight, backend service for **event ingestion and aggregation**, designed to handle:

* Idempotent event processing
* High-throughput bulk ingestion
* Concurrency-safe operations
* Efficient aggregation and querying

Built with a focus on **correctness, performance, and scalability**.

## 🚀 Tech Stack

* **Python 3.13**
* **FastAPI (async)**
* **PostgreSQL**
* **SQLAlchemy (async)**
* **Pytest + HTTPX**

### Key Components

* **API Layer** – request handling & validation
* **Service Layer** – business logic
* **DB Layer** – persistence & constraints
* **Background Worker** – incremental aggregation

## 📡 API Endpoints

* POST `/events` - ingest one event
* POST `/events/bulk` - ingest many events
* GET `/events` - query raw events
* GET `/metrics` - aggregated data
* GET `/health` - liveness
* GET `/ready` - DB readiness

## 🛡️ Validation & Security

* Bulk size limit (≤ 5000)
* UTC timestamp enforcement
* Input validation via Pydantic

## 🧪 Testing

Using **Pytest**:

* Idempotent ingestion
* Bulk ingestion
* Aggregation correctness
* Concurrency safety
* Time edge cases

## 🧠 Environment Variables

```text
APP_ENV=development
APP_DEBUG=True

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=data_ingestion_service
```

## ▶️ Running

```bash
uv sync
uv run uvicorn app.main:app --reload
uv run pytest
```

## 📈 Future Improvements

* Cursor-based pagination
* Distributed workers (Kafka/Celery)
* Redis rate limiting
* Observability (metrics + tracing)

## 🧠 Summary

This system demonstrates:

* Correct handling of **concurrency & idempotency**
* Efficient **database-driven aggregation**
* Scalable and clean **backend architecture**
