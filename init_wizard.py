#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentMem Interactive Initialization Wizard
交互式初始化嚮導 - 首次使用時自動運行
"""

import os
import sys
import json
import uuid
import subprocess
import platform
from pathlib import Path
from typing import Dict, Optional

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print welcome header"""
    print()
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.OKBLUE}AgentMem Interactive Setup Wizard{Colors.ENDC}")
    print(f"{Colors.OKBLUE}交互式初始化嚮導{Colors.ENDC}")
    print("=" * 70)
    print()

def print_step(step_num: int, title: str):
    """Print step header"""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}[Step {step_num}]{Colors.ENDC} {title}")
    print("-" * 70)

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}[OK]{Colors.ENDC} {message}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.WARNING}[!]{Colors.ENDC} {message}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {message}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKBLUE}[i]{Colors.ENDC} {message}")

def select_language() -> str:
    """Step 1: Select language"""
    print_step(1, "Select Language / 選擇語言")

    options = {
        "1": ("English", "en"),
        "2": ("繁體中文", "zh-TW"),
    }

    for key, (lang, _) in options.items():
        print(f"  {key}. {lang}")

    while True:
        choice = input("\nEnter your choice (1-2): ").strip()
        if choice in options:
            _, lang_code = options[choice]
            print_success(f"Language selected: {options[choice][0]}")
            return lang_code
        print_error("Invalid choice. Please enter 1 or 2.")

def check_environment() -> Dict[str, bool]:
    """Step 2: Check environment"""
    print_step(2, "Checking Environment / 檢查環境")

    checks = {
        "Python": False,
        "pip": False,
        "Git": False,
    }

    # Check Python
    print_info("Checking Python version...")
    try:
        import sys as sys_module
        version = sys_module.version.split()[0]
        if sys_module.version_info >= (3, 8):
            print_success(f"Python {version} (3.8+)")
            checks["Python"] = True
        else:
            print_warning(f"Python {version} - recommend 3.8 or higher")
    except Exception as e:
        print_error(f"Failed to check Python: {e}")

    # Check pip
    print_info("Checking pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                       capture_output=True, check=True)
        print_success("pip found")
        checks["pip"] = True
    except Exception as e:
        print_error(f"Failed to check pip: {e}")

    # Check Git (optional)
    print_info("Checking Git...")
    try:
        subprocess.run(["git", "--version"],
                       capture_output=True, check=True)
        print_success("Git found")
        checks["Git"] = True
    except Exception:
        print_warning("Git not found (optional - needed for updates)")

    return checks

def select_database() -> Dict[str, str]:
    """Step 3: Select database"""
    print_step(3, "Select Database / 選擇數據庫")

    options = {
        "1": {
            "name": "SQLite (Recommended for beginners)",
            "type": "sqlite",
            "url": "sqlite:///./agentmem.db"
        },
        "2": {
            "name": "PostgreSQL (Production)",
            "type": "postgresql",
            "url": None  # Will be configured later
        },
    }

    for key, config in options.items():
        print(f"  {key}. {config['name']}")

    while True:
        choice = input("\nEnter your choice (1-2): ").strip()
        if choice in options:
            selected = options[choice]
            print_success(f"Database selected: {selected['name']}")

            if choice == "2":
                # PostgreSQL configuration
                print_info("\nPostgreSQL Configuration:")
                host = input("  Database host (default: localhost): ").strip() or "localhost"
                port = input("  Database port (default: 5432): ").strip() or "5432"
                user = input("  Database user (default: postgres): ").strip() or "postgres"
                password = input("  Database password: ").strip()
                database = input("  Database name (default: agentmem): ").strip() or "agentmem"

                url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
                selected["url"] = url

            return selected
        print_error("Invalid choice. Please enter 1 or 2.")

def setup_agent_identity() -> Dict[str, str]:
    """Step 4: Agent Identity setup"""
    print_step(4, "Agent Identity Setup / Agent 身份設置")

    print_info("Each Agent needs a unique identifier for authentication.")
    print()

    # Generate default Agent ID
    default_agent_id = str(uuid.uuid4())

    agent_name = input("Agent Name (default: 'AgentMem-User'): ").strip() or "AgentMem-User"
    print_info(f"Agent name set to: {agent_name}")
    print()

    print_info(f"Auto-generated Agent ID: {default_agent_id}")
    use_default = input("Use this ID? (y/n, default: y): ").strip().lower()

    if use_default == "n":
        agent_id = input("Enter custom Agent ID: ").strip()
        if not agent_id:
            agent_id = default_agent_id
            print_warning("Empty input, using auto-generated ID")
    else:
        agent_id = default_agent_id

    print_success(f"Agent configured: {agent_name} ({agent_id})")

    return {
        "agent_name": agent_name,
        "agent_id": agent_id,
    }

def select_startup_options() -> Dict[str, bool]:
    """Step 5: Startup options"""
    print_step(5, "Select Startup Options / 選擇啟動選項")

    print_info("Choose which interfaces you want to enable:")
    print()

    options = {
        "web_ui": "Web UI Dashboard (Streamlit)",
        "api": "REST API Server",
        "cli": "Command-line Interface",
    }

    selected = {}

    for key, description in options.items():
        response = input(f"Enable {description}? (y/n, default: y): ").strip().lower()
        selected[key] = response != "n"

    print()
    enabled = [desc for key, desc in options.items() if selected[key]]
    for item in enabled:
        print_success(f"Enabled: {item}")

    return selected

def create_config(database: Dict, agent: Dict, startup: Dict) -> Dict:
    """Create configuration dictionary"""
    config = {
        "agent_name": agent["agent_name"],
        "agent_id": agent["agent_id"],
        "api_url": "http://localhost:8000",
        "api_port": 8000,
        "database": {
            "type": database["type"],
            "url": database["url"],
        },
        "startup": {
            "enable_web_ui": startup["web_ui"],
            "enable_api": startup["api"],
            "enable_cli": startup["cli"],
        },
        "ui": {
            "streamlit_port": 8501,
            "theme": "light",
        },
        "features": {
            "embedding_service": "local",  # or "openai"
            "semantic_search": True,
            "collaboration": True,
        }
    }
    return config

def save_config(config: Dict) -> bool:
    """Save configuration to file"""
    try:
        # Create config directory
        config_dir = Path.home() / ".agentmem"
        config_dir.mkdir(exist_ok=True)

        # Save config file
        config_file = config_dir / "config.json"
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        print_success(f"Configuration saved to: {config_file}")
        return True
    except Exception as e:
        print_error(f"Failed to save configuration: {e}")
        return False

def save_env_file(database: Dict) -> bool:
    """Create .env file for environment variables"""
    try:
        env_content = f"""# AgentMem Environment Configuration
# Generated by init_wizard.py

# Database Configuration
DATABASE_TYPE={database['type']}
DATABASE_URL={database['url']}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Embedding Service (local or openai)
EMBEDDING_SERVICE=local

# Optional: OpenAI API Key (if using OpenAI embeddings)
# OPENAI_API_KEY=sk-...

# Optional: Redis URL
# REDIS_URL=redis://localhost:6379

# Debug Mode
DEBUG=false
"""

        with open(".env", "w") as f:
            f.write(env_content)

        print_success("Environment file (.env) created")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False

def show_summary(config: Dict, language: str):
    """Show configuration summary"""
    print()
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.OKGREEN}Configuration Summary{Colors.ENDC}")
    print("=" * 70)
    print()

    print(f"Agent Name:          {config['agent_name']}")
    print(f"Agent ID:            {config['agent_id']}")
    print(f"API URL:             {config['api_url']}:{config['api_port']}")
    print(f"Database Type:       {config['database']['type']}")

    if config['database']['type'] == 'sqlite':
        print(f"Database URL:        {config['database']['url']}")
    else:
        print(f"Database URL:        [PostgreSQL configured]")

    print()
    print("Enabled Services:")
    if config['startup']['enable_api']:
        print(f"  - REST API Server (http://localhost:8000)")
    if config['startup']['enable_web_ui']:
        print(f"  - Web UI Dashboard (http://localhost:8501)")
    if config['startup']['enable_cli']:
        print(f"  - Command-line Interface")

    print()

def show_next_steps(config: Dict):
    """Show next steps"""
    print()
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.OKGREEN}Next Steps{Colors.ENDC}")
    print("=" * 70)
    print()

    print("1. Start the backend server:")
    print("   python -m src.main")
    print()

    if config['startup']['enable_web_ui']:
        print("2. In another terminal, start the Web UI:")
        print("   streamlit run ui/app.py")
        print()
        print("   Then open: http://localhost:8501")
        print()

    if config['startup']['enable_cli']:
        print("3. Try the CLI tool:")
        print("   python -m src.cli.main init")
        print("   python -m src.cli.main --help")
        print()

    print("4. Explore the documentation:")
    print("   - Quick Start: docs/QUICKSTART.md")
    print("   - Usage Guide: docs/USAGE_GUIDE.md")
    print("   - API Reference: docs/API_REFERENCE.md")
    print()

    print("5. Get help:")
    print("   - GitHub Issues: https://github.com/Hayatelin/agent-memory-mvp/issues")
    print("   - Documentation: https://github.com/Hayatelin/agent-memory-mvp#readme")
    print()

def main():
    """Main function"""
    try:
        print_header()

        # Step 1: Select language
        language = select_language()

        # Step 2: Check environment
        env_check = check_environment()

        # Step 3: Select database
        database = select_database()

        # Step 4: Agent identity
        agent = setup_agent_identity()

        # Step 5: Startup options
        startup = select_startup_options()

        # Create configuration
        config = create_config(database, agent, startup)

        # Show summary
        show_summary(config, language)

        # Confirm and save
        confirm = input("Proceed with this configuration? (y/n): ").strip().lower()
        if confirm != "y":
            print_warning("Setup cancelled.")
            return

        # Save configuration
        if save_config(config):
            save_env_file(database)
            print_success("Setup wizard completed successfully!")
            print()
            show_next_steps(config)
            print(f"{Colors.BOLD}{Colors.OKGREEN}Happy coding! 🚀{Colors.ENDC}")
            print()
        else:
            print_error("Failed to save configuration.")

    except KeyboardInterrupt:
        print()
        print_warning("Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
