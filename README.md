# Personal Expense Tracker 💰

A Python-based Personal Expense Tracker built with Tkinter GUI and SQLite database. It helps users manage their income, expenses, transactions and monthly financial summaries through a simple desktop application.

## Features

- **Income & Expense Management** – Add income and expense transactions.
- **SQLite Database** – Automatically stores transactions locally.
- **Transaction History** – View all recorded transactions.
- **Delete Transactions** – Remove selected transactions.
- **Category Filters** – Filter transactions by category.
- **Type Filters** – View income or expenses separately.
- **Monthly Summary** – Check monthly income, expenses and balance.
- **Financial Dashboard** – Visualise financial data through charts.
- **Category Expense Chart** – View expenses by category.
- **Income vs Expense Chart** – Compare total income and expenses.
- **Monthly Expense Trend** – Track expenses over the last six months.
- **Input Validation** – Validates amounts and dates before saving.

## Technologies Used

- Python 3
- Tkinter
- SQLite3
- Matplotlib

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RaavanHrishi07/Expense-Tracker-With-Python.git
   ```

2. Navigate to the project folder:

   ```bash
   cd Expense-Tracker-With-Python
   ```

3. Install the required library:

   ```bash
   pip install matplotlib
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## Database

The application automatically creates a local SQLite database named `expenses.db` when it runs for the first time.

Your transactions are stored locally and remain available when you reopen the application.

## Application Workflow

1. Add an income or expense transaction.
2. Select a category and enter the amount and date.
3. View transactions in the history table.
4. Apply category, type or month filters.
5. Review monthly financial summaries.
6. Open the Financial Dashboard to explore charts.

## Project Structure

```text
Expense-Tracker-With-Python/
│
├── main.py
├── expenses.db       # Generated locally when the application runs
├── README.md
├── .gitignore
└── LICENSE
```

## Future Improvements

- Export transactions to CSV or Excel.
- Add user authentication.
- Add budget planning and alerts.
- Add PDF financial reports.
- Improve dashboard customisation.

## Author

**Hrishikesh Sharma**

GitHub: [RaavanHrishi07](https://github.com/RaavanHrishi07)

## License

This project is licensed under the MIT License.