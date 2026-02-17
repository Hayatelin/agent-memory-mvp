> **Language**: [English](CHANGELOG.md) | [繁體中文](CHANGELOG.zh-TW.md)

# Changelog

All notable changes to this project are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/) rules.
Version numbering follows [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-02-17

### Added

- **Vector Embedding System**
  - EmbeddingService supports local models and OpenAI API
  - Batch embedding processing capability
  - Automatic embedding validation and normalization
  - Embedding utility functions (embedding.py)

- **Semantic Search Engine**
  - SearchService implements semantic search
  - Cosine similarity calculation
  - Similarity threshold filtering
  - Search result ranking

- **Memory Management API**
  - POST /memories - Create memory
  - GET /memories - List query
  - GET /memories/{id} - Detail query
  - PUT /memories/{id} - Update memory
  - DELETE /memories/{id} - Delete memory

- **Search API**
  - POST /memories/search - Semantic search
  - GET /memories/search/stats - Search statistics

- **Sharing Management API**
  - POST /memories/{id}/share - Share memory
  - GET /memories/{id}/shared-with - Query sharing
  - DELETE /memories/{id}/share/{agent_id} - Revoke sharing

- **Permission Management System**
  - PermissionManager fine-grained permission control
  - Read, edit, share permission validation
  - Access Control List (ACL) support
  - Memory visibility levels (private/shared/public)

- **Authentication System**
  - Bearer Token authentication
  - Agent identity authentication
  - Request-level authorization verification

- **Test Suite**
  - Embedding service tests (7 tests)
  - Search service tests (6 tests)
  - Permission management tests (8 tests)
  - End-to-end integration tests (4 tests)
  - Performance benchmark tests (5 tests)

- **Documentation**
  - Complete README.md
  - Feature update guide (WEEK2_UPDATES.md)
  - Integration report (INTEGRATION_REPORT.md)
  - Contributing guide (CONTRIBUTING.md)

- **Development Tools**
  - Docker & Docker Compose configuration
  - GitHub Actions CI/CD workflow
  - Pytest test framework configuration
  - Git workflow configuration

### Changed

- Database model added embedding-related fields
  - embeddings: JSON field to store vectors
  - embedding_model: Name of the model used
  - embedding_updated_at: Last update time

- Application version updated to 0.2.0

### Fixed

- Fixed UUID type compatibility issue in SQLite
- Fixed CRLF line ending issue on Windows platform

### Known Issues

- Embedding storage uses JSON format (future plan: upgrade to vector database)
- Authentication uses simple UUID Token (future plan: upgrade to JWT)
- No built-in caching layer (optional Redis integration)

## [0.1.0] - Unreleased

Initial project setup and planning.

---

## Version Release Process

### Semantic Versioning

- MAJOR version: Incompatible API changes
- MINOR version: Backward compatible new features
- PATCH version: Backward compatible bug fixes

### Release Checklist

Before releasing a new version:

- [ ] All tests pass
- [ ] Code coverage >85%
- [ ] Documentation update complete
- [ ] CHANGELOG.md updated
- [ ] README.md updated (if needed)
- [ ] Version number updated (src/main.py)
- [ ] Create git tag
- [ ] Update GitHub Release

### Release Commands

```bash
# 1. Update version number
# Edit version="x.y.z" in src/main.py

# 2. Update CHANGELOG.md
# Add new version information

# 3. Commit changes
git add CHANGELOG.md src/main.py
git commit -m "chore: Bump version to x.y.z"

# 4. Create tag
git tag -a vx.y.z -m "Release version x.y.z"

# 5. Push
git push origin main
git push origin vx.y.z

# 6. GitHub will auto-deploy
```

---

## Contributors

Thanks to the following people for contributing to this project:

- Claude Code (claude@anthropic.com) - Initial development

---

## License

This project uses the MIT License. See the LICENSE file for details.
