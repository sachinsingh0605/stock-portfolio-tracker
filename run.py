#!/usr/bin/env python3
"""
Simple launcher for the Stock Portfolio Tracker
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    missing_packages = []

    try:
        import yfinance
    except ImportError:
        missing_packages.append('yfinance')

    try:
        import pandas
    except ImportError:
        missing_packages.append('pandas')

    try:
        import tkinter
    except ImportError:
        missing_packages.append('tkinter (usually comes with Python)')

    if missing_packages:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False

    return True

def main():
    print("🚀 Starting Stock Portfolio Tracker...")
    print("=" * 50)

    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies first.")
        sys.exit(1)

    print("✅ All dependencies found")
    print("📊 Loading portfolio tracker...")

    # Run the main application
    try:
        import portfolio_tracker
        portfolio_tracker.main()
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Make sure all files are in the same directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
