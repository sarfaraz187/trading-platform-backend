# trading-platform-backend

# 🛠️ User Service - FastAPI + Firebase + PostgreSQL

This is the **User Service** in a microservices-based architecture. It is responsible for handling authenticated user operations after Firebase Authentication.

## 🧱 Tech Stack

- **FastAPI** – Python web framework for high-performance APIs
- **PostgreSQL** – Stores user metadata (email, display name, etc.)
- **Firebase Admin SDK** – Verifies Firebase ID tokens
- **Docker** – Containerized microservice
- **NGINX / API Gateway** – Routes authenticated requests to this service

## 🔐 Authentication Flow

1. User signs up or logs in via Firebase Authentication (on the frontend).
2. Firebase issues a JWT (`ID Token`).
3. The frontend sends the token via `Authorization: Bearer <token>` to the API Gateway.
4. The API Gateway proxies the request to this service.
5. This service verifies the ID token using Firebase Admin SDK.
6. If valid, it creates or accesses the user in the PostgreSQL database using the Firebase `uid`.

### MVP

project-root/
├── api-gateway/ # Express.js
│ └── Dockerfile
│ └── main.py
├── user-service/ # FastAPI
│ └── Dockerfile
├── market-data-service/ # Node.js
│ └── Dockerfile
├── trading-service/ # Go + Gin
│ └── Dockerfile
├── docker-compose.yml
