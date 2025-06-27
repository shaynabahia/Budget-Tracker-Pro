#!/usr/bin/env python3
"""
Professional Budget Tracker Application
A comprehensive personal finance management system with data persistence,
categorization, reporting, and interactive CLI interface.

Author: [Your Name]
Version: 1.0.0
"""

import json
import os
import sys
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import locale
from pathlib import Path


class TransactionType(Enum):
    """Enumeration for transaction types."""
    EXPENSE = "expense"
    INCOME = "income"


class Category(Enum):
    """Predefined categories for transactions."""
    # Expense categories
    FOOD = "Food & Dining"
    TRANSPORTATION = "Transportation"
    HOUSING = "Housing"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    TRAVEL = "Travel"
    INSURANCE = "Insurance"
    TAXES = "Taxes"
    OTHER_EXPENSE = "Other Expense"
    
    # Income categories
    SALARY = "Salary"
    FREELANCE = "Freelance"
    INVESTMENT = "Investment"
    BUSINESS = "Business"
    OTHER_INCOME = "Other Income"


@dataclass
class Transaction:
    """Data class representing a financial transaction."""
    id: str
    name: str
    amount: float
    category: Category
    transaction_type: TransactionType
    date: date
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'category': self.category.value,
            'transaction_type': self.transaction_type.value,
            'date': self.date.isoformat(),
            'description': self.description,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """Create transaction from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            amount=data['amount'],
            category=Category(data['category']),
            transaction_type=TransactionType(data['transaction_type']),
            date=date.fromisoformat(data['date']),
            description=data.get('description'),
            tags=data.get('tags', [])
        )


class BudgetTracker:
    """Main budget tracking application class."""
    
    def __init__(self, data_file: str = "budget_data.json"):
        """Initialize the budget tracker."""
        self.data_file = Path(data_file)
        self.transactions: List[Transaction] = []
        self.load_data()
        
        # Set locale for currency formatting
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    def generate_id(self) -> str:
        """Generate a unique ID for transactions."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def add_transaction(self, name: str, amount: float, category: Category,
                       transaction_type: TransactionType, description: Optional[str] = None,
                       tags: Optional[List[str]] = None, transaction_date: Optional[date] = None) -> Transaction:
        """Add a new transaction to the tracker."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if transaction_date is None:
            transaction_date = date.today()
        
        transaction = Transaction(
            id=self.generate_id(),
            name=name,
            amount=amount,
            category=category,
            transaction_type=transaction_type,
            date=transaction_date,
            description=description,
            tags=tags or []
        )
        
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def remove_transaction(self, transaction_id: str) -> bool:
        """Remove a transaction by ID."""
        for i, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                removed = self.transactions.pop(i)
                self.save_data()
                return True
        return False
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a transaction by ID."""
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    
    def get_balance(self) -> float:
        """Calculate current balance (income - expenses)."""
        income = sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.INCOME)
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.EXPENSE)
        return income - expenses
    
    def get_total_income(self) -> float:
        """Calculate total income."""
        return sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.INCOME)
    
    def get_total_expenses(self) -> float:
        """Calculate total expenses."""
        return sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.EXPENSE)
    
    def get_transactions_by_category(self, category: Category) -> List[Transaction]:
        """Get all transactions for a specific category."""
        return [t for t in self.transactions if t.category == category]
    
    def get_transactions_by_date_range(self, start_date: date, end_date: date) -> List[Transaction]:
        """Get transactions within a date range."""
        return [t for t in self.transactions if start_date <= t.date <= end_date]
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get monthly summary for a specific month."""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        monthly_transactions = self.get_transactions_by_date_range(start_date, end_date)
        
        income = sum(t.amount for t in monthly_transactions if t.transaction_type == TransactionType.INCOME)
        expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == TransactionType.EXPENSE)
        
        category_totals = {}
        for transaction in monthly_transactions:
            if transaction.transaction_type == TransactionType.EXPENSE:
                category = transaction.category.value
                category_totals[category] = category_totals.get(category, 0) + transaction.amount
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses,
            'category_totals': category_totals,
            'transaction_count': len(monthly_transactions)
        }
    
    def save_data(self) -> None:
        """Save transactions to JSON file."""
        data = {
            'transactions': [t.to_dict() for t in self.transactions],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self) -> None:
        """Load transactions from JSON file."""
        if not self.data_file.exists():
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading data: {e}")
            self.transactions = []
    
    def export_to_csv(self, filename: str = "budget_export.csv") -> None:
        """Export transactions to CSV file."""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Name', 'Amount', 'Category', 'Type', 'Date', 'Description', 'Tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow({
                    'ID': transaction.id,
                    'Name': transaction.name,
                    'Amount': transaction.amount,
                    'Category': transaction.category.value,
                    'Type': transaction.transaction_type.value,
                    'Date': transaction.date.isoformat(),
                    'Description': transaction.description or '',
                    'Tags': ', '.join(transaction.tags or [])
                })


class BudgetTrackerCLI:
    """Command-line interface for the budget tracker."""
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.tracker = BudgetTracker()
        self.running = True
    
    def format_currency(self, amount: float) -> str:
        """Format amount as currency."""
        return locale.currency(amount, grouping=True)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("💰 PROFESSIONAL BUDGET TRACKER 💰")
        print("="*50)
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Balance Summary")
        print("4. View Monthly Summary")
        print("5. View Transactions by Category")
        print("6. Remove Transaction")
        print("7. Export to CSV")
        print("8. Exit")
        print("="*50)
    
    def get_category_choice(self) -> Category:
        """Get category choice from user."""
        print("\nAvailable Categories:")
        for i, category in enumerate(Category, 1):
            print(f"{i:2d}. {category.value}")
        
        while True:
            try:
                choice = int(input("\nSelect category (1-15): ")) - 1
                if 0 <= choice < len(Category):
                    return list(Category)[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def add_transaction_flow(self) -> None:
        """Handle adding a new transaction."""
        print("\n--- Add New Transaction ---")
        
        # Get transaction type
        print("Transaction Type:")
        print("1. Expense")
        print("2. Income")
        
        while True:
            try:
                type_choice = int(input("Select type (1-2): "))
                if type_choice in [1, 2]:
                    transaction_type = TransactionType.EXPENSE if type_choice == 1 else TransactionType.INCOME
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get transaction details
        name = input("Transaction name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        
        while True:
            try:
                amount = float(input("Amount: $"))
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except ValueError:
                print("Please enter a valid amount.")
        
        category = self.get_category_choice()
        description = input("Description (optional): ").strip() or None
        tags_input = input("Tags (comma-separated, optional): ").strip()
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        # Add transaction
        try:
            transaction = self.tracker.add_transaction(
                name=name,
                amount=amount,
                category=category,
                transaction_type=transaction_type,
                description=description,
                tags=tags
            )
            print(f"\n✅ Transaction added successfully!")
            print(f"ID: {transaction.id}")
            print(f"Name: {transaction.name}")
            print(f"Amount: {self.format_currency(transaction.amount)}")
            print(f"Category: {transaction.category.value}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def view_transactions(self) -> None:
        """Display all transactions."""
        if not self.tracker.transactions:
            print("\n📭 No transactions found.")
            return
        
        print(f"\n📋 All Transactions ({len(self.tracker.transactions)} total)")
        print("-" * 80)
        print(f"{'ID':<8} {'Date':<12} {'Type':<8} {'Category':<20} {'Amount':<12} {'Name'}")
        print("-" * 80)
        
        for transaction in sorted(self.tracker.transactions, key=lambda x: x.date, reverse=True):
            amount_str = self.format_currency(transaction.amount)
            type_icon = "💸" if transaction.transaction_type == TransactionType.EXPENSE else "💰"
            print(f"{transaction.id:<8} {transaction.date:<12} {type_icon:<8} "
                  f"{transaction.category.value:<20} {amount_str:<12} {transaction.name}")
    
    def view_balance_summary(self) -> None:
        """Display balance summary."""
        total_income = self.tracker.get_total_income()
        total_expenses = self.tracker.get_total_expenses()
        balance = self.tracker.get_balance()
        
        print("\n📊 Balance Summary")
        print("=" * 40)
        print(f"Total Income:    {self.format_currency(total_income)}")
        print(f"Total Expenses:  {self.format_currency(total_expenses)}")
        print("-" * 40)
        
        if balance >= 0:
            print(f"Net Balance:     💚 {self.format_currency(balance)}")
        else:
            print(f"Net Balance:     🔴 {self.format_currency(balance)}")
        
        if total_income > 0:
            savings_rate = ((total_income - total_expenses) / total_income) * 100
            print(f"Savings Rate:    {savings_rate:.1f}%")
    
    def view_monthly_summary(self) -> None:
        """Display monthly summary."""
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        
        # Allow user to select different month/year
        print(f"\n📅 Monthly Summary")
        print(f"Current: {current_date.strftime('%B %Y')}")
        
        try:
            year_input = input(f"Enter year ({year}): ").strip()
            if year_input:
                year = int(year_input)
            
            month_input = input(f"Enter month (1-12, {month}): ").strip()
            if month_input:
                month = int(month_input)
                if not (1 <= month <= 12):
                    raise ValueError("Month must be between 1 and 12")
        except ValueError as e:
            print(f"Invalid input: {e}")
            return
        
        summary = self.tracker.get_monthly_summary(year, month)
        
        print(f"\n📊 Summary for {date(year, month, 1).strftime('%B %Y')}")
        print("=" * 50)
        print(f"Income:          {self.format_currency(summary['income'])}")
        print(f"Expenses:        {self.format_currency(summary['expenses'])}")
        print(f"Balance:         {self.format_currency(summary['balance'])}")
        print(f"Transactions:    {summary['transaction_count']}")
        
        if summary['category_totals']:
            print("\n📈 Expenses by Category:")
            for category, amount in sorted(summary['category_totals'].items(), 
                                         key=lambda x: x[1], reverse=True):
                print(f"  {category:<20} {self.format_currency(amount)}")
    
    def view_transactions_by_category(self) -> None:
        """Display transactions grouped by category."""
        category = self.get_category_choice()
        transactions = self.tracker.get_transactions_by_category(category)
        
        if not transactions:
            print(f"\n📭 No transactions found for category: {category.value}")
            return
        
        total = sum(t.amount for t in transactions)
        print(f"\n📋 Transactions for {category.value} (Total: {self.format_currency(total)})")
        print("-" * 70)
        print(f"{'Date':<12} {'Type':<8} {'Amount':<12} {'Name'}")
        print("-" * 70)
        
        for transaction in sorted(transactions, key=lambda x: x.date, reverse=True):
            amount_str = self.format_currency(transaction.amount)
            type_icon = "💸" if transaction.transaction_type == TransactionType.EXPENSE else "💰"
            print(f"{transaction.date:<12} {type_icon:<8} {amount_str:<12} {transaction.name}")
    
    def remove_transaction_flow(self) -> None:
        """Handle removing a transaction."""
        if not self.tracker.transactions:
            print("\n📭 No transactions to remove.")
            return
        
        print("\n--- Remove Transaction ---")
        transaction_id = input("Enter transaction ID to remove: ").strip()
        
        if self.tracker.remove_transaction(transaction_id):
            print("✅ Transaction removed successfully!")
        else:
            print("❌ Transaction not found.")
    
    def export_to_csv_flow(self) -> None:
        """Handle CSV export."""
        filename = input("Enter filename for export (default: budget_export.csv): ").strip()
        if not filename:
            filename = "budget_export.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            self.tracker.export_to_csv(filename)
            print(f"✅ Data exported successfully to {filename}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def run(self) -> None:
        """Run the CLI application."""
        print("🚀 Starting Professional Budget Tracker...")
        
        while self.running:
            try:
                self.display_menu()
                choice = input("\nSelect an option (1-8): ").strip()
                
                if choice == '1':
                    self.add_transaction_flow()
                elif choice == '2':
                    self.view_transactions()
                elif choice == '3':
                    self.view_balance_summary()
                elif choice == '4':
                    self.view_monthly_summary()
                elif choice == '5':
                    self.view_transactions_by_category()
                elif choice == '6':
                    self.remove_transaction_flow()
                elif choice == '7':
                    self.export_to_csv_flow()
                elif choice == '8':
                    print("\n👋 Thank you for using Professional Budget Tracker!")
                    self.running = False
                else:
                    print("❌ Invalid choice. Please try again.")
                
                if self.running:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Main entry point of the application."""
    try:
        cli = BudgetTrackerCLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
