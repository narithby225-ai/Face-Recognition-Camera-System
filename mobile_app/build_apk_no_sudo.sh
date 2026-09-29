#!/bin/bash
# Face Recognition Camera System - APK Build Script (No Sudo Required)
# This script builds APK without system-wide installations

set -e  # Exit on error

echo "=========================================="
echo "  Face Recognition APK Builder"
echo "  (User-space installation)"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "buildozer.spec" ]; then
    echo -e "${RED}Error: buildozer.spec not found!${NC}"
    echo "Please run this script from the mobile_app directory"
    exit 1
fi

echo -e "${BLUE}Working directory: $(pwd)${NC}"
echo ""

# Step 1: Install pip packages locally
echo -e "${BLUE}Step 1: Installing Python packages (user space)...${NC}"
python3 -m pip install --user --upgrade pip
python3 -m pip install --user cython==0.29.36
python3 -m pip install --user buildozer==1.5.0

# Add local bin to PATH
export PATH=$PATH:~/.local/bin

# Step 2: Check installation
echo -e "${BLUE}Step 2: Verifying installation...${NC}"
python3 --version
buildozer --version || echo -e "${YELLOW}Buildozer not found in PATH, trying direct path...${NC}"

# Try direct path to buildozer
BUILDOZER_PATH=~/.local/bin/buildozer
if [ -f "$BUILDOZER_PATH" ]; then
    echo -e "${GREEN}Found buildozer at: $BUILDOZER_PATH${NC}"
    BUILDOZER_CMD="$BUILDOZER_PATH"
else
    BUILDOZER_CMD="buildozer"
fi

# Step 3: Build APK
echo -e "${BLUE}Step 3: Building APK...${NC}"
echo -e "${YELLOW}This will take 20-30 minutes for first build...${NC}"
echo -e "${YELLOW}Buildozer will download Android SDK and NDK automatically${NC}"
echo ""

# Build debug APK
echo -e "${GREEN}Starting APK build...${NC}"
$BUILDOZER_CMD -v android debug

# Step 4: Show result
echo ""
echo "=========================================="
echo -e "${GREEN}✅ APK BUILD COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "Your APK is located at:"
ls -lh bin/*.apk 2>/dev/null && echo "" || echo -e "${YELLOW}APK will appear after build completes${NC}"
echo ""
echo "To copy to Windows D: drive:"
echo "  cp bin/*.apk /mnt/d/face_recognition_app.apk"
echo ""
echo "=========================================="
