# GitHub Deployment Script for Student Sleep Detection SysteWrite-Host "   git remote add origin YOUR_REPO_URL" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Example:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/yourusername/student-sleep-detection.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Replace YOUR_REPO_URL with your actual GitHub repository URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌟 Don't forget to add a star ⭐ to your own repo!" -ForegroundColor Magenta

# Pause to let user read the instructions
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')hell)
# Run this script to initialize git repository and prepare for GitHub upload

Write-Host "🛌 Student Sleep Detection System - GitHub Deployment" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "✅ Git is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first:" -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Initialize git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "🔄 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Add all files
Write-Host "🔄 Adding files to Git..." -ForegroundColor Yellow
git add .

# Create initial commit
Write-Host "🔄 Creating initial commit..." -ForegroundColor Yellow
$commitMessage = @"
Initial commit: Student Sleep Detection System

Features:
- AI-powered drowsiness detection using CNN
- Eye absence detection for inattention monitoring
- Real-time webcam monitoring with OpenCV
- Interactive UI with pause/resume functionality
- Dual alert system (audio + visual)
- Multiple detection algorithms
- Comprehensive documentation

Technologies: Python, TensorFlow, OpenCV, Pygame
"@

git commit -m $commitMessage

Write-Host "✅ Initial commit created" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Repository is ready for GitHub!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor White
Write-Host "1. Go to https://github.com and create a new repository" -ForegroundColor White
Write-Host "2. Name it 'student-sleep-detection' (or your preferred name)" -ForegroundColor White
Write-Host "3. Do NOT initialize with README (we already have one)" -ForegroundColor White
Write-Host "4. Copy the repository URL" -ForegroundColor White
Write-Host "5. Run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin <YOUR_REPO_URL>" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Example:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/samganguly/student-sleep-detection.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Replace <YOUR_REPO_URL> with your actual GitHub repository URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌟 Don't forget to add a star ⭐ to your own repo!" -ForegroundColor Magenta

# Pause to let user read the instructions
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
