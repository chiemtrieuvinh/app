#!/usr/bin/env python3
import subprocess
import sys
import os

def run_tests():
    """Run pytest with coverage reporting"""
    
    # Install test dependencies
    print("Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "test_requirements.txt"], check=True)
    
    # Run tests with coverage
    print("Running tests with coverage...")
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
        "-v"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("passed")
    else:
        print("failed")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()