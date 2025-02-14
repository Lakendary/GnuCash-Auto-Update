# GnuCash Auto Update

## Overview

GnuCash Auto Update is a Flask-based web application that connects to a MySQL database used by GnuCash. It simplifies the process of updating transaction descriptions, memos, and notes after importing bank statements from CSV or OFX files. The app allows users to automate updates based on predefined search terms and account mappings, making financial data organization more efficient.

## Features

🚀 Automated Transaction Updates: Modify descriptions, memos, and notes based on search terms.

🔍 Search Term Management: Add new search terms to customize transaction updates.

🏦 Account Selection: Choose the bank account and corresponding income, expense, asset, or liability account.

📅 Date Filtering: Select a specific period for transaction updates.

🛢 Database Connection: Currently supports MySQL.

### Future Features

🗄 Additional Database Support: PostgreSQL and SQLite integration.

❌ Search Term Management Enhancements: Ability to delete search terms.

✅ Reconciliation Settings: Option to update or exclude reconciled transactions.

## Installation

### Prerequisites

Ensure you have the following installed:
- 🐍 Python 3.8+
- 🛢 MySQL Server
- ⚙️ Flask and required dependencies

### Setup Steps

1. 📥 Clone the repository:
`git clone https://github.com/Lakendary/GnuCash-Auto-Update.git
cd GnuCash-Auto-Update`
2. 🛠 Create and activate a virtual environment (optional but recommended):
`python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate`
3. 📦 Install dependencies:
`pip install -r requirements.txt`
4. ⚙️ Configure the database connection:
- Update the .env file with your MySQL credentials.
- Example:
`DATABASE_URL=mysql://user:password@localhost/gnucash`
5. 🚀 Run the Flask application:
`flask run`
6. 🌐 Access the application:
  Open your browser and go to http://127.0.0.1:5000/

## Usage

- 📂 Import Transactions: Upload a CSV or OFX file.
- 🔎 Define Search Terms: Add or manage search terms to automate transaction updates.
- 🔄 Update Transactions: Select the date range and accounts, then apply updates.

## Contributing

Contributions are welcome! If you’d like to add new features or fix bugs:
1. 🍴 Fork the repository.
2. 🌿 Create a new branch (git checkout -b feature-branch).
3. 📝 Commit your changes (git commit -m "Add new feature").
4. 📤 Push to your branch (git push origin feature-branch).
5. 🔄 Open a pull request.

## License

This project is licensed under the MIT License. See LICENSE for details.

## Contact

For issues or feature requests, open an issue on GitHub: [GnuCash Auto Update](https://github.com/Lakendary/GnuCash-Auto-Update/issues/new)
