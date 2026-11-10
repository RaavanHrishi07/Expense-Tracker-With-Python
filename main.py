
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import sqlite3


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1050x800")
        self.root.minsize(900, 700)
        self.root.configure(bg="#111827")

        self.db_connection = sqlite3.connect("expenses.db")
        self.cursor = self.db_connection.cursor()

        self.create_database()
        self.create_ui()
        self.load_transactions()

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
        self.db_connection.commit()

    # ---------------- USER INTERFACE ----------------

    def create_ui(self):
        header = tk.Frame(self.root, bg="#111827")
        header.pack(fill="x", padx=25, pady=15)

        tk.Label(
            header,
            text="EXPENSE TRACKER",
            font=("Arial", 24, "bold"),
            bg="#111827",
            fg="#38BDF8"
        ).pack(side="left")

        tk.Label(
            header,
            text="Manage your money smartly",
            font=("Arial", 10),
            bg="#111827",
            fg="#9CA3AF"
        ).pack(side="right", pady=10)

        # Overall summary cards
        summary = tk.Frame(self.root, bg="#111827")
        summary.pack(fill="x", padx=25, pady=8)

        self.income_label = self.create_card(
            summary, "TOTAL INCOME", "₹0", "#22C55E"
        )

        self.expense_label = self.create_card(
            summary, "TOTAL EXPENSE", "₹0", "#EF4444"
        )

        self.balance_label = self.create_card(
            summary, "TOTAL BALANCE", "₹0", "#38BDF8"
        )

        # Transaction form
        form = tk.LabelFrame(
            self.root,
            text="  ADD TRANSACTION  ",
            font=("Arial", 11, "bold"),
            bg="#1F2937",
            fg="#38BDF8",
            padx=15,
            pady=12
        )
        form.pack(fill="x", padx=25, pady=10)

        self.type_var = tk.StringVar(value="Expense")
        self.category_var = tk.StringVar(value="Food")
        self.amount_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.date_var = tk.StringVar(value=date.today().isoformat())

        tk.Label(
            form, text="Type", bg="#1F2937", fg="white"
        ).grid(row=0, column=0, sticky="w", padx=8, pady=4)

        ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=15
        ).grid(row=1, column=0, padx=8, pady=4)

        tk.Label(
            form, text="Category", bg="#1F2937", fg="white"
        ).grid(row=0, column=1, sticky="w", padx=8, pady=4)

        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                "Food", "Transport", "Shopping",
                "Bills", "Entertainment", "Salary",
                "Business", "Other"
            ],
            width=18
        ).grid(row=1, column=1, padx=8, pady=4)

        tk.Label(
            form, text="Amount (₹)", bg="#1F2937", fg="white"
        ).grid(row=0, column=2, sticky="w", padx=8, pady=4)

        tk.Entry(
            form,
            textvariable=self.amount_var,
            width=17
        ).grid(row=1, column=2, padx=8, pady=4)

        tk.Label(
            form,
            text="Date (YYYY-MM-DD)",
            bg="#1F2937",
            fg="white"
        ).grid(row=2, column=0, sticky="w", padx=8, pady=6)

        tk.Entry(
            form,
            textvariable=self.date_var,
            width=18
        ).grid(row=3, column=0, padx=8, pady=4)

        tk.Label(
            form,
            text="Description",
            bg="#1F2937",
            fg="white"
        ).grid(row=2, column=1, sticky="w", padx=8, pady=6)

        tk.Entry(
            form,
            textvariable=self.note_var,
            width=40
        ).grid(
            row=3,
            column=1,
            columnspan=2,
            sticky="w",
            padx=8,
            pady=4
        )

        tk.Button(
            form,
            text="+ ADD TRANSACTION",
            command=self.add_transaction,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            relief="flat",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        ).grid(row=1, column=3, rowspan=3, padx=15)

        # Filter section
        filter_frame = tk.LabelFrame(
            self.root,
            text="  FILTER TRANSACTIONS  ",
            font=("Arial", 10, "bold"),
            bg="#1F2937",
            fg="#38BDF8",
            padx=12,
            pady=10
        )
        filter_frame.pack(fill="x", padx=25, pady=8)

        self.filter_category = tk.StringVar(value="All")
        self.filter_type = tk.StringVar(value="All")
        self.filter_month = tk.StringVar(
            value=date.today().strftime("%Y-%m")
        )

        tk.Label(
            filter_frame,
            text="Category",
            bg="#1F2937",
            fg="white"
        ).grid(row=0, column=0, padx=6, sticky="w")

        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_category,
            values=[
                "All", "Food", "Transport", "Shopping",
                "Bills", "Entertainment", "Salary",
                "Business", "Other"
            ],
            state="readonly",
            width=15
        ).grid(row=1, column=0, padx=6, pady=5)

        tk.Label(
            filter_frame,
            text="Transaction Type",
            bg="#1F2937",
            fg="white"
        ).grid(row=0, column=1, padx=6, sticky="w")

        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_type,
            values=["All", "Income", "Expense"],
            state="readonly",
            width=14
        ).grid(row=1, column=1, padx=6, pady=5)

        tk.Label(
            filter_frame,
            text="Month (YYYY-MM)",
            bg="#1F2937",
            fg="white"
        ).grid(row=0, column=2, padx=6, sticky="w")

        tk.Entry(
            filter_frame,
            textvariable=self.filter_month,
            width=15
        ).grid(row=1, column=2, padx=6, pady=5)

        tk.Button(
            filter_frame,
            text="APPLY FILTER",
            command=self.apply_filters,
            bg="#2563EB",
            fg="white",
            relief="flat",
            padx=12,
            pady=7
        ).grid(row=1, column=3, padx=8)

        tk.Button(
            filter_frame,
            text="RESET",
            command=self.reset_filters,
            bg="#4B5563",
            fg="white",
            relief="flat",
            padx=12,
            pady=7
        ).grid(row=1, column=4, padx=5)

        # Monthly summary
        monthly_frame = tk.LabelFrame(
            self.root,
            text="  MONTHLY SUMMARY  ",
            font=("Arial", 10, "bold"),
            bg="#1F2937",
            fg="#38BDF8",
            padx=12,
            pady=10
        )
        monthly_frame.pack(fill="x", padx=25, pady=8)

        self.month_income_label = self.create_month_card(
            monthly_frame, "MONTHLY INCOME", "₹0", "#22C55E"
        )

        self.month_expense_label = self.create_month_card(
            monthly_frame, "MONTHLY EXPENSE", "₹0", "#EF4444"
        )

        self.month_balance_label = self.create_month_card(
            monthly_frame, "MONTHLY BALANCE", "₹0", "#38BDF8"
        )

        # Transaction table
        table_frame = tk.Frame(self.root, bg="#111827")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=8
        )

        tk.Label(
            table_frame,
            text="TRANSACTIONS",
            font=("Arial", 12, "bold"),
            bg="#111827",
            fg="white"
        ).pack(anchor="w", pady=(0, 8))

        columns = (
            "date", "type", "category",
            "amount", "description"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        headings = {
            "date": "DATE",
            "type": "TYPE",
            "category": "CATEGORY",
            "amount": "AMOUNT",
            "description": "DESCRIPTION"
        }

        widths = {
            "date": 130,
            "type": 100,
            "category": 140,
            "amount": 130,
            "description": 300
        }

        for column in columns:
            self.table.heading(
                column,
                text=headings[column]
            )
            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table styling
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1F2937",
            foreground="white",
            fieldbackground="#1F2937",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#374151",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#2563EB")]
        )

        # Delete button
        tk.Button(
            self.root,
            text="DELETE SELECTED TRANSACTION",
            command=self.delete_transaction,
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=7
        ).pack(anchor="e", padx=25, pady=5)

        self.status_label = tk.Label(
            self.root,
            text="Ready | Database connected",
            bg="#111827",
            fg="#9CA3AF",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=5)

    # ---------------- SUMMARY CARDS ----------------

    def create_card(self, parent, title, value, color):
        card = tk.Frame(
            parent,
            bg="#1F2937",
            padx=20,
            pady=12
        )
        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg="#1F2937",
            fg="#9CA3AF"
        ).pack(anchor="w")

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 20, "bold"),
            bg="#1F2937",
            fg=color
        )
        label.pack(anchor="w", pady=4)

        return label

    def create_month_card(self, parent, title, value, color):
        card = tk.Frame(
            parent,
            bg="#273449",
            padx=15,
            pady=8
        )
        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 9, "bold"),
            bg="#273449",
            fg="#9CA3AF"
        ).pack(anchor="w")

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 17, "bold"),
            bg="#273449",
            fg=color
        )
        label.pack(anchor="w", pady=3)

        return label

    # ---------------- DATABASE OPERATIONS ----------------

    def add_transaction(self):
        transaction_type = self.type_var.get()
        category = self.category_var.get().strip()
        amount_text = self.amount_var.get().strip()
        transaction_date = self.date_var.get().strip()
        description = self.note_var.get().strip()

        if not amount_text or not category or not transaction_date:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in the amount, category and date."
            )
            return

        try:
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

            date.fromisoformat(transaction_date)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid positive amount and date (YYYY-MM-DD)."
            )
            return

        try:
            self.cursor.execute("""
                INSERT INTO transactions
                (date, type, category, amount, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                transaction_date,
                transaction_type,
                category,
                amount,
                description
            ))

            self.db_connection.commit()

            self.amount_var.set("")
            self.note_var.set("")

            self.load_transactions()

            self.status_label.config(
                text="Transaction saved successfully!"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def load_transactions(self):
        self.update_overall_summary()
        self.apply_filters(show_message=False)

    def update_overall_summary(self):
        self.cursor.execute("""
            SELECT
                COALESCE(SUM(
                    CASE WHEN type = 'Income' THEN amount ELSE 0 END
                ), 0),
                COALESCE(SUM(
                    CASE WHEN type = 'Expense' THEN amount ELSE 0 END
                ), 0)
            FROM transactions
        """)

        total_income, total_expense = self.cursor.fetchone()
        balance = total_income - total_expense

        self.income_label.config(
            text=f"₹{total_income:,.2f}"
        )
        self.expense_label.config(
            text=f"₹{total_expense:,.2f}"
        )
        self.balance_label.config(
            text=f"₹{balance:,.2f}"
        )

    def update_monthly_summary(self, selected_month):
        self.cursor.execute("""
            SELECT
                COALESCE(SUM(
                    CASE WHEN type = 'Income' THEN amount ELSE 0 END
                ), 0),
                COALESCE(SUM(
                    CASE WHEN type = 'Expense' THEN amount ELSE 0 END
                ), 0)
            FROM transactions
            WHERE date LIKE ?
        """, (selected_month + "%",))

        monthly_income, monthly_expense = self.cursor.fetchone()
        monthly_balance = monthly_income - monthly_expense

        self.month_income_label.config(
            text=f"₹{monthly_income:,.2f}"
        )
        self.month_expense_label.config(
            text=f"₹{monthly_expense:,.2f}"
        )
        self.month_balance_label.config(
            text=f"₹{monthly_balance:,.2f}"
        )

    def delete_transaction(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Transaction",
                "Please select a transaction to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        try:
            transaction_id = int(selected[0])

            self.cursor.execute(
                "DELETE FROM transactions WHERE id = ?",
                (transaction_id,)
            )

            self.db_connection.commit()
            self.load_transactions()

            self.status_label.config(
                text="Transaction deleted successfully!"
            )

        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror(
                "Delete Error",
                str(error)
            )

    # ---------------- FILTERS ----------------

    def apply_filters(self, show_message=True):
        selected_month = self.filter_month.get().strip()

        try:
            datetime.strptime(selected_month, "%Y-%m")
        except ValueError:
            if show_message:
                messagebox.showerror(
                    "Invalid Month",
                    "Please enter the month in YYYY-MM format.\nExample: 2026-11"
                )
            return

        category = self.filter_category.get()
        transaction_type = self.filter_type.get()

        query = """
            SELECT id, date, type, category, amount, description
            FROM transactions
            WHERE date LIKE ?
        """

        parameters = [selected_month + "%"]

        if category != "All":
            query += " AND category = ?"
            parameters.append(category)

        if transaction_type != "All":
            query += " AND type = ?"
            parameters.append(transaction_type)

        query += " ORDER BY date DESC, id DESC"

        try:
            self.cursor.execute(query, parameters)
            records = self.cursor.fetchall()

            for item in self.table.get_children():
                self.table.delete(item)

            for record in records:
                transaction_id, transaction_date, transaction_type, category, amount, description = record

                self.table.insert(
                    "",
                    "end",
                    iid=str(transaction_id),
                    values=(
                        transaction_date,
                        transaction_type,
                        category,
                        f"₹{amount:,.2f}",
                        description or ""
                    )
                )

            # Monthly summary is independent of category/type filters.
            self.update_monthly_summary(selected_month)

            self.status_label.config(
                text=f"Showing {len(records)} transactions for {selected_month}"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Filter Error",
                str(error)
            )

    def reset_filters(self):
        self.filter_category.set("All")
        self.filter_type.set("All")
        self.filter_month.set(date.today().strftime("%Y-%m"))

        self.apply_filters()

    # ---------------- CLOSE APPLICATION ----------------

    def close_app(self):
        self.db_connection.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
