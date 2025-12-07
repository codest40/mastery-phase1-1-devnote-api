# DevNotes Project

---

## Name  
DevNotes API – (Async FastAPI + PostgreSQL + Docker + DevOps CI/CD Pipeline)

---

## Purpose  
Build a production-ready, fully asynchronous note-taking API service with a cloud-aligned DevOps automation ecosystem.  
The project blends backend engineering, infrastructure orchestration, CI/CD automation, observability, and deployment strategies to simulate real-world API development and operations.

---

## Objective  
To establish an enterprise-grade backend foundation combined with a robust DevOps ecosystem.  
This includes:

- Modern async backend development  
- Dockerized infrastructure for reproducible environments  
- CI/CD automation via GitHub Actions  
- Multi-environment configuration switching  
- Logging, monitoring, and error visibility  
- Deployment readiness for Render, AWS, or similar platforms  

---

## Key Deliverables

### Backend Core  
- Asynchronous FastAPI CRUD API  
- SQLAlchemy 2.0 async ORM with asyncpg  
- PostgreSQL 15 as the primary backing database  
- Clean modularization:  
  - `models.py`  
  - `crud.py`  
  - `schemas.py`  
  - `notes.py`  
  - `db.py`  
  - `config.py`  
  - `main.py`  

### Environment System  
- Central Pydantic Settings configuration with auto-environment detection:  
  - local  
  - github_ci  
  - render  
  - aws  
- Automatic DB URL selection per environment  
- Safe `.env` loading with overrides and fallbacks  

### Containerization  
- Single Dockerfile optimized for dev + prod  
- Python 3.11 slim  
- Minimal system dependencies  
- Supports uvicorn/gunicorn  
- `docker-compose.yaml` orchestrating:  
  - FastAPI  
  - PostgreSQL  
  - pgAdmin  
  - Volumes, networks, and healthchecks  

### Logging & Observability  
- Multi-stream logging with rotation:  
  - audit, error, security, system, event, admin, access  
- Central logging hub ready for ELK/CloudWatch/Loki  

### Real-Time Error Tracking  
- Middleware capturing request failures, exceptions, timestamps, and error counters  
- `/stats` endpoint exposing metrics  
- `/trigger-error` endpoint for CI/CD testing  

### Admin Tools  
- pgAdmin 4  
- Healthcheck endpoints  
- CLI-friendly API test commands  

---

## DevOps Architecture

### DevOps Foundations  
The project is built with a **DevOps-first approach**, ensuring:

- Immutable, containerized environments  
- Automated build/testing/deployment  
- Strict environment isolation  
- Reproducible deployments  
- Continuous monitoring  
- A “no manual steps” pipeline philosophy  

---

### CI/CD Pipeline Strategy  
The repository includes a GitHub Actions workflow that automates testing, scanning, container validation, deployment, and reporting. It runs on every push, daily, and manually when needed.

#### Pipeline Overview  
The workflow is divided into clear jobs:

#### 1. Python Tests and Checks  
- Installs dependencies  
- Runs pytest for unit tests  
- Ensures no broken code continues through the pipeline  

#### 2. Dependency and Security Scan  
- Uses pip-audit to scan Python dependencies  
- Fails early if a vulnerability is detected  

#### 3. Docker Build and API Testing  
- Starts a PostgreSQL service  
- Builds the project into a Docker image  
- Runs the API container  
- Performs health checks and basic CRUD tests  
- Saves logs automatically if something fails  

#### 4. Production URL Monitoring  
- Checks the live `/health` endpoint  
- Fails if the production deployment is unreachable  

#### 5. Conditional Deployment  
- If Python tests pass, triggers a Render deployment  
- Saves deployment responses as artifacts  

#### 6. Daily Summary Email  
- Generates a simple table of job results  
- Sends summary as an automated email  

#### Scalability  
The pipeline is modular and can easily grow to include more tools such as:

- flake8 or ruff for linting  
- black for formatting checks  
- mypy for type checking  
- Terraform workflows  
- AWS deployment stages  
- Database migrations  
- Frontend build processes  

This makes the CI/CD system flexible as the project expands.

---

## DevOps Competencies Gained

| Category | Skills Demonstrated |
|---------|----------------------|
| CI/CD Automation | GitHub Actions orchestration, build/test/deploy pipelines |
| Container Lifecycle | Docker building, tagging, pushing |
| Security Automation | Dependency/image scanning |
| Monitoring | Metrics testing, healthchecks |
| Release Engineering | Automated deployment triggers |
| Infrastructure Discipline | Config isolation, reproducible builds |
| Pipeline Resilience | Independent jobs + final summary |

---

## Technical Competencies Acquired  
- FastAPI async architecture  
- PostgreSQL async ORM  
- Pydantic multi-environment config  
- Rotating multi-channel logs  
- Monitoring middleware + `/stats`  
- Docker Compose multi-service orchestration  
- CI/CD pipeline practices  
- Render deployment flows  
- Automated API testing  

---

## Conceptual Understanding Gained  
- Environment Abstraction  
- Immutable Infrastructure  
- Metrics-first monitoring  
- Automation as the source of truth  
- Resilient pipelines  
- Unified backend + infra + CI/CD understanding  

---

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| Language | Python 3.11 |
| Framework | FastAPI (async) |
| ORM | SQLAlchemy Async + asyncpg |
| Database | PostgreSQL 15 |
| Infrastructure | Docker, Docker Compose |
| Admin Tool | pgAdmin |
| Configuration | Pydantic Settings |
| Logging | Python Logging + RotatingFileHandler |
| Monitoring | Custom Middleware + `/stats` |
| Server | Uvicorn / Gunicorn |
| Version Control | Git & GitHub |
| CI/CD | GitHub Actions |
| Deployment | Render |
| OS Environment | Linux (Debian base) |

---

