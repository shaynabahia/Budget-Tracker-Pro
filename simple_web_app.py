#!/usr/bin/env python3
"""
Professional Budget Tracker - Simple Web Application
A fully functional web interface using inline templates.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
import json
from datetime import date, datetime, timedelta
import locale
from pathlib import Path
import sys
import os

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

# HTML Templates
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Budget Tracker Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #f8f9fa; }
        .card { border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .income { color: #27ae60; }
        .expense { color: #e74c3c; }
        .navbar-brand { font-weight: bold; }
        .btn-primary { background: linear-gradient(135deg, #2c3e50, #3498db); border: none; }
        .btn-success { background: linear-gradient(135deg, #27ae60, #2ecc71); border: none; }
        .btn-danger { background: linear-gradient(135deg, #e74c3c, #c0392b); border: none; }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(135deg, #2c3e50, #3498db);">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-wallet me-2"></i>Budget Tracker Pro
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/"><i class="fas fa-home me-1"></i>Dashboard</a>
                <a class="nav-link" href="/transactions"><i class="fas fa-list me-1"></i>Transactions</a>
                <a class="nav-link" href="/add_transaction"><i class="fas fa-plus me-1"></i>Add Transaction</a>
                <a class="nav-link" href="/reports"><i class="fas fa-chart-bar me-1"></i>Reports</a>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="container mt-3">
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
'''

DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
        <!-- Page Header -->
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="display-4 text-primary">
                    <i class="fas fa-chart-line me-3"></i>Financial Dashboard
                </h1>
                <p class="lead text-muted">Track your income, expenses, and financial goals</p>
            </div>
        </div>

        <!-- Summary Cards -->
        <div class="row mb-4">
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-success text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">Total Income</h6>
                        <h3 class="mb-0">{{ format_currency(total_income) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-danger text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">Total Expenses</h6>
                        <h3 class="mb-0">{{ format_currency(total_expenses) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-primary text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">Net Balance</h6>
                        <h3 class="mb-0">{{ format_currency(balance) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-info text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">This Month</h6>
                        <h3 class="mb-0">{{ format_currency(monthly_summary.balance) }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="row mb-4">
            <div class="col-lg-8 mb-3">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Expenses by Category</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="categoryChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-3">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-chart-bar me-2"></i>Monthly Overview</h5>
                    </div>
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-6">
                                <h4 class="text-success">{{ format_currency(monthly_summary.income) }}</h4>
                                <small class="text-muted">Income</small>
                            </div>
                            <div class="col-6">
                                <h4 class="text-danger">{{ format_currency(monthly_summary.expenses) }}</h4>
                                <small class="text-muted">Expenses</small>
                            </div>
                        </div>
                        <hr>
                        <div class="text-center">
                            <h5 class="text-primary">{{ format_currency(monthly_summary.balance) }}</h5>
                            <small class="text-muted">Net Balance</small>
                        </div>
                        <hr>
                        <div class="text-center">
                            <h6>{{ monthly_summary.transaction_count }}</h6>
                            <small class="text-muted">Transactions</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Transactions -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0"><i class="fas fa-clock me-2"></i>Recent Transactions</h5>
                        <a href="/transactions" class="btn btn-sm btn-primary">
                            <i class="fas fa-list me-1"></i>View All
                        </a>
                    </div>
                    <div class="card-body">
                        {% if recent_transactions %}
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Name</th>
                                            <th>Category</th>
                                            <th>Type</th>
                                            <th>Amount</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for transaction in recent_transactions %}
                                        <tr>
                                            <td>{{ transaction.date.strftime('%Y-%m-%d') }}</td>
                                            <td>
                                                <strong>{{ transaction.name }}</strong>
                                                {% if transaction.description %}
                                                    <br><small class="text-muted">{{ transaction.description }}</small>
                                                {% endif %}
                                            </td>
                                            <td>
                                                <span class="badge bg-secondary">{{ transaction.category.value }}</span>
                                            </td>
                                            <td>
                                                <span class="{{ transaction.transaction_type.value }}">
                                                    <i class="fas fa-{{ 'arrow-up' if transaction.transaction_type.value == 'income' else 'arrow-down' }} me-1"></i>
                                                    {{ transaction.transaction_type.value.title() }}
                                                </span>
                                            </td>
                                            <td>
                                                <strong class="{{ transaction.transaction_type.value }}">
                                                    {{ format_currency(transaction.amount) }}
                                                </strong>
                                            </td>
                                            <td>
                                                <form method="POST" action="/delete_transaction/{{ transaction.id }}" 
                                                      style="display: inline;" 
                                                      onsubmit="return confirm('Are you sure you want to delete this transaction?')">
                                                    <button type="submit" class="btn btn-sm btn-outline-danger">
                                                        <i class="fas fa-trash"></i>
                                                    </button>
                                                </form>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% else %}
                            <div class="text-center py-4">
                                <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                                <h5 class="text-muted">No transactions yet</h5>
                                <p class="text-muted">Start by adding your first transaction!</p>
                                <a href="/add_transaction" class="btn btn-primary">
                                    <i class="fas fa-plus me-1"></i>Add Transaction
                                </a>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
''').replace('{% block scripts %}{% endblock %}', '''
    <script>
        // Category Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        const categoryData = {
            labels: [{% for category, amount in category_totals %}'{{ category }}'{% if not loop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                data: [{% for category, amount in category_totals %}{{ amount }}{% if not loop.last %}, {% endif %}{% endfor %}],
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384',
                    '#36A2EB', '#FFCE56'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        };

        new Chart(categoryCtx, {
            type: 'doughnut',
            data: categoryData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    </script>
''')

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
    
    return render_template_string(DASHBOARD_TEMPLATE,
                                title="Dashboard",
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
    
    # Create transactions template
    transactions_template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
        <!-- Page Header -->
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="display-4 text-primary">
                    <i class="fas fa-list me-3"></i>All Transactions
                </h1>
                <p class="lead text-muted">View and manage your financial transactions</p>
            </div>
        </div>

        <!-- Transactions Table -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="fas fa-table me-2"></i>Transactions
                            <span class="badge bg-primary ms-2">{{ transactions|length }}</span>
                        </h5>
                        <a href="/add_transaction" class="btn btn-success">
                            <i class="fas fa-plus me-1"></i>Add Transaction
                        </a>
                    </div>
                    <div class="card-body">
                        {% if transactions %}
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Name</th>
                                            <th>Category</th>
                                            <th>Type</th>
                                            <th>Amount</th>
                                            <th>Description</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for transaction in transactions %}
                                        <tr>
                                            <td>{{ transaction.date.strftime('%Y-%m-%d') }}</td>
                                            <td><strong>{{ transaction.name }}</strong></td>
                                            <td><span class="badge bg-secondary">{{ transaction.category.value }}</span></td>
                                            <td>
                                                <span class="{{ transaction.transaction_type.value }}">
                                                    <i class="fas fa-{{ 'arrow-up' if transaction.transaction_type.value == 'income' else 'arrow-down' }} me-1"></i>
                                                    {{ transaction.transaction_type.value.title() }}
                                                </span>
                                            </td>
                                            <td>
                                                <strong class="{{ transaction.transaction_type.value }}">
                                                    {{ format_currency(transaction.amount) }}
                                                </strong>
                                            </td>
                                            <td>
                                                {% if transaction.description %}
                                                    <small class="text-muted">{{ transaction.description }}</small>
                                                {% else %}
                                                    <span class="text-muted">-</span>
                                                {% endif %}
                                            </td>
                                            <td>
                                                <form method="POST" action="/delete_transaction/{{ transaction.id }}" 
                                                      style="display: inline;" 
                                                      onsubmit="return confirm('Are you sure you want to delete this transaction?')">
                                                    <button type="submit" class="btn btn-sm btn-outline-danger" title="Delete">
                                                        <i class="fas fa-trash"></i>
                                                    </button>
                                                </form>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% else %}
                            <div class="text-center py-5">
                                <i class="fas fa-inbox fa-4x text-muted mb-4"></i>
                                <h4 class="text-muted">No transactions found</h4>
                                <p class="text-muted">Add your first transaction to get started!</p>
                                <a href="/add_transaction" class="btn btn-primary">
                                    <i class="fas fa-plus me-1"></i>Add Your First Transaction
                                </a>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    ''')
    
    return render_template_string(transactions_template,
                                title="Transactions",
                                transactions=filtered_transactions,
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
    
    # Create add transaction template
    add_template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
        <!-- Page Header -->
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="display-4 text-primary">
                    <i class="fas fa-plus me-3"></i>Add New Transaction
                </h1>
                <p class="lead text-muted">Record your income or expense</p>
            </div>
        </div>

        <!-- Add Transaction Form -->
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-edit me-2"></i>Transaction Details</h5>
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/add_transaction">
                            <!-- Transaction Type -->
                            <div class="row mb-3">
                                <div class="col-12">
                                    <label class="form-label">Transaction Type <span class="text-danger">*</span></label>
                                    <div class="d-flex gap-3">
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="transaction_type" 
                                                   id="type_expense" value="expense" checked>
                                            <label class="form-check-label" for="type_expense">
                                                <i class="fas fa-arrow-down text-danger me-1"></i>Expense
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="transaction_type" 
                                                   id="type_income" value="income">
                                            <label class="form-check-label" for="type_income">
                                                <i class="fas fa-arrow-up text-success me-1"></i>Income
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Name and Amount -->
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label for="name" class="form-label">Transaction Name <span class="text-danger">*</span></label>
                                    <input type="text" class="form-control" id="name" name="name" 
                                           placeholder="e.g., Grocery Shopping" required>
                                </div>
                                <div class="col-md-6">
                                    <label for="amount" class="form-label">Amount <span class="text-danger">*</span></label>
                                    <div class="input-group">
                                        <span class="input-group-text">$</span>
                                        <input type="number" class="form-control" id="amount" name="amount" 
                                               placeholder="0.00" step="0.01" min="0.01" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Category -->
                            <div class="row mb-3">
                                <div class="col-12">
                                    <label for="category" class="form-label">Category <span class="text-danger">*</span></label>
                                    <select class="form-select" id="category" name="category" required>
                                        <option value="">Select a category...</option>
                                        <optgroup label="Expense Categories">
                                            <option value="Food & Dining">Food & Dining</option>
                                            <option value="Transportation">Transportation</option>
                                            <option value="Housing">Housing</option>
                                            <option value="Utilities">Utilities</option>
                                            <option value="Entertainment">Entertainment</option>
                                            <option value="Shopping">Shopping</option>
                                            <option value="Healthcare">Healthcare</option>
                                            <option value="Education">Education</option>
                                            <option value="Travel">Travel</option>
                                            <option value="Insurance">Insurance</option>
                                            <option value="Taxes">Taxes</option>
                                            <option value="Other Expense">Other Expense</option>
                                        </optgroup>
                                        <optgroup label="Income Categories">
                                            <option value="Salary">Salary</option>
                                            <option value="Freelance">Freelance</option>
                                            <option value="Investment">Investment</option>
                                            <option value="Business">Business</option>
                                            <option value="Other Income">Other Income</option>
                                        </optgroup>
                                    </select>
                                </div>
                            </div>

                            <!-- Description -->
                            <div class="row mb-3">
                                <div class="col-12">
                                    <label for="description" class="form-label">Description</label>
                                    <textarea class="form-control" id="description" name="description" rows="3" 
                                              placeholder="Optional description of the transaction..."></textarea>
                                </div>
                            </div>

                            <!-- Tags -->
                            <div class="row mb-3">
                                <div class="col-12">
                                    <label for="tags" class="form-label">Tags</label>
                                    <input type="text" class="form-control" id="tags" name="tags" 
                                           placeholder="e.g., groceries, weekly, essential (comma-separated)">
                                    <div class="form-text">Add tags to help organize your transactions (optional)</div>
                                </div>
                            </div>

                            <!-- Submit Buttons -->
                            <div class="row">
                                <div class="col-12">
                                    <div class="d-flex gap-2">
                                        <button type="submit" class="btn btn-primary">
                                            <i class="fas fa-save me-1"></i>Save Transaction
                                        </button>
                                        <a href="/transactions" class="btn btn-outline-secondary">
                                            <i class="fas fa-times me-1"></i>Cancel
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    ''')
    
    return render_template_string(add_template, title="Add Transaction")

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
    """Reports page - simplified version."""
    # Get current month summary
    current_date = date.today()
    monthly_summary = tracker.get_monthly_summary(current_date.year, current_date.month)
    
    # Get category breakdown
    category_totals = {}
    for transaction in tracker.transactions:
        if transaction.transaction_type == TransactionType.EXPENSE:
            category = transaction.category.value
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
    
    # Create simple reports template
    reports_template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
        <!-- Page Header -->
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="display-4 text-primary">
                    <i class="fas fa-chart-bar me-3"></i>Financial Reports
                </h1>
                <p class="lead text-muted">Analyze your spending patterns and financial trends</p>
            </div>
        </div>

        <!-- Monthly Summary Cards -->
        <div class="row mb-4">
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-success text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">This Month Income</h6>
                        <h3 class="mb-0">{{ format_currency(monthly_summary.income) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-danger text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">This Month Expenses</h6>
                        <h3 class="mb-0">{{ format_currency(monthly_summary.expenses) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-primary text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">This Month Balance</h6>
                        <h3 class="mb-0">{{ format_currency(monthly_summary.balance) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-3">
                <div class="card bg-info text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">Transactions</h6>
                        <h3 class="mb-0">{{ monthly_summary.transaction_count }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Category Breakdown -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-list me-2"></i>Expense Breakdown by Category</h5>
                    </div>
                    <div class="card-body">
                        {% if category_totals %}
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Category</th>
                                            <th>Amount</th>
                                            <th>Percentage</th>
                                            <th>Progress Bar</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% set total_expenses = category_totals | map(attribute=1) | sum %}
                                        {% for category, amount in category_totals %}
                                        <tr>
                                            <td><strong>{{ category }}</strong></td>
                                            <td><strong>{{ format_currency(amount) }}</strong></td>
                                            <td><span class="badge bg-primary">{{ "%.1f"|format((amount / total_expenses) * 100) }}%</span></td>
                                            <td>
                                                <div class="progress" style="height: 20px;">
                                                    <div class="progress-bar" role="progressbar" 
                                                         style="width: {{ (amount / total_expenses) * 100 }}%"
                                                         aria-valuenow="{{ (amount / total_expenses) * 100 }}" 
                                                         aria-valuemin="0" aria-valuemax="100">
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% else %}
                            <div class="text-center py-4">
                                <i class="fas fa-chart-pie fa-3x text-muted mb-3"></i>
                                <h5 class="text-muted">No expense data available</h5>
                                <p class="text-muted">Add some transactions to see your spending breakdown.</p>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    ''')
    
    return render_template_string(reports_template,
                                title="Reports",
                                monthly_summary=monthly_summary,
                                category_totals=category_totals,
                                format_currency=format_currency)

if __name__ == '__main__':
    print("🚀 Starting Professional Budget Tracker Web Application...")
    print("📱 Open your browser to: http://127.0.0.1:8080")
    print("💡 Full-featured web interface with all budget tracking capabilities!")
    app.run(debug=True, host='127.0.0.1', port=8080) 