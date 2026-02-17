> **Language**: [English](README.md) | [繁體中文](README.zh-TW.md)

# AgentMem - Agent Memory System

An efficient memory management system designed for AI Agents, supporting vector embeddings, semantic search, collaborative sharing, and a user-friendly Web UI dashboard.

## Version

**0.3.0** - Complete Implementation with Web UI, SDK, CLI & Full Documentation

## Features

### ✨ Core Functionality
- **Memory Management**: Create, update, delete, and query memories
- **Vector Embeddings**: Automatically generate text embeddings (supports local and OpenAI API)
- **Semantic Search**: Intelligent search based on vector similarity
- **Collaborative Sharing**: Securely share memories between Agents
- **Fine-grained Permissions**: Three-level permission control (read, write, share)
- **High-performance Search**: 100 memories <200ms, 1000 memories <500ms

### 🖥️ User Interfaces
- **Web UI Dashboard**: Professional Streamlit-based web interface for non-technical users
  - Create, search, manage, and share memories visually
  - Real-time statistics and performance metrics
  - Responsive and intuitive design
- **Python SDK**: Simple and Pythonic API for developers
  - Object-oriented interface
  - Comprehensive error handling
  - Full feature support
- **Command-line Interface (CLI)**: Terminal tool for power users
  - Configuration management
  - Batch operations
  - Rich formatted output

### 📚 Documentation
- **5-minute Quick Start Guide** (English + 繁體中文)
- **Detailed Usage Guide** (English + 繁體中文)
- **10 Code Examples** (English + 繁體中文)
- **Complete API Reference** (English + 繁體中文)
- **Troubleshooting Guide** (English + 繁體中文)
- All documentation with language switchers

### 🔒 Security Features
- Bearer Token authentication
- Permission verification system
- Access Control List (ACL)
- Memory visibility levels (private/shared/public)

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
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

3. **Start the backend server**
   ```bash
   python -m src.main
   ```
   - Server runs on: http://localhost:8000
   - Health check: http://localhost:8000/health

### Choose Your Interface

#### 🌐 Web UI (Recommended for beginners)
```bash
streamlit run ui/app.py
```
- Access at: http://localhost:8501
- Intuitive visual interface
- Perfect for non-technical users

#### 🐍 Python SDK (For developers)
```python
from src.client import AgentMemClient

client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id="your-agent-id"
)

memory = client.create_memory(
    content="Your memory content",
    type="knowledge",
    category="ai"
)

results = client.search("search query")
```

#### 💻 Command-line Interface (For power users)
```bash
# Initialize CLI
python -m src.cli.main init

# Create memory
python -m src.cli.main create "Your memory content"

# Search
python -m src.cli.main search "query"

# View statistics
python -m src.cli.main stats
```

### Documentation
- 🚀 [5-Minute Quick Start](docs/QUICKSTART.md)
- 📖 [Detailed Usage Guide](docs/USAGE_GUIDE.md)
- 💻 [Code Examples](docs/EXAMPLES.md)
- 🔌 [API Reference](docs/API_REFERENCE.md)
- 🛠️ [Troubleshooting](docs/TROUBLESHOOTING.md)

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
│   ├── api/                 # REST API routes
│   │   ├── memories.py      # Memory CRUD API
│   │   ├── search.py        # Search API
│   │   └── sharing.py       # Sharing API
│   ├── client/              # Python SDK
│   │   ├── client.py        # Main client class
│   │   ├── models.py        # Data models
│   │   └── exceptions.py    # Exception handling
│   ├── cli/                 # Command-line interface
│   │   ├── main.py          # CLI entry point
│   │   ├── commands.py      # CLI commands
│   │   ├── config.py        # Configuration management
│   │   └── formatter.py     # Output formatting
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
├── ui/                      # Web UI Dashboard (Streamlit)
│   ├── app.py               # Main Streamlit app
│   └── features/            # UI feature modules
│       ├── create.py        # Create memory page
│       ├── search.py        # Search memory page
│       ├── manage.py        # Manage memory page
│       └── share.py         # Share memory page
├── docs/                    # Documentation (bilingual)
│   ├── QUICKSTART.md        # 5-minute quick start
│   ├── USAGE_GUIDE.md       # Detailed usage guide
│   ├── EXAMPLES.md          # Code examples
│   ├── API_REFERENCE.md     # API documentation
│   └── TROUBLESHOOTING.md   # Problem solving
├── examples/                # Example scripts
│   └── quick_start.py       # Quick start example
├── tests/                   # Tests
│   ├── test_embeddings.py
│   ├── test_search.py
│   ├── test_permissions.py
│   ├── test_integration.py
│   └── test_performance.py
├── requirements.txt         # Python dependencies
├── Makefile                 # Build automation
└── README.md                # Project README
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

## What's New in v0.3.0

✨ **New Features:**
- 🖥️ Professional Web UI Dashboard (Streamlit)
- 🐍 Complete Python SDK with full API support
- 💻 Command-line Interface (CLI) tool
- 📚 Comprehensive bilingual documentation (English + 繁體中文)
- 📖 10 practical code examples
- 🧪 Functional test scripts

🎯 **Improvements:**
- Streamlined user interface for non-technical users
- Pythonic SDK for easy integration
- CLI for power users and automation
- Complete documentation with 5 usage guides
- Better error handling and user feedback

---

**Last Updated**: February 17, 2026
**Version**: 0.3.0
**Status**: ✅ Production Ready
**Interfaces**: Web UI • SDK • CLI
**Documentation**: English • 繁體中文
