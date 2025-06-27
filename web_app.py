#!/usr/bin/env python3
"""
Professional Budget Tracker - Full Web Application
A complete web interface for the budget tracker with all functionality.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import json
from datetime import date, datetime, timedelta
import locale
from pathlib import Path
import sys
import os
import uuid

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the budget tracker classes by executing the main file
exec(open('budget-tracker.py').read())

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize the budget tracker
tracker = BudgetTracker("web_budget_data.json")

def format_currency(amount):
    """Format amount as currency."""
    try:
        return locale.currency(amount, grouping=True)
    except:
        return f"${amount:,.2f}"

@app.route('/')
def index():
    """Main dashboard page."""
    # Get summary data
    total_income = tracker.get_total_income()
    total_expenses = tracker.get_total_expenses()
    balance = tracker.get_balance()
    
    # Get recent transactions (last 10)
    recent_transactions = sorted(tracker.transactions, key=lambda x: x.date, reverse=True)[:10]
    
    # Get monthly summary for current month
    current_date = date.today()
    monthly_summary = tracker.get_monthly_summary(current_date.year, current_date.month)
    
    # Get category breakdown for expenses
    category_totals = {}
    for transaction in tracker.transactions:
        if transaction.transaction_type == TransactionType.EXPENSE:
            category = transaction.category.value
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
    
    # Sort categories by amount
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    
    return render_template('index.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance,
                         recent_transactions=recent_transactions,
                         monthly_summary=monthly_summary,
                         category_totals=sorted_categories,
                         format_currency=format_currency)

@app.route('/transactions')
def transactions():
    """Transactions page."""
    # Get filter parameters
    category_filter = request.args.get('category', '')
    type_filter = request.args.get('type', '')
    
    # Filter transactions
    filtered_transactions = tracker.transactions
    
    if category_filter:
        try:
            category = Category(category_filter)
            filtered_transactions = [t for t in filtered_transactions if t.category == category]
        except ValueError:
            pass
    
    if type_filter:
        try:
            transaction_type = TransactionType(type_filter)
            filtered_transactions = [t for t in filtered_transactions if t.transaction_type == transaction_type]
        except ValueError:
            pass
    
    # Sort by date (newest first)
    filtered_transactions = sorted(filtered_transactions, key=lambda x: x.date, reverse=True)
    
    return render_template('transactions.html',
                         transactions=filtered_transactions,
                         categories=Category,
                         transaction_types=TransactionType,
                         format_currency=format_currency)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add transaction page."""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name'].strip()
            amount = float(request.form['amount'])
            category = Category(request.form['category'])
            transaction_type = TransactionType(request.form['transaction_type'])
            description = request.form.get('description', '').strip() or None
            tags_input = request.form.get('tags', '').strip()
            tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
            
            # Validate
            if not name:
                flash('Transaction name is required', 'error')
                return redirect(url_for('add_transaction'))
            
            if amount <= 0:
                flash('Amount must be positive', 'error')
                return redirect(url_for('add_transaction'))
            
            # Add transaction
            transaction = tracker.add_transaction(
                name=name,
                amount=amount,
                category=category,
                transaction_type=transaction_type,
                description=description,
                tags=tags
            )
            
            flash(f'Transaction "{name}" added successfully!', 'success')
            return redirect(url_for('transactions'))
            
        except (ValueError, KeyError) as e:
            flash(f'Error adding transaction: {str(e)}', 'error')
            return redirect(url_for('add_transaction'))
    
    return render_template('add_transaction.html',
                         categories=Category,
                         transaction_types=TransactionType)

@app.route('/delete_transaction/<transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Delete a transaction."""
    if tracker.remove_transaction(transaction_id):
        flash('Transaction deleted successfully!', 'success')
    else:
        flash('Transaction not found!', 'error')
    
    return redirect(url_for('transactions'))

@app.route('/reports')
def reports():
    """Reports page."""
    # Get current month summary
    current_date = date.today()
    monthly_summary = tracker.get_monthly_summary(current_date.year, current_date.month)
    
    # Get category breakdown
    category_totals = {}
    for transaction in tracker.transactions:
        if transaction.transaction_type == TransactionType.EXPENSE:
            category = transaction.category.value
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
    
    # Get monthly data for the last 6 months
    monthly_data = []
    for i in range(6):
        month = current_date.month - i
        year = current_date.year
        if month <= 0:
            month += 12
            year -= 1
        
        summary = tracker.get_monthly_summary(year, month)
        monthly_data.append({
            'month': f"{date(year, month, 1).strftime('%B %Y')}",
            'income': summary['income'],
            'expenses': summary['expenses'],
            'balance': summary['balance']
        })
    
    monthly_data.reverse()  # Show oldest to newest
    
    return render_template('reports.html',
                         monthly_summary=monthly_summary,
                         category_totals=category_totals,
                         monthly_data=monthly_data,
                         format_currency=format_currency)

@app.route('/api/export_csv')
def export_csv():
    """Export data to CSV."""
    try:
        filename = f"budget_export_{date.today().strftime('%Y%m%d')}.csv"
        tracker.export_to_csv(filename)
        flash(f'Data exported to {filename}', 'success')
    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
    
    return redirect(url_for('reports'))

@app.route('/api/transaction/<transaction_id>')
def get_transaction(transaction_id):
    """Get transaction details via API."""
    transaction = tracker.get_transaction(transaction_id)
    if transaction:
        return jsonify({
            'id': transaction.id,
            'name': transaction.name,
            'amount': transaction.amount,
            'category': transaction.category.value,
            'transaction_type': transaction.transaction_type.value,
            'date': transaction.date.isoformat(),
            'description': transaction.description,
            'tags': transaction.tags
        })
    return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/summary')
def get_summary():
    """Get financial summary via API."""
    return jsonify({
        'total_income': tracker.get_total_income(),
        'total_expenses': tracker.get_total_expenses(),
        'balance': tracker.get_balance(),
        'transaction_count': len(tracker.transactions)
    })

@app.route('/api/categories')
def get_categories():
    """Get category breakdown via API."""
    category_totals = {}
    for transaction in tracker.transactions:
        if transaction.transaction_type == TransactionType.EXPENSE:
            category = transaction.category.value
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
    
    return jsonify(category_totals)

if __name__ == '__main__':
    print("🚀 Starting Professional Budget Tracker Web Application...")
    print("📱 Open your browser to: http://127.0.0.1:8080")
    print("💡 Full-featured web interface with all budget tracking capabilities!")
    app.run(debug=True, host='127.0.0.1', port=8080) 