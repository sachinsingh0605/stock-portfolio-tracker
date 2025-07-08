# 📈 Stock Portfolio Tracker (India Edition 🇮🇳)

A desktop GUI application built with **Python & Tkinter** to manage and monitor your stock portfolio in real-time. Designed especially for the **Indian stock market**, this tool helps track gains/losses, fetches live prices (via Yahoo Finance), and exports data effortlessly.

---

## 🔧 Features

- 🏦 Track multiple Indian stocks (NSE/BSE) like `HDFCBANK.NS`, `INFY.NS`, etc.
- 💸 Live stock price updates with `₹` currency symbol.
- 📊 Real-time gain/loss & total value calculations.
- 🧾 SQLite-powered local storage.
- 📁 Export portfolio to CSV.
- 🧹 Add/Delete stocks easily.
- 🚀 Auto-refresh with threading to prevent GUI freeze.

---

## 🖼️ Preview

![Portfolio Screenshot](./screenshot.png) <!-- (Optional: Replace with actual screenshot path) -->

---

## 🛠️ Requirements

- Python 3.8+
- Modules:
  - `yfinance`
  - `pandas`
  - `tkinter` *(usually built-in)*

---

## 📦 Installation

1. **Clone or Download the repo**
   ```bash
   git clone https://github.com/yourusername/portfolio-tracker.git
   cd portfolio-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. *(Optional)* **Setup demo data**
   ```bash
   python setup_demo.py
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

---

## 🔍 Supported Stock Format

To track Indian stocks, use the **`.NS`** suffix for NSE stocks (e.g., `TCS.NS`, `RELIANCE.NS`).  
You can search & autocomplete symbols using the updated dropdown feature.

---

## 📤 Exporting

Click on **"Export CSV"** to download your full portfolio data to a `.csv` file for further analysis in Excel, Google Sheets, or Power BI.

---

## ✅ Testing

Run the built-in test suite to validate core functionality:
```bash
python test_portfolio.py
```

---

## 💡 Tips

- Prices are fetched in **INR (₹)** using Yahoo Finance.
- You can manually add more stock symbols or import from CSV.

---

## 🧠 Powered By

- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Yahoo Finance API via yfinance](https://pypi.org/project/yfinance/)
- [SQLite3](https://www.sqlite.org/index.html)
- [Pandas](https://pandas.pydata.org/)

---

## 📃 License

MIT License — free for personal or commercial use.

---

> Crafted with ❤️ by [Your Name] | Feel free to fork, star, or contribute!
