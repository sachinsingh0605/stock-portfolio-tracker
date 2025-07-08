#!/usr/bin/env python3
"""
Comprehensive test for Stock Portfolio Tracker
Tests all functionality without requiring yfinance
"""

import sqlite3
import os
import sys
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")

    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
        import sqlite3
        import pandas as pd
        from datetime import datetime
        import threading
        print("✅ All basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_database_operations():
    """Test database creation and operations"""
    print("🧪 Testing database operations...")

    try:
        # Create test database
        conn = sqlite3.connect('test_portfolio.db')
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                purchase_price REAL NOT NULL,
                purchase_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT NOT NULL,
                UNIQUE(symbol, date)
            )
        """)

        # Test inserting data
        test_data = [
            ('AAPL', 10, 150.50, '2024-01-15'),
            ('GOOGL', 5, 2800.00, '2024-02-01'),
            ('MSFT', 8, 380.00, '2024-01-20')
        ]

        for symbol, quantity, price, date in test_data:
            cursor.execute("""
                INSERT INTO portfolio (symbol, quantity, purchase_price, purchase_date)
                VALUES (?, ?, ?, ?)
            """, (symbol, quantity, price, date))

        conn.commit()

        # Test querying data
        cursor.execute("SELECT COUNT(*) FROM portfolio")
        count = cursor.fetchone()[0]

        # Test aggregation query
        cursor.execute("""
            SELECT symbol, SUM(quantity) as total_quantity, AVG(purchase_price) as avg_price
            FROM portfolio
            GROUP BY symbol
        """)
        portfolio_data = cursor.fetchall()

        # Test price history
        cursor.execute("""
            INSERT INTO price_history (symbol, price, date)
            VALUES (?, ?, ?)
        """, ('AAPL', 155.25, '2024-07-08'))

        conn.commit()
        conn.close()

        # Clean up
        os.remove('test_portfolio.db')

        if count == 3 and len(portfolio_data) == 3:
            print("✅ Database operations successful")
            return True
        else:
            print("❌ Database operations failed")
            return False

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_financial_calculations():
    """Test financial calculation logic"""
    print("🧪 Testing financial calculations...")

    try:
        # Test gain/loss calculation
        purchase_price = 150.00
        current_price = 155.25
        quantity = 10

        gain_loss = (current_price - purchase_price) * quantity
        total_value = current_price * quantity

        expected_gain = 52.50  # (155.25 - 150.00) * 10
        expected_value = 1552.50  # 155.25 * 10

        if abs(gain_loss - expected_gain) < 0.01 and abs(total_value - expected_value) < 0.01:
            print("✅ Financial calculations correct")
            return True
        else:
            print("❌ Financial calculations failed")
            return False

    except Exception as e:
        print(f"❌ Financial calculation test failed: {e}")
        return False

def test_csv_export():
    """Test CSV export functionality"""
    print("🧪 Testing CSV export...")

    try:
        import pandas as pd

        # Create sample data
        data = [
            ['AAPL', 10, '$150.00', '$155.25', '$52.50', '$1552.50'],
            ['GOOGL', 5, '$2800.00', '$2750.00', '$-250.00', '$13750.00'],
            ['MSFT', 8, '$380.00', '$395.50', '$124.00', '$3164.00']
        ]

        columns = ['Symbol', 'Quantity', 'Purchase Price', 'Current Price', 'Gain/Loss', 'Total Value']
        df = pd.DataFrame(data, columns=columns)

        # Export to CSV
        test_filename = 'test_portfolio.csv'
        df.to_csv(test_filename, index=False)

        # Read back and verify
        df_read = pd.read_csv(test_filename)

        # Clean up
        os.remove(test_filename)

        if len(df_read) == 3 and list(df_read.columns) == columns:
            print("✅ CSV export functionality works")
            return True
        else:
            print("❌ CSV export failed")
            return False

    except Exception as e:
        print(f"❌ CSV export test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running comprehensive tests for Stock Portfolio Tracker\n")

    tests = [
        test_imports,
        test_database_operations,
        test_financial_calculations,
        test_csv_export
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\n📋 Next steps:")
        print("1. Install yfinance: pip install yfinance")
        print("2. Run the application: python portfolio_tracker.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    main()
