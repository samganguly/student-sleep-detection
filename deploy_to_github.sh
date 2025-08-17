#!/bin/bash
# GitHub Deployment Script for Student Sleep Detection System
# Run this script to initialize git repository and prepare for GitHub upload

echo "🛌 Student Sleep Detection System - GitHub Deployment"
echo "========================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first:"
    echo "   Download from: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "🔄 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "🔄 Adding files to Git..."
git add .

# Create initial commit
echo "🔄 Creating initial commit..."
git commit -m "Initial commit: Student Sleep Detection System

Features:
- AI-powered drowsiness detection using CNN
- Eye absence detection for inattention monitoring
- Real-time webcam monitoring with OpenCV
- Interactive UI with pause/resume functionality
- Dual alert system (audio + visual)
- Multiple detection algorithms
- Comprehensive documentation

Technologies: Python, TensorFlow, OpenCV, Pygame"

echo "✅ Initial commit created"

echo ""
echo "🎉 Repository is ready for GitHub!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://github.com and create a new repository"
echo "2. Name it 'student-sleep-detection' (or your preferred name)"
echo "3. Do NOT initialize with README (we already have one)"
echo "4. Copy the repository URL"
echo "5. Run these commands:"
echo ""
echo "   git remote add origin <YOUR_REPO_URL>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Example:"
echo "   git remote add origin https://github.com/yourusername/student-sleep-detection.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "💡 Replace <YOUR_REPO_URL> with your actual GitHub repository URL"
echo ""
echo "🌟 Don't forget to add a star ⭐ to your own repo!"
