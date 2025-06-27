#!/usr/bin/env python3
"""
Demo data script for the web application
Adds sample transactions to demonstrate the web interface.
"""

import sys
import os
from datetime import date, timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the budget tracker classes
exec(open('budget-tracker.py').read())

def add_demo_data():
    """Add sample transactions to demonstrate the web interface."""
    tracker = BudgetTracker("web_budget_data.json")
    
    # Clear existing data
    tracker.transactions = []
    
    # Sample income transactions
    income_transactions = [
        ("Monthly Salary", 5000.00, Category.SALARY, "Primary job income"),
        ("Freelance Project", 1200.00, Category.FREELANCE, "Web development project"),
        ("Investment Dividends", 150.00, Category.INVESTMENT, "Stock dividends"),
        ("Side Business", 800.00, Category.BUSINESS, "Online store sales"),
    ]
    
    # Sample expense transactions
    expense_transactions = [
        ("Grocery Shopping", 120.50, Category.FOOD, "Weekly groceries"),
        ("Gas Station", 45.00, Category.TRANSPORTATION, "Fuel for car"),
        ("Rent Payment", 1800.00, Category.HOUSING, "Monthly rent"),
        ("Electric Bill", 85.00, Category.UTILITIES, "Electricity bill"),
        ("Netflix Subscription", 15.99, Category.ENTERTAINMENT, "Streaming service"),
        ("Coffee Shop", 4.50, Category.FOOD, "Morning coffee"),
        ("Amazon Purchase", 67.25, Category.SHOPPING, "Books and supplies"),
        ("Doctor Visit", 25.00, Category.HEALTHCARE, "Co-pay for checkup"),
        ("Online Course", 199.00, Category.EDUCATION, "Python programming course"),
        ("Weekend Trip", 350.00, Category.TRAVEL, "Hotel and food"),
        ("Car Insurance", 120.00, Category.INSURANCE, "Monthly premium"),
        ("Restaurant Dinner", 45.75, Category.FOOD, "Date night"),
        ("Gym Membership", 50.00, Category.HEALTHCARE, "Monthly gym fee"),
        ("Movie Tickets", 24.00, Category.ENTERTAINMENT, "Weekend movie"),
        ("Home Depot", 89.99, Category.SHOPPING, "Home improvement supplies"),
    ]
    
    # Add income transactions (spread over the last 3 months)
    for i, (name, amount, category, description) in enumerate(income_transactions):
        transaction_date = date.today() - timedelta(days=30 * (i % 3))
        tracker.add_transaction(
            name=name,
            amount=amount,
            category=category,
            transaction_type=TransactionType.INCOME,
            description=description,
            tags=["income", "monthly"] if category == Category.SALARY else ["income"],
            transaction_date=transaction_date
        )
    
    # Add expense transactions (spread over the last 2 months)
    for i, (name, amount, category, description) in enumerate(expense_transactions):
        transaction_date = date.today() - timedelta(days=15 * (i % 4))
        tracker.add_transaction(
            name=name,
            amount=amount,
            category=category,
            transaction_type=TransactionType.EXPENSE,
            description=description,
            tags=["essential"] if category in [Category.HOUSING, Category.UTILITIES, Category.FOOD] else ["discretionary"],
            transaction_date=transaction_date
        )
    
    # Save the data
    tracker.save_data()
    
    print("✅ Demo data added successfully!")
    print(f"📊 Total transactions: {len(tracker.transactions)}")
    print(f"💰 Total income: ${tracker.get_total_income():,.2f}")
    print(f"💸 Total expenses: ${tracker.get_total_expenses():,.2f}")
    print(f"💳 Net balance: ${tracker.get_balance():,.2f}")
    print("\n🚀 You can now run the web application and see the data!")

if __name__ == "__main__":
    add_demo_data() 