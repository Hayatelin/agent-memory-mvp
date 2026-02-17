> **Language**: [English](README.md) | [繁體中文](README.zh-TW.md)

# AgentMem - Agent Memory System

An efficient memory management system designed for AI Agents, supporting vector embeddings, semantic search, and collaborative sharing.

## Version

**0.2.0** - Week 2-3 Enhanced Version

## Features

### ✨ Core Functionality
- **Memory Management**: Create, update, delete, and query memories
- **Vector Embeddings**: Automatically generate text embeddings (supports local and OpenAI API)
- **Semantic Search**: Intelligent search based on vector similarity
- **Collaborative Sharing**: Securely share memories between Agents
- **Fine-grained Permissions**: Three-level permission control (read, write, share)
- **High-performance Search**: 100 memories <200ms, 1000 memories <500ms

### 🔒 Security Features
- Bearer Token authentication
- Permission verification system
- Access Control List (ACL)
- Memory visibility levels (private/shared/public)

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- 4GB+ RAM (for model loading)

### Installation and Running

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent-memory-mvp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Docker containers**
   ```bash
   make docker-up
   ```

4. **Run tests**
   ```bash
   make test
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## API Endpoints

### Memory API
| Method | Route | Description |
|--------|-------|-------------|
| POST | /memories | Create memory |
| GET | /memories | List memories |
| GET | /memories/{id} | Get memory |
| PUT | /memories/{id} | Update memory |
| DELETE | /memories/{id} | Delete memory |

### Search API
| Method | Route | Description |
|--------|-------|-------------|
| POST | /memories/search | Semantic search |
| GET | /memories/search/stats | Search statistics |

### Sharing API
| Method | Route | Description |
|--------|-------|-------------|
| POST | /memories/{id}/share | Share memory |
| GET | /memories/{id}/shared-with | Query sharing |
| DELETE | /memories/{id}/share/{agent_id} | Revoke sharing |

## Usage Examples

### Authentication
```bash
# Use Bearer Token authentication
Authorization: Bearer <agent-uuid>
```

### Create Memory
```bash
curl -X POST http://localhost:8000/memories \
  -H "Authorization: Bearer <agent-uuid>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "knowledge",
    "category": "ai",
    "content": "Machine learning is an important branch of artificial intelligence",
    "visibility": "private"
  }'
```

### Search Memory
```bash
curl -X POST http://localhost:8000/memories/search \
  -H "Authorization: Bearer <agent-uuid>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "limit": 10,
    "similarity_threshold": 0.3
  }'
```

## Project Structure

```
agent-memory-mvp/
├── src/
│   ├── api/                 # API routes
│   │   ├── memories.py      # Memory CRUD API
│   │   ├── search.py        # Search API
│   │   └── sharing.py       # Sharing API
│   ├── services/            # Business services
│   │   ├── embedding_service.py
│   │   └── search_service.py
│   ├── core/                # Core logic
│   │   └── permissions.py
│   ├── models/              # Data models
│   │   └── models.py
│   ├── db/                  # Database
│   │   └── database.py
│   ├── utils/               # Utility functions
│   │   ├── auth.py
│   │   └── embedding.py
│   └── main.py              # FastAPI application
├── tests/                   # Tests
│   ├── test_embeddings.py
│   ├── test_search.py
│   ├── test_permissions.py
│   ├── test_integration.py
│   └── test_performance.py
├── docs/                    # Documentation
│   └── WEEK2_UPDATES.md
├── requirements.txt         # Dependencies
├── docker-compose.yml       # Docker configuration
├── Dockerfile
├── Makefile
└── README.md
```

## Testing

### Run all tests
```bash
pytest tests/ -v
```

### Run specific tests
```bash
pytest tests/test_embeddings.py -v
pytest tests/test_search.py -v
pytest tests/test_permissions.py -v
pytest tests/test_integration.py -v
pytest tests/test_performance.py -v
```

### Generate coverage report
```bash
pytest --cov=src tests/
```

## Performance Benchmarks

Using all-MiniLM-L6-v2 model:

| Operation | Scale | Time |
|-----------|-------|------|
| Embedding generation | 100 texts | ~1s |
| Search | 100 memories | <200ms |
| Search | 1000 memories | <500ms |
| Similarity calculation | 1000 vectors | <100ms |

## Environment Variables

```bash
# Database configuration
DATABASE_URL=sqlite:///./test.db  # Development
DATABASE_URL=postgresql://user:password@localhost/agentmem  # Production

# Redis (Optional)
REDIS_URL=redis://localhost:6379

# OpenAI API (Optional)
OPENAI_API_KEY=sk-...
```

## Development Guide

### Adding New API Endpoint
1. Create new route module in `src/api/`
2. Include route in `src/main.py`
3. Add tests in `tests/`

### Adding New Service
1. Implement service class in `src/services/`
2. Add corresponding tests
3. Use the service in API

### Updating Data Models
1. Modify `src/models/models.py`
2. Create and run database migrations
3. Update related tests

## Troubleshooting

### Model Download Failed
```bash
# Manually download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Database Connection Error
```bash
# Check Docker status
docker-compose ps

# Restart service
make docker-restart
```

### Authentication Failed
Ensure you include a valid Bearer Token in the request header:
```bash
Authorization: Bearer <valid-uuid>
```

## Contributing

Pull Requests and Issues are welcome.

## License

MIT License

## Contact

- Project Homepage: https://github.com/...
- Documentation: http://localhost:8000/docs

---

**Last Updated**: February 17, 2026
**Version**: 0.2.0
**Status**: ✅ Production Ready
