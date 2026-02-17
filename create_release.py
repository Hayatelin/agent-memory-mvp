#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GitHub Release Creator for AgentMem v0.3.0

This script creates a GitHub release using the GitHub REST API.

Usage:
    python create_release.py <github_token> <repository>

Example:
    python create_release.py ghp_xxxx Hayatelin/agent-memory-mvp

Note:
    - Requires GITHUB_TOKEN environment variable or command-line argument
    - Repository format: owner/repo_name
    - Tag must already exist in Git
"""

import requests
import os
import sys
from pathlib import Path

# Release information
RELEASE_TAG = "v0.3.0"
RELEASE_TITLE = "v0.3.0 - Complete Implementation with Web UI, SDK & CLI"
RELEASE_DRAFT = False
RELEASE_PRERELEASE = False

# Read release notes from file
RELEASE_NOTES_FILE = Path(__file__).parent / "RELEASE_NOTES_v0.3.0.md"

def read_release_notes():
    """Read release notes from file"""
    if RELEASE_NOTES_FILE.exists():
        with open(RELEASE_NOTES_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "See RELEASE_NOTES_v0.3.0.md for details"

def create_release(token, repo, tag=RELEASE_TAG, title=RELEASE_TITLE):
    """
    Create a GitHub release using the REST API

    Args:
        token: GitHub personal access token
        repo: Repository in format owner/repo
        tag: Git tag to create release from
        title: Release title

    Returns:
        dict: Release information or error
    """

    url = f"https://api.github.com/repos/{repo}/releases"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    body = read_release_notes()

    payload = {
        "tag_name": tag,
        "name": title,
        "body": body,
        "draft": RELEASE_DRAFT,
        "prerelease": RELEASE_PRERELEASE,
        "generate_release_notes": False
    }

    print(f"\n{'='*70}")
    print("  Creating GitHub Release")
    print(f"{'='*70}\n")
    print(f"Repository: {repo}")
    print(f"Tag: {tag}")
    print(f"Title: {title}")
    print(f"Draft: {RELEASE_DRAFT}")
    print(f"Pre-release: {RELEASE_PRERELEASE}")
    print(f"\nRelease notes length: {len(body)} characters")

    print("\nSending request to GitHub API...")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 201:
            result = response.json()
            print("\n✅ Release created successfully!\n")
            print(f"Release ID: {result['id']}")
            print(f"URL: {result['html_url']}")
            print(f"Created at: {result['created_at']}")
            print(f"Published at: {result['published_at']}")
            print(f"\nYou can view your release at:")
            print(f"  {result['html_url']}")
            return result
        else:
            print(f"\n❌ Error creating release (Status: {response.status_code})")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return None

def main():
    """Main function"""

    # Get token and repo from arguments or environment
    token = None
    repo = None

    if len(sys.argv) > 2:
        token = sys.argv[1]
        repo = sys.argv[2]
    else:
        # Try to get from environment
        token = os.environ.get("GITHUB_TOKEN")
        repo = os.environ.get("GITHUB_REPO", "Hayatelin/agent-memory-mvp")

    if not token or not repo:
        print("\n" + "="*70)
        print("  GitHub Release Creator for AgentMem v0.3.0")
        print("="*70 + "\n")
        print("Usage:")
        print("  python create_release.py <token> <repo>\n")
        print("Example:")
        print("  python create_release.py ghp_xxxxxxxxxxxx Hayatelin/agent-memory-mvp\n")
        print("Or set environment variables:")
        print("  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx")
        print("  export GITHUB_REPO=Hayatelin/agent-memory-mvp")
        print("  python create_release.py\n")
        print("="*70 + "\n")

        # Provide manual instructions
        print_manual_instructions(repo or "Hayatelin/agent-memory-mvp")
        return 1

    result = create_release(token, repo)
    return 0 if result else 1

def print_manual_instructions(repo):
    """Print manual instructions for creating release"""

    print("Manual Release Creation Instructions:")
    print("-" * 70)
    print(f"\n1. Go to: https://github.com/{repo}/releases/new")
    print(f"\n2. Fill in the release information:")
    print(f"   Tag version: v0.3.0")
    print(f"   Release title: v0.3.0 - Complete Implementation with Web UI, SDK & CLI")
    print(f"   Description: Copy content from RELEASE_NOTES_v0.3.0.md")
    print(f"\n3. Configure options:")
    print(f"   - Draft: No")
    print(f"   - Pre-release: No")
    print(f"   - Generate release notes: No")
    print(f"\n4. Click 'Publish release'")
    print(f"\n" + "="*70 + "\n")

if __name__ == "__main__":
    sys.exit(main())
