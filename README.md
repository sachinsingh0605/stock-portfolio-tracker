# Stock Portfolio Tracker

A simple yet powerful desktop application for tracking stock investments, built with Python and SQLite. Perfect for demonstrating programming skills for finance job applications.

## 🎯 Features

- **Add Stocks**: Input stock symbols, quantities, and purchase prices
- **Real-time Prices**: Fetch current stock prices from Yahoo Finance API
- **Portfolio Management**: View all holdings with automatic gain/loss calculations
- **Data Export**: Export portfolio data to CSV format for external analysis
- **Database Storage**: Persistent storage using SQLite database
- **Clean GUI**: User-friendly interface built with tkinter
- **Multi-threading**: Non-blocking price updates to prevent GUI freezing

## 📸 Screenshots

![Portfolio Tracker Interface](https://via.placeholder.com/800x600?text=Portfolio+Tracker+Interface)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection (for fetching stock prices)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/yourusername/stock-portfolio-tracker.git
   cd stock-portfolio-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python portfolio_tracker.py
   ```

### Alternative Launch Methods

- **Using the launcher script:**
  ```bash
  python run.py
  ```

- **Add demo data (optional):**
  ```bash
  python setup_demo.py
  ```

- **Run tests:**
  ```bash
  python test_portfolio.py
  ```

## 💡 How to Use

### Adding Stocks
1. Enter stock symbol (e.g., AAPL, GOOGL, MSFT)
2. Enter quantity of shares purchased
3. Enter purchase price per share
4. Click "Add Stock"

### Viewing Portfolio
- See all your stocks with current prices
- View gain/loss for each position
- Monitor total portfolio value
- Stocks are automatically grouped by symbol

### Refreshing Prices
- Click "Refresh Prices" to update current market prices
- Uses Yahoo Finance API for real-time data
- Updates happen in background thread (non-blocking)

### Managing Positions
- Select a stock in the table and click "Delete Selected" to remove
- Export portfolio data to CSV for external analysis
- All data is automatically saved to SQLite database

## 🏗️ Project Structure

```
stock-portfolio-tracker/
├── portfolio_tracker.py    # Main application file
├── requirements.txt        # Python dependencies
├── setup_demo.py          # Demo data setup script
├── run.py                 # Application launcher
├── test_portfolio.py      # Test suite
├── README.md              # This file
├── .gitignore            # Git ignore patterns
└── portfolio.db          # SQLite database (created automatically)
```

## 🔧 Technical Details

### Database Schema

**Portfolio Table:**
- `id`: Primary key (auto-increment)
- `symbol`: Stock symbol (TEXT)
- `quantity`: Number of shares (INTEGER)
- `purchase_price`: Price per share at purchase (REAL)
- `purchase_date`: Date of purchase (TEXT)
- `created_at`: Timestamp of record creation

**Price History Table:**
- `id`: Primary key (auto-increment)
- `symbol`: Stock symbol (TEXT)
- `price`: Current price (REAL)
- `date`: Date of price record (TEXT)
- Unique constraint on (symbol, date)

### Key Features Implementation

**GUI Components:**
- `tkinter` for cross-platform desktop interface
- `ttk` widgets for modern appearance
- `Treeview` for tabular data display
- Thread-safe price updates

**Data Management:**
- SQLite database for persistent storage
- Pandas for data manipulation and CSV export
- Proper input validation and error handling

**Financial Calculations:**
- Automatic gain/loss computation
- Portfolio value aggregation
- Average price calculation for multiple purchases

## 📋 Resume Points

### Technical Skills Demonstrated
- **Python Programming**: Object-oriented design, GUI development
- **Database Management**: SQLite, SQL queries, data modeling
- **API Integration**: Yahoo Finance API for real-time data
- **Data Processing**: Pandas for data manipulation
- **Multi-threading**: Background processing for responsive UI
- **Error Handling**: Comprehensive input validation

### Professional Features
- **Complete Application**: End-to-end functionality
- **Production Ready**: Proper error handling and user feedback
- **Modular Design**: Clean, maintainable code structure
- **Documentation**: Comprehensive README and comments

## 🧪 Testing

Run the test suite to verify all functionality:

```bash
python test_portfolio.py
```

Tests cover:
- Module imports and dependencies
- Database operations (create, read, update, delete)
- Financial calculations accuracy
- CSV export functionality

## 🚀 Installation Troubleshooting

### Common Issues

**Import Error: No module named 'yfinance'**
```bash
pip install yfinance pandas
```

**Tkinter Not Found (Linux)**
```bash
sudo apt-get install python3-tk
```

**Permission Denied (macOS)**
```bash
pip install --user yfinance pandas
```

### Requirements
- `yfinance==0.2.18` - Yahoo Finance API for stock data
- `pandas==2.0.3` - Data manipulation and CSV export

## 📊 Example Usage

1. **Start the application**
   ```bash
   python portfolio_tracker.py
   ```

2. **Add some stocks**
   - AAPL: 10 shares at $150.00
   - GOOGL: 5 shares at $2800.00
   - MSFT: 8 shares at $380.00

3. **Refresh prices** to see current values and gains/losses

4. **Export to CSV** for further analysis

## 🎯 Interview Talking Points

When discussing this project:

1. **Database Design**: "I designed a normalized SQLite schema with proper relationships and constraints"
2. **API Integration**: "I integrated Yahoo Finance API with proper error handling and rate limiting"
3. **GUI Development**: "I built a responsive desktop application using tkinter with multi-threading"
4. **Financial Logic**: "I implemented portfolio calculations including gain/loss analysis and valuation"
5. **Error Handling**: "I added comprehensive input validation and user feedback mechanisms"

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Perfect for finance job applications!** This project demonstrates practical programming skills applied to financial domain problems.
