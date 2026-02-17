> **Language**: [English](CONTRIBUTING.md) | [繁體中文](CONTRIBUTING.zh-TW.md)

# Contributing Guide

Thank you for your interest in the AgentMem project! This document will help you get started with contributing.

## Code of Conduct

This project has adopted the Contributor Covenant. Participants should adhere to the following principles:

- Respect all contributors
- Accept constructive criticism
- Focus on what is best for the project and community
- Show empathy toward community members

## How to Contribute

### Reporting Bugs

When reporting a bug, please:

1. Verify the bug hasn't already been reported
2. Use a descriptive title
3. Provide detailed reproduction steps
4. Describe the actual behavior versus expected behavior
5. Include environment information (OS, Python version, etc.)

### Proposing Features

When proposing a new feature, please:

1. Use a descriptive title
2. Provide a detailed description of the use case
3. List possible implementation approaches
4. Explain the expected benefits

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/agent-memory-mvp.git
   cd agent-memory-mvp
   ```

2. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow PEP 8 code style
   - Add type hints
   - Write docstrings
   - Add corresponding tests

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

5. **Push to remote**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use the provided PR template
   - Clearly describe your changes
   - Link related Issues

## Development Setup

### Required Tools

- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**
   ```bash
   pytest tests/ -v
   ```

3. **Code quality checks**
   ```bash
   black src tests
   isort src tests
   flake8 src tests
   mypy src
   ```

4. **Start the application**
   ```bash
   python -m uvicorn src.main:app --reload
   ```

## Code Style

### Python Code Style

Follow PEP 8:
- Line length: maximum 120 characters
- Indentation: 4 spaces
- Naming: snake_case for functions/variables, PascalCase for classes

### Type Hints

All functions should have type hints:

```python
async def get_embeddings(
    text: str,
    model_name: Optional[str] = None
) -> List[float]:
    """Get embeddings for the input text.

    Args:
        text: Input text
        model_name: Model name (optional)

    Returns:
        List of embedding values

    Raises:
        ValueError: If text is empty
    """
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description.

    More detailed description (if needed).

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: Description of exception

    Example:
        >>> function_name("test", 42)
        True
    """
```

## Testing

### Writing Tests

- Use the pytest framework
- One test file per source file
- Naming: test_*.py or *_test.py
- Test function naming: test_*

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific file
pytest tests/test_embeddings.py -v

# Run specific test
pytest tests/test_embeddings.py::test_embedding_service_basic -v

# Generate coverage report
pytest tests/ --cov=src --cov-report=html
```

## Commit Messages

Follow this format:

```
[TYPE] Brief description

Detailed explanation (optional)

Related issues: #123
```

Types include:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation update
- **refactor**: Code refactoring
- **test**: Test-related changes
- **perf**: Performance optimization
- **chore**: Build, dependencies, etc.

Example:
```
feat: Add support for multiple embedding models

- Add model selection parameter to EmbeddingService
- Implement model caching mechanism
- Update tests to cover new functionality

Related issues: #42
```

## Pull Request Process

1. **Test locally**
   - Run all tests
   - Check code quality
   - Verify documentation

2. **Submit PR**
   - Use the template to fill in information
   - Clearly describe your changes
   - Link related Issues

3. **Code Review**
   - Maintainers will review your code
   - May request changes
   - Will be merged after approval

4. **Merge**
   - PR is merged into main branch
   - Your name will be added to the contributors list

## Building and Deployment

### Local Docker Build

```bash
docker build -t agent-memory-mvp:local .
docker-compose up -d
```

### Release Version

When releasing a version:
1. Update version number (src/main.py)
2. Update CHANGELOG.md
3. Create git tag
4. GitHub Actions will auto-deploy

## Documentation

- Update README.md if you change usage
- Add docstrings to new functions
- Update WEEK2_UPDATES.md if there are significant changes
- Keep documentation in sync

## Bilingual Documentation Maintenance

This project maintains documentation in both English and Traditional Chinese.

### When Updating Documentation

1. **Always update both versions** when making documentation changes
2. **Keep structure identical** between language versions
3. **Translate accurately** - use technical terminology consistently
4. **Test both versions** before submitting PR
5. **Verify language switchers** work correctly

### File Naming Convention

- English: `filename.md`
- Traditional Chinese: `filename.zh-TW.md`

### Making Changes

When updating a document:
1. Edit the English version first (primary)
2. Update the corresponding Chinese version
3. Ensure technical details match exactly
4. Commit both versions together

Example commit:
```bash
git commit -m "docs: Update README with new API endpoint

- Update README.md (English)
- Update README.zh-TW.md (Chinese)
- Add documentation for /new-endpoint
"
```

### Getting Translation Help

If you need help translating:
- Open an issue with `translation-needed` label
- Submit PR with English version only
- Community will assist with Chinese translation

## License

By submitting code, you agree to release it under the MIT License.

## Issues and Discussions

- Use Issues to report bugs and feature requests
- Use Discussions for general discussions
- Contact maintainers directly for security-related issues

---

Thank you for your contribution! 🎉
