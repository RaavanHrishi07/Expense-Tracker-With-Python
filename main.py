
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import calendar

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DB_NAME = "expenses.db"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Salary",
    "Business",
    "Other"
]


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1100x850")
        self.root.minsize(950, 700)

        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        self.create_database()
        self.setup_style()
        self.create_widgets()
        self.load_transactions()
        self.update_summary()
        self.update_monthly_summary()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)
        self.conn.commit()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=27)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("TButton", padding=6)

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="PERSONAL EXPENSE TRACKER",
            font=("Arial", 21, "bold")
        )
        title.pack(pady=12)

        # Overall summary cards
        summary_frame = tk.Frame(self.root)
        summary_frame.pack(fill="x", padx=20, pady=5)

        self.income_label = self.create_card(
            summary_frame, "TOTAL INCOME", "0.00"
        )
        self.expense_label = self.create_card(
            summary_frame, "TOTAL EXPENSE", "0.00"
        )
        self.balance_label = self.create_card(
            summary_frame, "BALANCE", "0.00"
        )

        # Transaction form
        form = tk.LabelFrame(
            self.root,
            text="Add New Transaction",
            padx=12,
            pady=10
        )
        form.pack(fill="x", padx=20, pady=8)

        tk.Label(form, text="Type").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Expense")
        ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=15
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Category").grid(row=0, column=2, padx=5)
        self.category_var = tk.StringVar(value="Food")
        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=CATEGORIES,
            state="readonly",
            width=15
        ).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Amount").grid(row=0, column=4, padx=5)
        self.amount_entry = ttk.Entry(form, width=16)
        self.amount_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(form, text="Date (YYYY-MM-DD)").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.date_entry = ttk.Entry(form, width=18)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Description").grid(
            row=1, column=2, padx=5
        )
        self.description_entry = ttk.Entry(form, width=35)
        self.description_entry.grid(
            row=1, column=3, columnspan=2, padx=5, pady=5
        )

        ttk.Button(
            form,
            text="Add Transaction",
            command=self.add_transaction
        ).grid(row=1, column=5, padx=5, pady=5)

        # Filters
        filter_frame = tk.LabelFrame(
            self.root,
            text="Transaction Filters",
            padx=10,
            pady=8
        )
        filter_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(filter_frame, text="Category:").pack(side="left", padx=5)

        self.filter_category = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_category,
            values=["All"] + CATEGORIES,
            state="readonly",
            width=15
        ).pack(side="left", padx=5)

        tk.Label(filter_frame, text="Type:").pack(side="left", padx=5)

        self.filter_type = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_type,
            values=["All", "Income", "Expense"],
            state="readonly",
            width=12
        ).pack(side="left", padx=5)

        tk.Label(filter_frame, text="Month (YYYY-MM):").pack(
            side="left", padx=5
        )

        self.month_filter = ttk.Entry(filter_frame, width=12)
        self.month_filter.pack(side="left", padx=5)

        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.apply_filters
        ).pack(side="left", padx=5)

        ttk.Button(
            filter_frame,
            text="Reset",
            command=self.reset_filters
        ).pack(side="left", padx=5)

        # Monthly summary
        monthly_frame = tk.LabelFrame(
            self.root,
            text="Monthly Summary",
            padx=10,
            pady=8
        )
        monthly_frame.pack(fill="x", padx=20, pady=5)

        self.month_income_label = tk.Label(
            monthly_frame, text="Income: 0.00",
            font=("Arial", 10, "bold")
        )
        self.month_income_label.pack(side="left", padx=20)

        self.month_expense_label = tk.Label(
            monthly_frame, text="Expense: 0.00",
            font=("Arial", 10, "bold")
        )
        self.month_expense_label.pack(side="left", padx=20)

        self.month_balance_label = tk.Label(
            monthly_frame, text="Balance: 0.00",
            font=("Arial", 10, "bold")
        )
        self.month_balance_label.pack(side="left", padx=20)

        # Transactions table
        table_frame = tk.LabelFrame(
            self.root,
            text="Transaction History",
            padx=10,
            pady=8
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=8)

        columns = (
            "ID", "Date", "Type", "Category", "Amount", "Description"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.tree.heading(column, text=column)

        self.tree.column("ID", width=45, anchor="center")
        self.tree.column("Date", width=110, anchor="center")
        self.tree.column("Type", width=90, anchor="center")
        self.tree.column("Category", width=120, anchor="center")
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Description", width=250)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_transaction
        ).pack(side="left", padx=5)

        ttk.Button(
            action_frame,
            text="View Financial Charts",
            command=self.show_charts
        ).pack(side="left", padx=5)

    def create_card(self, parent, title, value):
        card = tk.LabelFrame(parent, text=title, padx=15, pady=10)
        card.pack(side="left", fill="both", expand=True, padx=8)

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 17, "bold")
        )
        label.pack()

        return label

    def add_transaction(self):
        transaction_type = self.type_var.get()
        category = self.category_var.get()
        amount_text = self.amount_entry.get().strip()
        date_text = self.date_entry.get().strip()
        description = self.description_entry.get().strip()

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount greater than zero."
            )
            return

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please enter the date in YYYY-MM-DD format."
            )
            return

        self.cursor.execute("""
            INSERT INTO transactions
            (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            date_text,
            transaction_type,
            category,
            amount,
            description
        ))

        self.conn.commit()

        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

        self.load_transactions()
        self.update_summary()
        self.update_monthly_summary()

        messagebox.showinfo(
            "Success",
            "Transaction added successfully!"
        )

    def load_transactions(self, query=None, params=()):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if query is None:
            query = """
                SELECT id, date, type, category, amount, description
                FROM transactions
                ORDER BY date DESC, id DESC
            """

        self.cursor.execute(query, params)

        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def update_summary(self):
        self.cursor.execute("""
            SELECT
                SUM(CASE WHEN type='Income' THEN amount ELSE 0 END),
                SUM(CASE WHEN type='Expense' THEN amount ELSE 0 END)
            FROM transactions
        """)

        income, expense = self.cursor.fetchone()
        income = income or 0
        expense = expense or 0
        balance = income - expense

        self.income_label.config(text=f"₹{income:,.2f}")
        self.expense_label.config(text=f"₹{expense:,.2f}")
        self.balance_label.config(text=f"₹{balance:,.2f}")

    def update_monthly_summary(self):
        month = datetime.today().strftime("%Y-%m")

        self.cursor.execute("""
            SELECT
                SUM(CASE WHEN type='Income' THEN amount ELSE 0 END),
                SUM(CASE WHEN type='Expense' THEN amount ELSE 0 END)
            FROM transactions
            WHERE date LIKE ?
        """, (month + "%",))

        income, expense = self.cursor.fetchone()
        income = income or 0
        expense = expense or 0

        self.month_income_label.config(
            text=f"Income: ₹{income:,.2f}"
        )
        self.month_expense_label.config(
            text=f"Expense: ₹{expense:,.2f}"
        )
        self.month_balance_label.config(
            text=f"Balance: ₹{income - expense:,.2f}"
        )

    def apply_filters(self):
        query = """
            SELECT id, date, type, category, amount, description
            FROM transactions
            WHERE 1=1
        """
        params = []

        category = self.filter_category.get()
        transaction_type = self.filter_type.get()
        month = self.month_filter.get().strip()

        if category != "All":
            query += " AND category = ?"
            params.append(category)

        if transaction_type != "All":
            query += " AND type = ?"
            params.append(transaction_type)

        if month:
            try:
                datetime.strptime(month, "%Y-%m")
            except ValueError:
                messagebox.showerror(
                    "Invalid Month",
                    "Please use YYYY-MM format."
                )
                return

            query += " AND date LIKE ?"
            params.append(month + "%")

        query += " ORDER BY date DESC, id DESC"

        self.load_transactions(query, params)

    def reset_filters(self):
        self.filter_category.set("All")
        self.filter_type.set("All")
        self.month_filter.delete(0, tk.END)
        self.load_transactions()

    def delete_transaction(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        transaction_id = self.tree.item(
            selected[0], "values"
        )[0]

        self.cursor.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )
        self.conn.commit()

        self.load_transactions()
        self.update_summary()
        self.update_monthly_summary()

        messagebox.showinfo(
            "Deleted",
            "Transaction deleted successfully."
        )

    def get_monthly_expense_trend(self):
        today = datetime.today()
        months = []

        for offset in range(5, -1, -1):
            year = today.year
            month = today.month - offset

            while month <= 0:
                month += 12
                year -= 1

            month_key = f"{year:04d}-{month:02d}"
            month_label = calendar.month_abbr[month]

            self.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE type = 'Expense' AND date LIKE ?
            """, (month_key + "%",))

            total = self.cursor.fetchone()[0]
            months.append((month_label, total))

        return months

    def show_charts(self):
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Financial Dashboard")
        chart_window.geometry("1150x750")

        heading = tk.Label(
            chart_window,
            text="FINANCIAL DASHBOARD",
            font=("Arial", 18, "bold")
        )
        heading.pack(pady=10)

        figure = Figure(figsize=(11, 6.5), dpi=100)

        # Chart 1: Expense by category
        ax1 = figure.add_subplot(221)

        self.cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'Expense'
            GROUP BY category
        """)

        category_data = self.cursor.fetchall()

        if category_data:
            labels = [row[0] for row in category_data]
            values = [row[1] for row in category_data]

            ax1.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )
            ax1.set_title("Expenses by Category")
        else:
            ax1.text(
                0.5, 0.5, "No expense data available",
                ha="center", va="center"
            )
            ax1.set_title("Expenses by Category")

        # Chart 2: Income vs Expense
        ax2 = figure.add_subplot(222)

        self.cursor.execute("""
            SELECT
                SUM(CASE WHEN type='Income' THEN amount ELSE 0 END),
                SUM(CASE WHEN type='Expense' THEN amount ELSE 0 END)
            FROM transactions
        """)

        income, expense = self.cursor.fetchone()
        income = income or 0
        expense = expense or 0

        ax2.bar(
            ["Income", "Expense"],
            [income, expense]
        )
        ax2.set_title("Overall Income vs Expense")
        ax2.set_ylabel("Amount (₹)")

        # Chart 3: Last six months expense trend
        ax3 = figure.add_subplot(212)

        trend = self.get_monthly_expense_trend()
        month_labels = [item[0] for item in trend]
        expense_values = [item[1] for item in trend]

        ax3.plot(
            month_labels,
            expense_values,
            marker="o"
        )
        ax3.set_title("Monthly Expense Trend - Last 6 Months")
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Expense (₹)")
        ax3.grid(True, alpha=0.3)

        figure.tight_layout(pad=3)

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_window
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def close_app(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
