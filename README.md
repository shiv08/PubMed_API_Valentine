# PubMed Search Application 🔍

A modern web application built with FastAPI that provides an intuitive interface to search PubMed articles. The application includes both a user-friendly web interface and REST API endpoints for programmatic access.

## ✨ Features

### Search Capabilities
- 📚 **Title Search**: Find articles using keywords in titles
- 📝 **Abstract Search**: Search through article abstracts
- 📅 **Date-based Search**: Filter articles by publication date range

### Interface Options
- 🌐 **Web Interface**: Clean, responsive Bootstrap-based UI
- 🔌 **API Endpoints**: RESTful API with Swagger documentation

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Template Engine**: Jinja2
- **Frontend**: Bootstrap 5
- **Testing**: pytest
- **API Documentation**: Swagger/OpenAPI

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/pubmed-search-app.git
cd pubmed-search-app
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
uvicorn main:app --reload
```

5. **Access the Application**
- Web Interface: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs

## 📁 Project Structure

```
pubmed_webapp/
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_api.py        # API endpoint tests
│   └── test_pubmed_client.py  # PubMed client tests
├── static/
│   └── style.css          # Custom styles
├── templates/
│   ├── base.html          # Base template
│   └── index.html         # Main search interface
├── main.py                # FastAPI application
├── pubmed_client.py       # PubMed API client
└── requirements.txt       # Project dependencies
```

## 🔍 API Endpoints

### Title Search
```http
GET /api/search/title?keywords=cancer&max_results=5
```
- **Parameters**:
  - `keywords`: Search terms
  - `max_results`: Maximum number of results (default: 10)

### Abstract Search
```http
GET /api/search/abstract?keywords=covid&max_results=5
```
- **Parameters**:
  - `keywords`: Search terms
  - `max_results`: Maximum number of results (default: 10)

### Date Search
```http
GET /api/search/date?start_date=2024/01/01&end_date=2024/03/01&max_results=5
```
- **Parameters**:
  - `start_date`: Start date (YYYY/MM/DD)
  - `end_date`: End date (YYYY/MM/DD)
  - `max_results`: Maximum number of results (default: 10)

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_api.py
```

## 📈 Future Enhancements

### 1. Scalability Improvements
- [ ] **Caching Layer**
  - Redis implementation for response caching
  - Configurable cache timeouts
  - Distributed caching support

- [ ] **Database Integration**
  - PostgreSQL for search history
  - Async database operations
  - Connection pooling

- [ ] **Load Balancing**
  - Nginx load balancer implementation
  - Multiple server instances
  - Health check endpoints

- [ ] **Container Orchestration**
  - Docker containerization
  - Kubernetes deployment
  - Auto-scaling configuration

### 2. Performance Optimizations
- [ ] **Rate Limiting**
  - Redis-based rate limiting
  - Per-user and global limits
  - Custom rate limit policies

- [ ] **Parallel Processing**
  - Async request handling
  - Batch processing for large queries
  - Worker pools for CPU-intensive tasks

### 3. Monitoring and Logging
- [ ] **Metrics Collection**
  - Prometheus integration
  - Grafana dashboards
  - Custom metrics for search patterns

- [ ] **Logging System**
  - ELK stack integration
  - Structured logging
  - Log aggregation

### 4. High Availability
- [ ] **Service Discovery**
  - Consul integration
  - Dynamic service registration
  - Health monitoring

- [ ] **Failover Mechanisms**
  - Circuit breakers
  - Fallback strategies
  - Replica sets

### 5. Security Enhancements
- [ ] **Authentication System**
  - JWT implementation
  - OAuth2 integration
  - Role-based access control

### 6. Feature Additions
- [ ] Advanced search filters
- [ ] Export functionality (PDF, CSV)
- [ ] User dashboard
- [ ] Search history tracking
- [ ] Result sorting options

## 🔒 Security

- Input validation for all search parameters
- Rate limiting on API endpoints
- Error handling for invalid requests

## 🐛 Known Issues

- Limited to 100 results per query
- Date search requires specific format (YYYY/MM/DD)

## 🚀 Deployment Architecture

### Current Architecture
```
Client -> FastAPI Server -> PubMed API
```

### Planned Scalable Architecture
```
                                    ┌─── FastAPI Server 1 ───┐
Client -> Nginx Load Balancer ─────├─── FastAPI Server 2 ───├─── Redis Cache ─── PubMed API
                                    └─── FastAPI Server 3 ───┘
                                              │
                                              │
                                     PostgreSQL Database
```

## 📦 Containerization

### Planned Docker Setup
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
  redis:
    image: redis:alpine
  postgres:
    image: postgres:13
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact

- Developer Name - [Your Email]
- Project Link: [https://github.com/your-username/pubmed-search-app](https://github.com/your-username/pubmed-search-app)
