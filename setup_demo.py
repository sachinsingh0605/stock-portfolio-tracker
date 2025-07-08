#!/usr/bin/env python3
"""
Setup demo data for the Stock Portfolio Tracker
"""

import sqlite3
from datetime import datetime

def setup_demo_data():
    """Add some demo stocks to the portfolio"""
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
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

    # Demo stocks with realistic purchase prices
    demo_stocks = [
        ('AAPL', 10, 150.00, '2024-01-15'),
        ('GOOGL', 5, 2800.00, '2024-02-01'),
        ('MSFT', 8, 380.00, '2024-01-20'),
        ('TSLA', 3, 200.00, '2024-03-01'),
        ('AMZN', 6, 145.00, '2024-02-15'),
        ('META', 4, 350.00, '2024-01-10'),
        ('NFLX', 7, 450.00, '2024-02-20')
    ]

    print("Adding demo stocks to portfolio...")

    # Clear existing data
    cursor.execute('DELETE FROM portfolio')
    cursor.execute('DELETE FROM price_history')

    for symbol, quantity, price, date in demo_stocks:
        cursor.execute("""
            INSERT INTO portfolio (symbol, quantity, purchase_price, purchase_date)
            VALUES (?, ?, ?, ?)
        """, (symbol, quantity, price, date))
        print(f"Added {quantity} shares of {symbol} at ${price}")

    conn.commit()
    conn.close()

    print("\n✅ Demo data added successfully!")
    print("💡 Run 'python portfolio_tracker.py' to see your portfolio.")

if __name__ == "__main__":
    setup_demo_data()
