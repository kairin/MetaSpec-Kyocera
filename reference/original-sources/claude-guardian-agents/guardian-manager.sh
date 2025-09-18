#!/bin/bash
# Guardian Agents Manager Script
# Manages installation, updates, and uninstallation of Guardian Agents

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

REPO_URL="https://github.com/kairin/claude-guardian-agents"
INSTALL_DIR=".guardian"
CLAUDE_AGENTS_DIR=".claude/agents"
LOCAL_GENERATE_MANIFEST_SCRIPT="scripts/generate-manifest.py"

# --- Helper Functions ---

check_git_repo() {
    if [ ! -d ".git" ]; then
        echo -e "${RED}❌ Error: Must be run from a git repository root${NC}"
        exit 1
    fi
}

copy_generate_manifest_script() {
    if [ -f "$LOCAL_GENERATE_MANIFEST_SCRIPT" ]; then
        cp "$LOCAL_GENERATE_MANIFEST_SCRIPT" "$INSTALL_DIR/scripts/generate-manifest.py"
        echo -e "${GREEN}✅ Copied local generate-manifest.py to .guardian/scripts/${NC}"
    else
        echo -e "${YELLOW}⚠️ Warning: Local generate-manifest.py not found. Using cloned version.${NC}"
    fi
}

generate_manifest_and_symlinks() {
    echo -e "${BLUE}🔗 Setting up Claude Code integration...${NC}"
    mkdir -p "$CLAUDE_AGENTS_DIR"

    echo -e "${BLUE}🔧 Generating complete manifest...${NC}"
    cd "$INSTALL_DIR"
    python3 scripts/generate-manifest.py --claude-index "../$CLAUDE_AGENTS_DIR/agent-index.json"
    cd ..

    echo -e "${BLUE}🔗 Creating agent category links...${NC}"
    cd "$CLAUDE_AGENTS_DIR"
    ln -sf "../../$INSTALL_DIR/1-product"/* . 2>/dev/null || true
    ln -sf "../../$INSTALL_DIR/2-engineering"/* . 2>/dev/null || true
    ln -sf "../../$INSTALL_DIR/3-operations"/* . 2>/dev/null || true
    ln -sf "../../$INSTALL_DIR/4-thinktank"/* . 2>/dev/null || true
    ln -sf "../../$INSTALL_DIR/5-meta-agents"/* . 2>/dev/null || true # Added meta-agents symlink
    cd ../..
}

setup_gitignore() {
    echo -e "${BLUE}📋 Updating .gitignore...${NC}"
    if [ -f ".gitignore" ]; then
        if ! grep -q "^\.guardian/$" ".gitignore"; then
            echo "" >> .gitignore
            echo "# Guardian Agents (managed separately)" >> .gitignore
            echo ".guardian/" >> .gitignore
        fi
    else
        echo "# Guardian Agents (managed separately)" > .gitignore
        echo ".guardian/" >> .gitignore
    fi

    if grep -q "^\.claude/$" ".gitignore"; then
        sed -i '/^\.claude\/$/d' .gitignore
    fi
}

install_agents() {
    check_git_repo
    echo -e "${BLUE}🛡️  Guardian Agents Installation${NC}"
    echo "Installing into: $(pwd)/$INSTALL_DIR"
    echo ""

    echo -e "${BLUE}📁 Creating Guardian Agents directory...${NC}"
    mkdir -p "$INSTALL_DIR"

    echo -e "${BLUE}📥 Downloading Guardian Agents...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
    copy_generate_manifest_script # Copy after clone

    generate_manifest_and_symlinks
    setup_gitignore

    echo ""
    echo -e "${GREEN}✅ Guardian Agents installation complete!${NC}"
    echo ""
    echo "📋 What was installed:"
    echo "  • $INSTALL_DIR/           - Complete Guardian Agents system"
    echo "  • $CLAUDE_AGENTS_DIR/      - Claude Code integration"
    echo ""
    echo "🚀 Usage:"
    echo "  • Agents are now available in Claude Code"
    echo "  • Run this script (./guardian-manager.sh) to manage updates or uninstallation"
    echo "  • The $INSTALL_DIR/ directory is git-ignored (managed separately)"
    echo ""
}

update_agents() {
    check_git_repo
    if [ ! -d "$INSTALL_DIR" ]; then
        echo -e "${RED}❌ Guardian Agents not installed. Please run install first.${NC}"
        return 1
    fi

    echo -e "${YELLOW}🔄 Updating existing Guardian Agents...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
    cd ..
    copy_generate_manifest_script # Copy after pull

    generate_manifest_and_symlinks

    echo -e "${GREEN}✅ Guardian Agents updated to latest version!${NC}"
}

uninstall_agents() {
    echo -e "${RED}🗑️ Uninstalling Guardian Agents...${NC}"
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
        echo -e "${GREEN}✅ Removed $INSTALL_DIR/${NC}"
    else
        echo -e "${YELLOW}⚠️ $INSTALL_DIR/ not found, skipping removal.${NC}"
    fi

    if [ -d "$CLAUDE_AGENTS_DIR" ]; then
        rm -rf "$CLAUDE_AGENTS_DIR"
        echo -e "${GREEN}✅ Removed $CLAUDE_AGENTS_DIR/${NC}"
    else
        echo -e "${YELLOW}⚠️ $CLAUDE_AGENTS_DIR/ not found, skipping removal.${NC}"
    fi

    # Remove .guardian/ line from .gitignore if it exists
    if [ -f ".gitignore" ]; then
        sed -i '/^\.guardian\/$/d' .gitignore
        sed -i '/^# Guardian Agents (managed separately)$/d' .gitignore
        echo -e "${GREEN}✅ Cleaned .gitignore${NC}"
    fi

    echo -e "${GREEN}✅ Guardian Agents uninstallation complete!${NC}"
}

# --- TUI Functions ---

display_menu() {
    clear
    echo -e "${BLUE}=== Guardian Agents Manager ===${NC}"
    echo -e "1. ${GREEN}Install Guardian Agents${NC}"
    echo -e "2. ${YELLOW}Update Guardian Agents${NC}"
    echo -e "3. ${RED}Uninstall Guardian Agents${NC}"
    echo -e "4. Exit"
    echo -e "-------------------------------"
    echo -n "Enter your choice: "
}

handle_choice() {
    case $1 in
        1) install_agents ;;
        2) update_agents ;;
        3) uninstall_agents ;;
        4) exit 0 ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
}

# --- Main Logic ---

# If no arguments, display TUI
if [ $# -eq 0 ]; then
    while true; do
        display_menu
        read -r choice
        handle_choice "$choice"
    done
else # Handle direct commands (e.g., ./guardian-manager.sh install)
    case $1 in
        install) install_agents ;;
        update) update_agents ;;
        uninstall) uninstall_agents ;;
        *) echo -e "${RED}Invalid command. Use install, update, uninstall, or run without arguments for menu.${NC}" ; exit 1 ;;
    esac
fi
