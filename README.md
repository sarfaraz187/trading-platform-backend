# Trading Platform Backend

A microservices-based trading platform backend built with modern technologies.

## 🏗️ Architecture Overview

This platform follows a microservices architecture pattern with multiple specialized services connected through an API Gateway:

- **API Gateway** - FastAPI service that handles authentication and routes requests to appropriate microservices
- **User Service** - Manages user profiles and account settings
- **Market Data Service** - Provides real-time and historical market data
- **Trading Service** - Handles order execution and portfolio management

## 🧱 Tech Stack

- **FastAPI** - High-performance Python web framework for building APIs
- **PostgreSQL** - Relational database for persistent storage
- **Firebase Authentication** - Secure user authentication
- **NGINX** - Web server and reverse proxy for load balancing
- **Docker** - Containerization for consistent deployment
- **httpx** - Asynchronous HTTP client for Python

## 🔐 Authentication Flow

1. User signs up or logs in via Firebase Authentication (on the frontend)
2. Firebase issues a JWT (`ID Token`)
3. The frontend sends the token via `Authorization: Bearer <token>` to the API Gateway
4. API Gateway verifies the token using Firebase Admin SDK
5. If valid, the API Gateway forwards the request to appropriate microservice with user information
6. Each service processes the authenticated request with user context

## 📁 Project Structure

```
trading-platform-backend/
├── api-gateway/              # FastAPI-based API Gateway
│   ├── lib/                  # Shared libraries
│   │   └── firebase_auth.py  # Firebase authentication utilities
│   ├── routers/              # API route definitions
│   │   └── users.py          # User service routing
│   └── Dockerfile
├── user-service/             # User profile management service
│   └── Dockerfile
├── market-data-service/      # Market data provider service
│   └── Dockerfile
├── trading-service/          # Trading and order execution service
│   └── Dockerfile
├── nginx/                    # NGINX configuration files
│   └── Dockerfile
└── docker-compose.yml        # Service orchestration
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Firebase project credentials
- Python 3.8+

### Setup and Running

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/trading-platform-backend.git
   cd trading-platform-backend
   ```

2. Configure environment variables in a `.env` file:

   ```
   USER_SERVICE_URL=http://user-service:8000
   FIREBASE_CREDENTIALS=path/to/firebase-credentials.json
   ```

3. Start the services:

   ```bash
   docker-compose up -d
   ```

4. Access the API documentation at http://localhost:8000/docs

## 📝 API Documentation

- **API Gateway**: http://localhost:8000/docs
- **User Service**: http://localhost:8001/docs
- **Market Data Service**: http://localhost:8002/docs
- **Trading Service**: http://localhost:8003/docs

## 🔄 Service Communication

Services communicate through HTTP using the API Gateway as an intermediary. The gateway:

1. Authenticates incoming requests
2. Forwards user context to the appropriate service
3. Returns responses back to the client

NGINX serves as the front-facing reverse proxy that:

1. Handles SSL termination
2. Performs load balancing
3. Routes requests to the API Gateway
4. Serves static assets when needed

## 🚀 CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

### Workflow

1. **Trigger**: The pipeline is triggered on pushes to the main branch
2. **Build**: Docker images are built for each microservice using Docker Buildx
3. **Push**: Images are pushed to DockerHub with appropriate tags
4. **Deploy**: Deployment to EC2 instance via SSH

### Components Deployed

- NGINX reverse proxy
- API Gateway service
- User service
- Other microservices as needed

### Infrastructure

The application is deployed to AWS EC2 instances in a development environment, with:
- Docker Compose for container orchestration
- DockerHub as the container registry
- GitHub Actions as the CI/CD platform

To view workflow details, check `.github/workflows/deploy.yml`.

## 🧪 Testing

Run tests for individual services:

```bash
cd service-name
pytest
```

## 📦 Deployment

The platform can be deployed to any environment supporting Docker containers:

- AWS EC2 (currently configured)
- Kubernetes
- AWS ECS
- Google Cloud Run
- Azure Container Instances

For production deployment, update environment variables and configuration files as needed.
