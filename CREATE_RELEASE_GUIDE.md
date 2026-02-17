# Creating GitHub Release for v0.3.0

This guide explains how to create a GitHub release for AgentMem v0.3.0.

## Option 1: Using the Web Interface (Easiest)

### Steps:

1. **Go to GitHub Releases**
   - Visit: https://github.com/Hayatelin/agent-memory-mvp/releases/new

2. **Fill in Release Information**
   - **Tag version**: `v0.3.0`
   - **Release title**: `v0.3.0 - Complete Implementation with Web UI, SDK & CLI`
   - **Description**: Copy the entire content from `RELEASE_NOTES_v0.3.0.md`

3. **Configure Options**
   - [ ] This is a draft release
   - [ ] This is a pre-release
   - [ ] Do not generate release notes automatically

4. **Publish Release**
   - Click the "Publish release" button

### Result:
- Release will be published immediately
- Will appear in the releases page
- Will show up in release history

---

## Option 2: Using the Automation Script

### Prerequisites:
- Python 3.8+
- GitHub Personal Access Token

### Getting a GitHub Token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo` (for repository access)
4. Copy the generated token

### Running the Script:

**Method A: Command-line arguments**
```bash
python create_release.py ghp_xxxxxxxxxxxx Hayatelin/agent-memory-mvp
```

**Method B: Environment variables**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
export GITHUB_REPO=Hayatelin/agent-memory-mvp
python create_release.py
```

**Method C: Interactive**
```bash
python create_release.py
# Follow the prompts
```

### Expected Output:
```
======================================================================
  Creating GitHub Release
======================================================================

Repository: Hayatelin/agent-memory-mvp
Tag: v0.3.0
Title: v0.3.0 - Complete Implementation with Web UI, SDK & CLI
Draft: False
Pre-release: False

Release notes length: 2847 characters

Sending request to GitHub API...

✅ Release created successfully!

Release ID: 123456789
URL: https://github.com/Hayatelin/agent-memory-mvp/releases/tag/v0.3.0
Created at: 2026-02-17T10:30:00Z
Published at: 2026-02-17T10:30:00Z

You can view your release at:
  https://github.com/Hayatelin/agent-memory-mvp/releases/tag/v0.3.0
```

---

## Option 3: Using GitHub CLI (If Available)

If you have `gh` CLI installed:

```bash
gh release create v0.3.0 --title "v0.3.0 - Complete Implementation" --notes-file RELEASE_NOTES_v0.3.0.md
```

---

## Release Details

### Tag: v0.3.0
- Already pushed to GitHub
- Ready for release

### Release Notes Location
- File: `RELEASE_NOTES_v0.3.0.md`
- Automatically used by the script
- 284 lines, comprehensive information

### Key Information Included
- ✅ New features (Web UI, SDK, CLI)
- ✅ Project statistics
- ✅ Quick start guides
- ✅ Documentation links
- ✅ Testing information
- ✅ Security features
- ✅ Directory structure

---

## Verification

After creating the release, verify it at:

```
https://github.com/Hayatelin/agent-memory-mvp/releases/tag/v0.3.0
```

You should see:
- ✅ Release title
- ✅ Release date (Feb 17, 2026)
- ✅ Full release notes
- ✅ "Latest" badge (if it's the latest release)

---

## Rollback (If Needed)

To delete a release (only the release, not the tag):

**Via Web UI:**
1. Go to the release page
2. Click the three dots menu
3. Select "Delete"

**Via Script:**
```bash
curl -X DELETE https://api.github.com/repos/Hayatelin/agent-memory-mvp/releases/{release_id} \
  -H "Authorization: token YOUR_TOKEN"
```

---

## Troubleshooting

### "Tag not found"
- Ensure tag v0.3.0 exists: `git tag v0.3.0`
- Push tags: `git push origin v0.3.0`

### "Invalid credentials"
- Check your GitHub token is valid
- Token must have `repo` scope
- Don't share your token!

### "Release already exists"
- Delete the existing release first
- Or use a different version tag

### Script doesn't work
- Ensure you have requests library: `pip install requests`
- Check Python version: Python 3.8+
- Verify file paths are correct

---

## Best Practices

✅ **Always test** before publishing
✅ **Include comprehensive** release notes
✅ **Tag commits** before creating releases
✅ **Keep** a consistent tagging scheme
✅ **Announce** the release to users
✅ **Update** documentation with new version

---

## Next Steps

After creating the release:

1. **Announce the release**
   - Update project website
   - Post on social media
   - Send to mailing list

2. **Pin the release**
   - Highlight important features
   - Link from README

3. **Update documentation**
   - Mark old docs as archived
   - Add links to new docs

4. **Monitor feedback**
   - Watch for issues
   - Respond to user feedback

---

## Additional Resources

- [GitHub Release Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Creating Tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [GitHub API Reference](https://docs.github.com/en/rest/releases/releases)

---

## Release Information

| Item | Value |
|------|-------|
| Version | v0.3.0 |
| Release Date | February 17, 2026 |
| Status | Production Ready ✅ |
| Repository | Hayatelin/agent-memory-mvp |
| Release Notes | RELEASE_NOTES_v0.3.0.md |
| Tag Status | Already pushed |

---

**Choose your preferred method above and create the release!** 🚀
