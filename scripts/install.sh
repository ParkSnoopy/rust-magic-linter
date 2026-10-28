#!/bin/bash
# ============================================
# RUST-MAGIC-LINTER INSTALLER
# ============================================
# Usage: ./install.sh [preset]
#   preset: minimal, standard (default), or maximum
#
# This script will:
# 1. Add lint configuration to Cargo.toml
# 2. Create the selected profile's clippy.toml for complexity thresholds
# 3. Optionally create .cargo/deny.toml

set -e

PRESET="${1:-standard}"
REPO_URL="https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a Rust project
if [ ! -f "Cargo.toml" ]; then
    echo_error "No Cargo.toml found. Please run this script from a Rust project root."
    exit 1
fi

# Validate preset
case "$PRESET" in
    minimal|standard|maximum)
        echo_info "Using preset: $PRESET"
        ;;
    *)
        echo_error "Invalid preset: $PRESET"
        echo "Valid presets: minimal, standard, maximum"
        exit 1
        ;;
esac
PROFILE_URL="$REPO_URL/skills/rust-magic-linter/assets/$PRESET"

# Check if lints already exist
if grep -Eq '^[[:space:]]*\[[[:space:]]*(workspace[[:space:]]*\.[[:space:]]*)?lints[[:space:]]*(\.|\])' Cargo.toml; then
    echo_error "Lint configuration already exists in Cargo.toml. Merge the selected profile manually."
    exit 1
fi

# Determine if this is a workspace
IS_WORKSPACE=false
if grep -Eq '^[[:space:]]*\[[[:space:]]*workspace[[:space:]]*\]' Cargo.toml; then
    IS_WORKSPACE=true
    echo_info "Detected workspace project"
fi

# Download the preset
echo_info "Downloading $PRESET preset..."
PRESET_CONTENT=$(curl -fsSL "$PROFILE_URL/lint.toml")

if [ "$PRESET_CONTENT" = "" ]; then
    echo_error "Failed to download preset. Check your internet connection."
    exit 1
fi

# Download required companion settings before modifying the manifest.
if [ ! -f "clippy.toml" ] && [ ! -f ".clippy.toml" ]; then
    CLIPPY_CONTENT=$(curl -fsSL "$PROFILE_URL/clippy.toml")
    if [ "$CLIPPY_CONTENT" = "" ]; then
        echo_error "Failed to download clippy.toml."
        exit 1
    fi
fi

# For workspaces, convert [lints.*] to [workspace.lints.*]
if [ "$IS_WORKSPACE" = true ]; then
    PRESET_CONTENT=$(echo "$PRESET_CONTENT" | sed 's/\[lints\./[workspace.lints./g')
fi

# Append to Cargo.toml
echo "" >> Cargo.toml
echo "# ============================================" >> Cargo.toml
echo "# RUST-MAGIC-LINTER ($PRESET preset)" >> Cargo.toml
echo "# https://github.com/ParkSnoopy/rust-magic-linter" >> Cargo.toml
echo "# ============================================" >> Cargo.toml
echo "$PRESET_CONTENT" >> Cargo.toml

echo_info "Added lint configuration to Cargo.toml"

# Create clippy.toml if it doesn't exist
if [ ! -f "clippy.toml" ] && [ ! -f ".clippy.toml" ]; then
    echo_info "Creating clippy.toml..."
    printf '%s\n' "$CLIPPY_CONTENT" > clippy.toml
    echo_info "Created clippy.toml"
else
    echo_warn "clippy.toml or .clippy.toml already exists, skipping"
fi

# Ask about deny.toml
if read -r -p "Create .cargo/deny.toml for supply chain security? (y/N) " REPLY && [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p .cargo
    curl -fsSL "$REPO_URL/skills/rust-magic-linter/assets/deny.toml" -o .cargo/deny.toml
    echo_info "Created .cargo/deny.toml"
    echo_info "Run 'cargo deny check' to verify dependencies (requires cargo-deny)"
fi

# Ask about CONSTITUTION.md
if read -r -p "Create CONSTITUTION.md template? (y/N) " REPLY && [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -f "CONSTITUTION.md" ]; then
        curl -fsSL "$PROFILE_URL/CONSTITUTION.md" -o CONSTITUTION.md
        echo_info "Created CONSTITUTION.md - customize it for your project!"
    else
        echo_warn "CONSTITUTION.md already exists, skipping"
    fi
fi

echo ""
echo_info "Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Run 'cargo clippy' to see any new warnings/errors"
echo "  2. Fix issues or adjust relaxations in Cargo.toml"
echo "  3. Customize clippy.toml thresholds for your project"
if [ "$IS_WORKSPACE" = true ]; then
    echo "  Add [lints] with workspace = true to each member package that should inherit workspace lints"
    if grep -q "\[package\]" Cargo.toml; then
        echo "  The root package also needs [lints] with workspace = true"
    fi
fi
if [ -f "CONSTITUTION.md" ]; then
    echo "  4. Edit CONSTITUTION.md with your project's specific rules"
fi
echo ""
echo "Documentation: https://github.com/ParkSnoopy/rust-magic-linter"
