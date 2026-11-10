
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sqlite3


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("950x650")
        self.root.minsize(800, 550)
        self.root.configure(bg="#111827")

        self.db_connection = sqlite3.connect("expenses.db")
        self.cursor = self.db_connection.cursor()

        self.create_database()
        self.create_ui()
        self.load_transactions()

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

    def create_ui(self):
        header = tk.Frame(self.root, bg="#111827")
        header.pack(fill="x", padx=25, pady=20)

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

        # Summary cards
        summary = tk.Frame(self.root, bg="#111827")
        summary.pack(fill="x", padx=25, pady=10)

        self.income_label = self.create_card(
            summary, "TOTAL INCOME", "₹0", "#22C55E"
        )

        self.expense_label = self.create_card(
            summary, "TOTAL EXPENSE", "₹0", "#EF4444"
        )

        self.balance_label = self.create_card(
            summary, "BALANCE", "₹0", "#38BDF8"
        )

        # Transaction form
        form = tk.LabelFrame(
            self.root,
            text="  ADD TRANSACTION  ",
            font=("Arial", 11, "bold"),
            bg="#1F2937",
            fg="#38BDF8",
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=25, pady=15)

        self.type_var = tk.StringVar(value="Expense")
        self.category_var = tk.StringVar(value="Food")
        self.amount_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.date_var = tk.StringVar(value=date.today().isoformat())

        tk.Label(
            form,
            text="Type",
            bg="#1F2937",
            fg="white"
        ).grid(row=0, column=0, sticky="w", padx=8, pady=5)

        ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=15
        ).grid(row=1, column=0, padx=8, pady=5)

        tk.Label(
            form,
            text="Category",
            bg="#1F2937",
            fg="white"
        ).grid(row=0, column=1, sticky="w", padx=8, pady=5)

        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                "Food", "Transport", "Shopping",
                "Bills", "Entertainment", "Salary",
                "Business", "Other"
            ],
            width=18
        ).grid(row=1, column=1, padx=8, pady=5)

        tk.Label(
            form,
            text="Amount (₹)",
            bg="#1F2937",
            fg="white"
        ).grid(row=0, column=2, sticky="w", padx=8, pady=5)

        tk.Entry(
            form,
            textvariable=self.amount_var,
            width=17
        ).grid(row=1, column=2, padx=8, pady=5)

        tk.Label(
            form,
            text="Date (YYYY-MM-DD)",
            bg="#1F2937",
            fg="white"
        ).grid(row=2, column=0, sticky="w", padx=8, pady=8)

        tk.Entry(
            form,
            textvariable=self.date_var,
            width=18
        ).grid(row=3, column=0, padx=8, pady=5)

        tk.Label(
            form,
            text="Description",
            bg="#1F2937",
            fg="white"
        ).grid(row=2, column=1, sticky="w", padx=8, pady=8)

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
            pady=5
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

        # Transaction table
        table_frame = tk.Frame(self.root, bg="#111827")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        tk.Label(
            table_frame,
            text="RECENT TRANSACTIONS",
            font=("Arial", 12, "bold"),
            bg="#111827",
            fg="white"
        ).pack(anchor="w", pady=(0, 10))

        columns = (
            "date", "type", "category",
            "amount", "description"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
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

        self.table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1F2937",
            foreground="white",
            fieldbackground="#1F2937",
            rowheight=30,
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
            table_frame,
            text="DELETE SELECTED TRANSACTION",
            command=self.delete_transaction,
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=8
        ).pack(anchor="e", pady=8)

        self.status_label = tk.Label(
            self.root,
            text="Ready | Database connected",
            bg="#111827",
            fg="#9CA3AF",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=8)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_card(self, parent, title, value, color):
        card = tk.Frame(
            parent,
            bg="#1F2937",
            padx=20,
            pady=15
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
            font=("Arial", 21, "bold"),
            bg="#1F2937",
            fg=color
        )

        label.pack(anchor="w", pady=5)

        return label

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

            self.load_transactions()

            self.amount_var.set("")
            self.note_var.set("")

            self.status_label.config(
                text="Transaction saved successfully!"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def load_transactions(self):
        self.cursor.execute("""
            SELECT id, date, type, category, amount, description
            FROM transactions
            ORDER BY date DESC, id DESC
        """)

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

        self.update_summary()

    def update_summary(self):
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

    def close_app(self):
        self.db_connection.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
