# GoldenCity Memo API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![API](https://img.shields.io/badge/API-REST-orange.svg)]()
[![Tests](https://img.shields.io/badge/tests-34%20passed-brightgreen.svg)]()

A high-performance RESTful API for memo management built with FastAPI. Features full CRUD operations with in-memory storage for rapid development and testing.

## 🎯 Overview

The **GoldenCity Memo API** is a RESTful API developed for note/memo management, offering complete CRUD operations (Create, Read, Update, Delete) with in-memory storage for fast development and testing.

## 🚀 Features

- **Fast & Modern**: Built with FastAPI for high performance
- **Full CRUD**: Create, Read, Update, Delete operations
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Data Validation**: Pydantic models for robust data handling
- **In-Memory Storage**: Quick setup without database dependencies
- **CORS Support**: Ready for frontend integration
- **Comprehensive Logging**: Structured logging throughout the application
- **Complete Test Suite**: 34 tests covering all scenarios
- **Type Safety**: Full type hints for better code quality

## 📝 Purpose & Use Cases

### Main Objectives
Provide a simple and efficient solution for:
- **Note Creation** with title and content
- **List All Notes** ordered by creation date
- **Search Specific Notes** by unique ID
- **Partial or Complete Updates** of existing notes
- **Note Deletion** when needed

### Use Cases
- Annotation system for GoldenCity platform
- Real estate property notes
- Meeting memos
- General user observations
- Rapid prototyping of features

## 📋 Requirements

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- pytest (for testing)

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/goldencity-memo-api.git
   cd goldencity-memo-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

1. **Start the server**
   ```bash
   # Option 1: Using the startup script
   python run.py
   
   # Option 2: Using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**
   - **Base URL**: `http://localhost:8000`
   - **Interactive Docs**: `http://localhost:8000/docs`
   - **ReDoc**: `http://localhost:8000/redoc`

## 📚 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/` | Health check | 200 |
| `POST` | `/notes` | Create a new memo | 201, 422 |
| `GET` | `/notes` | Get all memos | 200 |
| `GET` | `/notes/{id}` | Get memo by ID | 200, 404 |
| `PUT` | `/notes/{id}` | Update memo by ID | 200, 404, 422 |
| `DELETE` | `/notes/{id}` | Delete memo by ID | 204, 404 |

### Example Usage

**Health Check:**
```bash
curl -X GET "http://localhost:8000/"
```

**Create a memo:**
```bash
curl -X POST "http://localhost:8000/notes" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Meeting Notes",
       "content": "Discuss API implementation and testing strategies"
     }'
```

**Get all memos:**
```bash
curl -X GET "http://localhost:8000/notes"
```

**Update a memo:**
```bash
curl -X PUT "http://localhost:8000/notes/{id}" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Updated Meeting Notes",
       "content": "Implementation completed successfully"
     }'
```

**Delete a memo:**
```bash
curl -X DELETE "http://localhost:8000/notes/{id}"
```

## 📊 Data Model

```json
{
  "id": "uuid4-string",
  "title": "string (1-200 chars)",
  "content": "string (min 1 char)",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 🏗️ Project Structure

```
goldencity-memo-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic data models
│   ├── routes.py        # API route handlers
│   └── storage.py       # In-memory storage management
├── tests/
│   ├── __init__.py
│   ├── test_api.py      # API endpoint tests
│   └── test_storage.py  # Storage layer unit tests
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Modern Python project configuration
├── run.py              # Quick start script
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation (English)
└── GoldenCity_Memo_API.postman_collection.json  # Postman collection
```

## 🧪 Testing

### Run Automated Tests
```bash
# All tests (34 tests)
pytest

# With coverage report
pytest --cov=app

# Specific test file
pytest tests/test_api.py

# Specific test class
pytest tests/test_api.py::TestNoteCreation
```

### Test Coverage
- **Unit Tests**: Storage layer operations
- **Integration Tests**: API endpoints
- **Validation Tests**: Input validation scenarios
- **Error Tests**: 404, 422, 500 error cases
- **Mocked Tests**: Simulated failure scenarios
- **End-to-End Tests**: Complete CRUD workflows

### Using Postman
Import the `GoldenCity_Memo_API.postman_collection.json` file into Postman for interactive testing.

## 🛠️ Technology Choices

### FastAPI
**Why we chose it:**
- **Performance**: One of the fastest Python frameworks
- **Auto Documentation**: Integrated Swagger UI and ReDoc
- **Type Hints**: Native Python type system support
- **Auto Validation**: Pydantic integration
- **Modern Standards**: async/await and OpenAPI support

### Pydantic
**Why we chose it:**
- **Data Validation**: Automatic and robust
- **Serialization**: Native JSON support
- **Type Safety**: Perfect integration with type hints
- **Performance**: C-level validation (via Rust)

### In-Memory Storage
**Why we chose it:**
- **Simplicity**: No database configuration needed
- **Speed**: Instant data access
- **Prototyping**: Ideal for development and testing

## ⚖️ Advantages & Disadvantages

### ✅ Advantages

**Technical:**
- High performance with FastAPI + Uvicorn
- Type safety reduces bugs
- Automatic documentation always up-to-date
- Robust data validation with Pydantic
- Clean architecture facilitates testing

**Development:**
- Rapid development and prototyping
- Excellent developer experience
- Easy maintenance and scalability
- Follows industry best practices

### ❌ Disadvantages

**Current Limitations:**
- **Persistence**: Data lost on restart
- **Concurrency**: No concurrent access control
- **Scalability**: Limited to single instance
- **Production**: Needs real database integration

**Missing Features:**
- Authentication and authorization
- Rate limiting
- Caching mechanisms
- Data backup and recovery

## 🔧 Development

**Code formatting:**
```bash
black app/ tests/
```

**Linting:**
```bash
flake8 app/ tests/
```

**Type checking:**
```bash
mypy app/
```

## 🚀 Deployment

**Development server:**
```bash
python run.py
```

**Production server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker (optional):**
```bash
docker build -t goldencity-memo-api .
docker run -p 8000:8000 goldencity-memo-api
```

## 🤝 Integration

This API can be integrated into the GoldenCity platform to provide memo functionality for users to take notes about properties, meetings, or general observations.

### Future Enhancements
- **Database Integration**: PostgreSQL/MongoDB support
- **Authentication**: JWT or OAuth2 implementation
- **User Context**: Associate notes with users
- **Property Context**: Link notes to properties
- **Pagination**: For large datasets
- **Search & Filters**: Advanced querying capabilities
- **Real-time Updates**: WebSocket support
- **Audit Trail**: Change tracking and history

## 📖 Documentation

- **English**: This README file
- **API Docs**: Available at `/docs` when running the server
- **Postman Collection**: Import the JSON file for interactive testing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨💻 Author

Developed with ❤️ by Jaqueline Monteiro.
