#!/bin/bash

################################################################################
# AgentMem Installation Setup Script (macOS/Linux)
# 一鍵安裝和配置 AgentMem
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          AgentMem - Quick Setup Script                     ║${NC}"
    echo -e "${BLUE}║     🚀 Automated Installation & Configuration              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check system requirements
check_requirements() {
    print_step "Checking system requirements..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"

    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git not found. Please install Git."
        exit 1
    fi

    GIT_VERSION=$(git --version | cut -d' ' -f3)
    print_success "Git $GIT_VERSION found"

    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 not found. Please ensure pip is installed with Python."
        exit 1
    fi

    print_success "pip3 found"
    echo ""
}

# Clone repository
clone_repository() {
    print_step "Cloning AgentMem repository..."

    if [ -d "agent-memory-mvp" ]; then
        print_warning "Directory 'agent-memory-mvp' already exists."
        read -p "Do you want to overwrite it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf agent-memory-mvp
        else
            print_info "Using existing directory."
            return
        fi
    fi

    git clone https://github.com/Hayatelin/agent-memory-mvp.git
    print_success "Repository cloned successfully"
    echo ""
}

# Install dependencies
install_dependencies() {
    print_step "Installing Python dependencies..."

    cd agent-memory-mvp

    # Upgrade pip
    print_info "Upgrading pip..."
    python3 -m pip install --upgrade pip

    # Install requirements
    if [ -f "requirements.txt" ]; then
        python3 -m pip install -r requirements.txt
        print_success "All dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi

    echo ""
}

# Run initialization wizard
run_init_wizard() {
    print_step "Starting initialization wizard..."
    echo ""

    if [ -f "init_wizard.py" ]; then
        python3 init_wizard.py
    else
        print_warning "init_wizard.py not found. Running manual setup..."
        manual_setup
    fi

    echo ""
}

# Manual setup (fallback)
manual_setup() {
    print_info "Setting up configuration manually..."

    # Create config directory if not exists
    mkdir -p ~/.agentmem

    # Generate or use default Agent ID
    if [ ! -f ~/.agentmem/config.json ]; then
        print_info "Generating default Agent ID..."
        AGENT_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

        cat > ~/.agentmem/config.json <<EOF
{
    "agent_id": "$AGENT_ID",
    "api_url": "http://localhost:8000",
    "database_type": "sqlite",
    "database_url": "sqlite:///./agentmem.db"
}
EOF

        print_success "Configuration file created at ~/.agentmem/config.json"
        print_info "Agent ID: $AGENT_ID"
    else
        print_info "Configuration file already exists"
    fi
}

# Display next steps
show_next_steps() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║            ✓ Installation Complete!                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    print_info "Next steps to get started:"
    echo ""
    echo -e "${YELLOW}1. Start the backend server:${NC}"
    echo "   cd agent-memory-mvp"
    echo "   python -m src.main"
    echo ""
    echo -e "${YELLOW}2. In a new terminal, start the Web UI:${NC}"
    echo "   cd agent-memory-mvp"
    echo "   streamlit run ui/app.py"
    echo ""
    echo -e "${YELLOW}3. Access the application:${NC}"
    echo "   • Web UI: http://localhost:8501"
    echo "   • API: http://localhost:8000"
    echo "   • API Docs: http://localhost:8000/docs"
    echo ""

    print_info "Alternative ways to use AgentMem:"
    echo ""
    echo -e "${BLUE}• Python SDK:${NC}"
    echo "  python3 -c \"from src.client import AgentMemClient; client = AgentMemClient()\""
    echo ""
    echo -e "${BLUE}• Command Line Interface:${NC}"
    echo "  python -m src.cli.main --help"
    echo ""

    print_info "Useful documentation:"
    echo "  • Quick Start: docs/QUICKSTART.md"
    echo "  • Usage Guide: docs/USAGE_GUIDE.md"
    echo "  • API Reference: docs/API_REFERENCE.md"
    echo "  • Examples: docs/EXAMPLES.md"
    echo ""

    print_info "Need help?"
    echo "  • GitHub Issues: https://github.com/Hayatelin/agent-memory-mvp/issues"
    echo "  • Documentation: https://github.com/Hayatelin/agent-memory-mvp#readme"
    echo ""

    echo -e "${GREEN}Happy coding! 🚀${NC}"
    echo ""
}

# Main execution
main() {
    print_header

    check_requirements
    clone_repository
    install_dependencies
    run_init_wizard
    show_next_steps
}

# Run main function
main
