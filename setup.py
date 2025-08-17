#!/usr/bin/env python3
"""
Setup script for Student Sleep Detection System
Run this script to install all dependencies and test the system
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Output: {e.output}")
        return False

def main():
    print("🛌 Student Sleep Detection System - Setup Script")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("💡 Tip: Try 'pip3 install -r requirements.txt' if the above failed")
        return
    
    # Test the system
    if not run_command("python test_system.py", "Testing system components"):
        print("💡 Some components may not be working properly")
    
    print("\n🎉 Setup completed!")
    print("\n🚀 To start the sleep detection system, run:")
    print("   python enhanced_sleep_detection_with_absence.py")
    print("\n📚 For more options, check the README.md file")

if __name__ == "__main__":
    main()
