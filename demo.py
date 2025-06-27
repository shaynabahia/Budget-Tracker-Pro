#!/usr/bin/env python3
"""
Demo script for the Professional Budget Tracker
This script demonstrates the core functionality with sample data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the classes from the main budget tracker file
exec(open('budget-tracker.py').read())

from datetime import date, timedelta


def run_demo():
    """Run a demonstration of the budget tracker features."""
    print("🚀 Professional Budget Tracker - Demo Mode")
    print("=" * 50)
    
    # Initialize tracker
    tracker = BudgetTracker("demo_data.json")
    
    # Add sample transactions
    print("\n📝 Adding sample transactions...")
    
    # Income transactions
    tracker.add_transaction(
        name="Monthly Salary",
        amount=5000.00,
        category=Category.SALARY,
        transaction_type=TransactionType.INCOME,
        description="Regular monthly salary payment",
        tags=["salary", "monthly"]
    )
    
    tracker.add_transaction(
        name="Freelance Project",
        amount=1200.00,
        category=Category.FREELANCE,
        transaction_type=TransactionType.INCOME,
        description="Web development project",
        tags=["freelance", "web-dev"]
    )
    
    # Expense transactions
    tracker.add_transaction(
        name="Grocery Shopping",
        amount=150.00,
        category=Category.FOOD,
        transaction_type=TransactionType.EXPENSE,
        description="Weekly groceries",
        tags=["groceries", "weekly"]
    )
    
    tracker.add_transaction(
        name="Gas Station",
        amount=45.00,
        category=Category.TRANSPORTATION,
        transaction_type=TransactionType.EXPENSE,
        description="Fuel for car",
        tags=["gas", "transport"]
    )
    
    tracker.add_transaction(
        name="Netflix Subscription",
        amount=15.99,
        category=Category.ENTERTAINMENT,
        transaction_type=TransactionType.EXPENSE,
        description="Monthly streaming service",
        tags=["entertainment", "subscription"]
    )
    
    tracker.add_transaction(
        name="Electric Bill",
        amount=89.50,
        category=Category.UTILITIES,
        transaction_type=TransactionType.EXPENSE,
        description="Monthly electricity bill",
        tags=["utilities", "monthly"]
    )
    
    tracker.add_transaction(
        name="Restaurant Dinner",
        amount=65.00,
        category=Category.FOOD,
        transaction_type=TransactionType.EXPENSE,
        description="Dinner with friends",
        tags=["dining", "social"]
    )
    
    print("✅ Sample transactions added successfully!")
    
    # Display summary
    print("\n📊 Current Financial Summary")
    print("=" * 40)
    print(f"Total Income:    ${tracker.get_total_income():,.2f}")
    print(f"Total Expenses:  ${tracker.get_total_expenses():,.2f}")
    print(f"Net Balance:     ${tracker.get_balance():,.2f}")
    
    # Show transactions by category
    print("\n📈 Expenses by Category:")
    print("-" * 30)
    for category in Category:
        if category.value in ["Food & Dining", "Transportation", "Entertainment", "Utilities"]:
            transactions = tracker.get_transactions_by_category(category)
            if transactions:
                total = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)
                print(f"{category.value:<20} ${total:,.2f}")
    
    # Monthly summary
    current_date = date.today()
    monthly_summary = tracker.get_monthly_summary(current_date.year, current_date.month)
    
    print(f"\n📅 Monthly Summary ({current_date.strftime('%B %Y')})")
    print("=" * 40)
    print(f"Income:          ${monthly_summary['income']:,.2f}")
    print(f"Expenses:        ${monthly_summary['expenses']:,.2f}")
    print(f"Balance:         ${monthly_summary['balance']:,.2f}")
    print(f"Transactions:    {monthly_summary['transaction_count']}")
    
    # Export to CSV
    print("\n💾 Exporting data to CSV...")
    tracker.export_to_csv("demo_export.csv")
    print("✅ Data exported to demo_export.csv")
    
    print("\n🎉 Demo completed successfully!")
    print("You can now run 'python budget-tracker.py' to use the interactive interface.")
    print("Or check the generated files:")
    print("- demo_data.json (transaction data)")
    print("- demo_export.csv (exported data)")


if __name__ == "__main__":
    run_demo() 