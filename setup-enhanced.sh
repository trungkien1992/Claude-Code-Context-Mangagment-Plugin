#!/bin/bash

# Enhanced Claude AI Development Workflow Engine - Setup Script
# One-command installation for revolutionary EAEPT methodology

set -e

# Colors for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC} 🚀 ${CYAN}${BOLD}Enhanced Claude AI Development Workflow Engine${NC}      ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                    ${YELLOW}Setup & Installation${NC}                   ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() { echo -e "${BLUE}[SETUP]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_innovation() { echo -e "${PURPLE}[INNOVATION]${NC} $1"; }

check_requirements() {
    print_step "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        echo "Please install Python 3.8+ and try again"
        exit 1
    fi
    
    # Check Claude Code CLI
    if ! command -v claude-code &> /dev/null; then
        print_warning "Claude Code CLI not found in PATH"
        echo "Please install Claude Code CLI for full integration"
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed"
        exit 1
    fi
    
    print_success "System requirements met"
}

install_dependencies() {
    print_step "Installing Python dependencies..."
    
    # Install required packages
    pip3 install -q pyyaml requests asyncio dataclasses
    
    print_success "Dependencies installed"
}

setup_directories() {
    print_step "Setting up directory structure..."
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Ensure directories exist
    mkdir -p "$SCRIPT_DIR/workflow"
    mkdir -p "$SCRIPT_DIR/config"
    mkdir -p "$SCRIPT_DIR/logs"
    mkdir -p "$SCRIPT_DIR/sessions"
    
    # Make CLI executable
    chmod +x "$SCRIPT_DIR/eaept"
    
    print_success "Directory structure created"
}

configure_claude_integration() {
    print_step "Configuring Claude Code integration..."
    
    CLAUDE_DIR="$HOME/.claude"
    CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
    
    # Create .claude directory if it doesn't exist
    mkdir -p "$CLAUDE_DIR"
    
    # Add enhanced workflow configuration to CLAUDE.md
    if [ -f "$CLAUDE_MD" ]; then
        # Check if already configured
        if ! grep -q "Enhanced EAEPT Workflow" "$CLAUDE_MD"; then
            echo "" >> "$CLAUDE_MD"
            echo "# 🚀 Enhanced EAEPT Workflow Engine Integration" >> "$CLAUDE_MD"
            echo "" >> "$CLAUDE_MD"
            echo "## Revolutionary Development Methodology" >> "$CLAUDE_MD"
            echo "- **ALWAYS use Enhanced EAEPT workflow** for complex development tasks" >> "$CLAUDE_MD"
            echo "- **Auto-orchestration enabled** for seamless context management" >> "$CLAUDE_MD"
            echo "- **Phase-specific optimization** for each development stage" >> "$CLAUDE_MD"
            echo "- **RAG integration** for intelligent research and discovery" >> "$CLAUDE_MD"
            echo "" >> "$CLAUDE_MD"
            echo "## Usage Commands" >> "$CLAUDE_MD"
            echo "\`\`\`bash" >> "$CLAUDE_MD"
            echo "# Start enhanced workflow" >> "$CLAUDE_MD"
            echo "./eaept start \"Implement feature name\"" >> "$CLAUDE_MD"
            echo "" >> "$CLAUDE_MD"
            echo "# Quick templates" >> "$CLAUDE_MD"
            echo "./eaept quick" >> "$CLAUDE_MD"
            echo "" >> "$CLAUDE_MD"
            echo "# Continue workflow" >> "$CLAUDE_MD"
            echo "./eaept continue" >> "$CLAUDE_MD"
            echo "\`\`\`" >> "$CLAUDE_MD"
            echo "" >> "$CLAUDE_MD"
            echo "## EAEPT Methodology" >> "$CLAUDE_MD"
            echo "- **Express**: Deep analysis and task framing" >> "$CLAUDE_MD"
            echo "- **Ask**: Interactive clarification and validation" >> "$CLAUDE_MD"
            echo "- **Explore**: RAG-powered research and discovery" >> "$CLAUDE_MD"
            echo "- **Plan**: Detailed implementation planning" >> "$CLAUDE_MD"
            echo "- **Code**: Auto-monitored development with optimization" >> "$CLAUDE_MD"
            echo "- **Test**: Comprehensive validation and quality assurance" >> "$CLAUDE_MD"
            echo "" >> "$CLAUDE_MD"
            
            print_success "Enhanced EAEPT configuration added to CLAUDE.md"
        else
            print_warning "Enhanced EAEPT already configured in CLAUDE.md"
        fi
    else
        # Create new CLAUDE.md with enhanced configuration
        cat > "$CLAUDE_MD" << 'EOF'
# 🚀 Enhanced EAEPT Workflow Engine Integration

## Revolutionary Development Methodology
- **ALWAYS use Enhanced EAEPT workflow** for complex development tasks
- **Auto-orchestration enabled** for seamless context management  
- **Phase-specific optimization** for each development stage
- **RAG integration** for intelligent research and discovery

## Usage Commands
```bash
# Start enhanced workflow
./eaept start "Implement feature name"

# Quick templates
./eaept quick

# Continue workflow
./eaept continue
```

## EAEPT Methodology
- **Express**: Deep analysis and task framing
- **Ask**: Interactive clarification and validation
- **Explore**: RAG-powered research and discovery
- **Plan**: Detailed implementation planning
- **Code**: Auto-monitored development with optimization
- **Test**: Comprehensive validation and quality assurance
EOF
        print_success "Created CLAUDE.md with Enhanced EAEPT configuration"
    fi
}

create_symlinks() {
    print_step "Creating convenient symlinks..."
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Create symlink in /usr/local/bin for global access (if writable)
    if [ -w "/usr/local/bin" ]; then
        ln -sf "$SCRIPT_DIR/eaept" "/usr/local/bin/eaept"
        print_success "Global 'eaept' command available"
    else
        print_warning "Cannot create global symlink (no write permission to /usr/local/bin)"
        echo "You can run the workflow using: $SCRIPT_DIR/eaept"
    fi
}

run_demo() {
    print_step "Running demonstration..."
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    echo ""
    echo -e "${CYAN}🎮 Demo: Enhanced EAEPT Workflow Engine${NC}"
    echo ""
    
    # Show the help to demonstrate functionality
    "$SCRIPT_DIR/eaept" help
    
    echo ""
    print_innovation "Setup complete! Try: './eaept quick' for templates"
}

main() {
    print_header
    print_innovation "Installing Enhanced Claude AI Development Workflow Engine"
    echo ""
    
    check_requirements
    echo ""
    
    install_dependencies
    echo ""
    
    setup_directories
    echo ""
    
    configure_claude_integration
    echo ""
    
    create_symlinks
    echo ""
    
    run_demo
    
    echo ""
    echo -e "${GREEN}${BOLD}🎉 Installation Complete!${NC}"
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo "1. Try: ${YELLOW}./eaept quick${NC} - Choose from development templates"
    echo "2. Try: ${YELLOW}./eaept start \"Your task description\"${NC} - Start full workflow"
    echo "3. Try: ${YELLOW}./eaept help${NC} - See all available commands"
    echo ""
    echo -e "${PURPLE}Welcome to the future of AI-powered development! 🚀${NC}"
}

main "$@"