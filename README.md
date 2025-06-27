# Professional Budget Tracker

A comprehensive, feature-rich personal finance management system built with Python. This application demonstrates modern software development practices including object-oriented design, data persistence, type hints, and both CLI and web interfaces.

## 🚀 Features

### Core Functionality
- **Transaction Management**: Add, view, and remove income and expense transactions
- **Categorization**: 15 predefined categories for better organization
- **Data Persistence**: Automatic JSON-based data storage
- **Date Tracking**: Full date support with monthly summaries
- **Balance Calculation**: Real-time balance and savings rate tracking

### Advanced Features
- **Monthly Reports**: Detailed monthly summaries with category breakdowns
- **CSV Export**: Export transaction data for external analysis
- **Tagging System**: Add custom tags to transactions
- **Currency Formatting**: Professional currency display with locale support
- **Error Handling**: Robust error handling and validation
- **Interactive CLI**: User-friendly command-line interface with emojis
- **Web Interface**: Modern, responsive web application with charts and filtering

### Technical Highlights
- **Type Hints**: Full type annotation for better code maintainability
- **Data Classes**: Modern Python dataclasses for clean data structures
- **Enums**: Type-safe category and transaction type management
- **Modular Design**: Separation of concerns with distinct classes
- **Documentation**: Comprehensive docstrings and comments
- **Web Framework**: Flask-based web interface with Bootstrap UI

## 📋 Requirements

- Python 3.7+
- Flask (for web interface only)

## 🛠️ Installation

1. Clone or download the project
2. Install dependencies (for web interface):
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

### Command Line Interface (No dependencies required!)
```bash
python3 budget-tracker.py
```

### Web Interface
```bash
python3 web_demo.py
```
Then open your browser to: http://localhost:5000

### Demo Script
```bash
python3 demo.py
```

## 📖 CLI Menu Options

1. **Add Transaction**: Create new income or expense entries
2. **View All Transactions**: See complete transaction history
3. **View Balance Summary**: Get current financial overview
4. **View Monthly Summary**: Analyze spending by month
5. **View Transactions by Category**: Filter by spending categories
6. **Remove Transaction**: Delete unwanted entries
7. **Export to CSV**: Export data for external analysis
8. **Exit**: Close the application

## 🌐 Web Interface Features

- **Dashboard**: Beautiful overview with charts and summary cards
- **Transaction Management**: Add, view, and delete transactions
- **Filtering**: Filter by category and transaction type
- **Reports**: Interactive charts and detailed financial analysis
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Bootstrap 5 with custom styling

## 📊 Transaction Categories

**Expenses:**
- Food & Dining
- Transportation
- Housing
- Utilities
- Entertainment
- Shopping
- Healthcare
- Education
- Travel
- Insurance
- Taxes
- Other Expense

**Income:**
- Salary
- Freelance
- Investment
- Business
- Other Income

## 💾 Data Storage

The application automatically saves all data to JSON files:
- `budget_data.json` (CLI version)
- `web_budget_data.json` (Web version)

## 📊 Sample Output

### CLI Interface
```
💰 PROFESSIONAL BUDGET TRACKER 💰
==================================================
1. Add Transaction
2. View All Transactions
3. View Balance Summary
4. View Monthly Summary
5. View Transactions by Category
6. Remove Transaction
7. Export to CSV
8. Exit
==================================================

📊 Balance Summary
========================================
Total Income:    $5,000.00
Total Expenses:  $3,200.00
----------------------------------------
Net Balance:     💚 $1,800.00
Savings Rate:    36.0%
```

### Web Interface
- Modern dashboard with interactive charts
- Responsive design with Bootstrap 5
- Real-time data visualization
- Professional financial reporting

## 🔧 Technical Architecture

### Class Structure

- **`TransactionType`**: Enum for income/expense classification
- **`Category`**: Enum for transaction categorization
- **`Transaction`**: Dataclass for transaction data with serialization
- **`BudgetTracker`**: Core business logic and data management
- **`BudgetTrackerCLI`**: User interface and interaction handling
- **Flask App**: Web interface with templates and routing

### Design Patterns

- **Data Transfer Objects**: Clean data structures with validation
- **Repository Pattern**: Centralized data access and persistence
- **Command Pattern**: Modular CLI command handling
- **Factory Pattern**: Transaction creation with validation
- **MVC Pattern**: Web interface with separation of concerns

## 🧪 Testing

The application includes comprehensive error handling and input validation:
- Amount validation (positive numbers only)
- Date range validation
- Category selection validation
- File I/O error handling
- Graceful error recovery
- Web form validation

## 📈 Future Enhancements

Potential improvements for future versions:
- Database integration (SQLite/PostgreSQL)
- User authentication and multi-user support
- Budget goals and alerts
- Recurring transaction support
- Advanced data visualization
- Multi-currency support
- Cloud synchronization
- Mobile app development

## 🤝 Contributing

This project demonstrates professional Python development practices suitable for:
- Portfolio projects
- Resume showcases
- Learning modern Python features
- Understanding software architecture
- Full-stack development examples

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

[Your Name] - Professional Python Developer

---

*Built with ❤️ using modern Python practices and Flask* 