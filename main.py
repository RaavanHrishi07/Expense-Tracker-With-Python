
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("950x650")
        self.root.minsize(800, 550)
        self.root.configure(bg="#111827")

        self.transactions = []

        self.create_ui()

    def create_ui(self):
        # Header
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

        # First row
        tk.Label(
            form, text="Type", bg="#1F2937", fg="white"
        ).grid(row=0, column=0, sticky="w", padx=8, pady=5)

        type_box = ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=15
        )
        type_box.grid(row=1, column=0, padx=8, pady=5)

        tk.Label(
            form, text="Category", bg="#1F2937", fg="white"
        ).grid(row=0, column=1, sticky="w", padx=8, pady=5)

        self.category_box = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                "Food", "Transport", "Shopping",
                "Bills", "Entertainment", "Salary",
                "Business", "Other"
            ],
            width=18
        )
        self.category_box.grid(row=1, column=1, padx=8, pady=5)

        tk.Label(
            form, text="Amount (₹)", bg="#1F2937", fg="white"
        ).grid(row=0, column=2, sticky="w", padx=8, pady=5)

        tk.Entry(
            form,
            textvariable=self.amount_var,
            width=17
        ).grid(row=1, column=2, padx=8, pady=5)

        # Second row
        tk.Label(
            form, text="Date (YYYY-MM-DD)",
            bg="#1F2937", fg="white"
        ).grid(row=2, column=0, sticky="w", padx=8, pady=8)

        tk.Entry(
            form,
            textvariable=self.date_var,
            width=18
        ).grid(row=3, column=0, padx=8, pady=5)

        tk.Label(
            form, text="Description",
            bg="#1F2937", fg="white"
        ).grid(row=2, column=1, sticky="w", padx=8, pady=8)

        tk.Entry(
            form,
            textvariable=self.note_var,
            width=40
        ).grid(
            row=3, column=1, columnspan=2,
            sticky="w", padx=8, pady=5
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
            self.table.heading(column, text=headings[column])
            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.table.pack(fill="both", expand=True)

        # Table styling
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

        self.status_label = tk.Label(
            self.root,
            text="Ready | No transactions added",
            bg="#111827",
            fg="#9CA3AF",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=8)

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

        transaction = {
            "date": transaction_date,
            "type": transaction_type,
            "category": category,
            "amount": amount,
            "description": description
        }

        self.transactions.append(transaction)

        self.table.insert(
            "",
            "end",
            values=(
                transaction_date,
                transaction_type,
                category,
                f"₹{amount:,.2f}",
                description
            )
        )

        self.update_summary()

        self.amount_var.set("")
        self.note_var.set("")

        self.status_label.config(
            text=f"Transaction added successfully | {len(self.transactions)} total"
        )

    def update_summary(self):
        total_income = sum(
            item["amount"]
            for item in self.transactions
            if item["type"] == "Income"
        )

        total_expense = sum(
            item["amount"]
            for item in self.transactions
            if item["type"] == "Expense"
        )

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


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
