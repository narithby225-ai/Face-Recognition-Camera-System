#!/bin/bash
# Face Recognition Camera System - APK Build Script
# This script sets up everything and builds the Android APK

set -e  # Exit on error

echo "=========================================="
echo "  Face Recognition APK Builder"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Update system
echo -e "${BLUE}Step 1: Updating system packages...${NC}"
sudo apt update
sudo apt upgrade -y

# Step 2: Install Python and build tools
echo -e "${BLUE}Step 2: Installing Python and build tools...${NC}"
sudo apt install -y python3 python3-pip git zip unzip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y cmake libopenblas-dev liblapack-dev libblas-dev
sudo apt install -y autoconf automake libtool pkg-config
sudo apt install -y zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5

# Step 3: Install Java (required for Android)
echo -e "${BLUE}Step 3: Installing Java Development Kit...${NC}"
sudo apt install -y openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> ~/.bashrc

# Step 4: Install Cython and Buildozer
echo -e "${BLUE}Step 4: Installing Cython and Buildozer...${NC}"
pip3 install --upgrade pip
pip3 install --user cython==0.29.36
pip3 install --user buildozer==1.5.0
pip3 install --user wheel setuptools

# Add local bin to PATH
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc

# Step 5: Check installation
echo -e "${BLUE}Step 5: Verifying installation...${NC}"
python3 --version
pip3 --version
java -version
buildozer --version

# Step 6: Build APK
echo -e "${BLUE}Step 6: Building APK (this will take 20-30 minutes first time)...${NC}"
echo -e "${YELLOW}Buildozer will download Android SDK and NDK automatically${NC}"
echo ""

# Initialize buildozer (first time only)
if [ ! -d ".buildozer" ]; then
    echo -e "${GREEN}Initializing buildozer...${NC}"
    buildozer init
fi

# Clean previous builds (optional)
# buildozer android clean

# Build debug APK
echo -e "${GREEN}Starting APK build...${NC}"
buildozer android debug

# Step 7: Show result
echo ""
echo "=========================================="
echo -e "${GREEN}✅ APK BUILD COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "Your APK is located at:"
echo "  $(pwd)/bin/*.apk"
echo ""
ls -lh bin/*.apk 2>/dev/null || echo "APK file will appear here after build completes"
echo ""
echo "To transfer to Windows:"
echo "  cp bin/*.apk /mnt/d/face_recognition.apk"
echo ""
echo "To install on phone (USB connected):"
echo "  adb install bin/*.apk"
echo ""
echo "=========================================="
