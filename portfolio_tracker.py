import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import yfinance as yf
import pandas as pd
from datetime import datetime
import threading
import csv

class PortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("900x600")

        # Initialize database
        self.init_database()

        # Create GUI
        self.create_widgets()

        # Load existing data
        self.refresh_portfolio()

    def init_database(self):
        self.conn = sqlite3.connect('portfolio.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                purchase_price REAL NOT NULL,
                purchase_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT NOT NULL,
                UNIQUE(symbol, date)
            )
        """)
        self.conn.commit()

    def load_symbols_from_csv(self):
        symbols = []
        try:
            with open('nse_symbols.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbols.append(row['Symbol'])
        except Exception as e:
            print(f"Error loading symbols: {e}")
        return symbols

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        input_frame = ttk.LabelFrame(main_frame, text="Add Stock", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(input_frame, text="Symbol:").grid(row=0, column=0, sticky=tk.W)
        self.stock_symbols = self.load_symbols_from_csv()
        self.symbol_entry = ttk.Combobox(input_frame, values=self.stock_symbols)
        self.symbol_entry.grid(row=0, column=1, padx=(5, 20))

        ttk.Label(input_frame, text="Quantity:").grid(row=0, column=2, sticky=tk.W)
        self.quantity_entry = ttk.Entry(input_frame, width=15)
        self.quantity_entry.grid(row=0, column=3, padx=(5, 20))

        ttk.Label(input_frame, text="Purchase Price:").grid(row=0, column=4, sticky=tk.W)
        self.price_entry = ttk.Entry(input_frame, width=15)
        self.price_entry.grid(row=0, column=5, padx=(5, 20))

        ttk.Button(input_frame, text="Add Stock", command=self.add_stock).grid(row=0, column=6, padx=(10, 0))

        display_frame = ttk.LabelFrame(main_frame, text="Portfolio", padding="10")
        display_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        columns = ('Symbol', 'Quantity', 'Purchase Price', 'Current Price', 'Gain/Loss', 'Total Value')
        self.tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(button_frame, text="Refresh Prices", command=self.refresh_prices_threaded).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=(0, 10))

        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

    def add_stock(self):
        symbol = self.symbol_entry.get().upper().strip()
        if not symbol.endswith(".NS"):
            symbol += ".NS"
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not symbol or not quantity or not price:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and price must be a number")
            return

        if quantity <= 0 or price <= 0:
            messagebox.showerror("Error", "Quantity and price must be positive numbers")
            return

        purchase_date = datetime.now().strftime('%Y-%m-%d')
        try:
            self.cursor.execute("""
                INSERT INTO portfolio (symbol, quantity, purchase_price, purchase_date)
                VALUES (?, ?, ?, ?)
            """, (symbol, quantity, price, purchase_date))
            self.conn.commit()
            self.symbol_entry.set('')
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.refresh_portfolio()
            self.status_label.config(text=f"Added {quantity} shares of {symbol}")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def refresh_portfolio(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("""
            SELECT symbol, SUM(quantity) as total_quantity, AVG(purchase_price) as avg_price
            FROM portfolio
            GROUP BY symbol
        """)
        portfolio_data = self.cursor.fetchall()

        if not portfolio_data:
            self.status_label.config(text="No stocks in portfolio")
            return

        for symbol, quantity, avg_price in portfolio_data:
            self.tree.insert('', 'end', values=(symbol, quantity, f"₹{avg_price:.2f}", "Loading...", "Loading...", "Loading..."))
        self.status_label.config(text="Portfolio loaded")

    def get_stock_price(self, symbol):
        """Get current stock price using yfinance and convert to INR if needed"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            currency = info.get('currency', 'USD')  # Get currency of stock

            if current_price is None:
                return None

            if currency == "INR":
                return round(current_price, 2)  # Already in rupees
            else:
                # Convert USD to INR
                usd_inr = yf.Ticker("USDINR=X").info.get("regularMarketPrice", None)
                if usd_inr is None:
                    print("⚠️ Unable to fetch USD to INR rate")
                    return None
                return round(current_price * usd_inr, 2)

        except Exception as e:
            print(f"Error getting price for {symbol}: {e}")
            return None



    def refresh_prices_threaded(self):
        def refresh_prices():
            self.status_label.config(text="Updating prices...")
            for item in self.tree.get_children():
                values = list(self.tree.item(item)['values'])
                symbol = values[0]
                quantity = int(values[1])
                purchase_price = float(values[2].replace('₹', ''))

                current_price = self.get_stock_price(symbol)
                if current_price:
                    gain_loss = (current_price - purchase_price) * quantity
                    total_value = current_price * quantity
                    self.tree.item(item, values=(
                        symbol, quantity, f"₹{purchase_price:.2f}", f"₹{current_price:.2f}", f"₹{gain_loss:.2f}", f"₹{total_value:.2f}"
                    ))
                    today = datetime.now().strftime('%Y-%m-%d')
                    try:
                        self.cursor.execute("""
                            INSERT OR REPLACE INTO price_history (symbol, price, date)
                            VALUES (?, ?, ?)
                        """, (symbol, current_price, today))
                        self.conn.commit()
                    except sqlite3.Error:
                        pass
                else:
                    self.tree.item(item, values=(symbol, quantity, f"₹{purchase_price:.2f}", "Error", "Error", "Error"))
            self.status_label.config(text="Prices updated")

        thread = threading.Thread(target=refresh_prices)
        thread.daemon = True
        thread.start()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a stock to delete")
            return

        item = selected[0]
        symbol = self.tree.item(item)['values'][0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all {symbol} positions?"):
            try:
                self.cursor.execute('DELETE FROM portfolio WHERE symbol = ?', (symbol,))
                self.conn.commit()
                self.refresh_portfolio()
                self.status_label.config(text=f"Deleted {symbol} from portfolio")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    def export_csv(self):
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No data to export")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                data = [self.tree.item(item)['values'] for item in self.tree.get_children()]
                df = pd.DataFrame(data, columns=['Symbol', 'Quantity', 'Purchase Price', 'Current Price', 'Gain/Loss', 'Total Value'])
                df.to_csv(filename, index=False)
                self.status_label.config(text=f"Data exported to {filename}")
                messagebox.showinfo("Success", f"Portfolio data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = PortfolioTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
