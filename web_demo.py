#!/usr/bin/env python3
"""
Simple Web Demo for Budget Tracker
This demonstrates the web interface capabilities.
"""

from flask import Flask, render_template_string, request, redirect, url_for
import json
from datetime import date, datetime
import locale

app = Flask(__name__)
app.secret_key = 'demo-key'

# Sample data for demo
sample_transactions = [
    {
        'id': 'abc123',
        'name': 'Grocery Shopping',
        'amount': 150.00,
        'category': 'Food & Dining',
        'type': 'expense',
        'date': '2024-01-15',
        'description': 'Weekly groceries'
    },
    {
        'id': 'def456',
        'name': 'Salary Payment',
        'amount': 5000.00,
        'category': 'Salary',
        'type': 'income',
        'date': '2024-01-01',
        'description': 'Monthly salary'
    },
    {
        'id': 'ghi789',
        'name': 'Gas Station',
        'amount': 45.00,
        'category': 'Transportation',
        'type': 'expense',
        'date': '2024-01-14',
        'description': 'Fuel for car'
    }
]

def format_currency(amount):
    """Format amount as currency."""
    try:
        return locale.currency(amount, grouping=True)
    except:
        return f"${amount:,.2f}"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Budget Tracker Pro - Web Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .income { color: #27ae60; }
        .expense { color: #e74c3c; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-wallet me-2"></i>Budget Tracker Pro - Web Demo
            </span>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <h1 class="display-4 text-primary">
                    <i class="fas fa-chart-line me-3"></i>Financial Dashboard
                </h1>
                <p class="lead text-muted">Professional Budget Tracker with Web Interface</p>
            </div>
        </div>

        <!-- Summary Cards -->
        <div class="row mb-4">
            <div class="col-md-4 mb-3">
                <div class="card bg-success text-white">
                    <div class="card-body text-center">
                        <h5>Total Income</h5>
                        <h3>{{ format_currency(total_income) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card bg-danger text-white">
                    <div class="card-body text-center">
                        <h5>Total Expenses</h5>
                        <h3>{{ format_currency(total_expenses) }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card bg-primary text-white">
                    <div class="card-body text-center">
                        <h5>Net Balance</h5>
                        <h3>{{ format_currency(balance) }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Transactions Table -->
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0"><i class="fas fa-list me-2"></i>Sample Transactions</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>Date</th>
                                <th>Name</th>
                                <th>Category</th>
                                <th>Type</th>
                                <th>Amount</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for transaction in transactions %}
                            <tr>
                                <td>{{ transaction.date }}</td>
                                <td><strong>{{ transaction.name }}</strong></td>
                                <td><span class="badge bg-secondary">{{ transaction.category }}</span></td>
                                <td>
                                    <span class="{{ transaction.type }}">
                                        <i class="fas fa-{{ 'arrow-up' if transaction.type == 'income' else 'arrow-down' }} me-1"></i>
                                        {{ transaction.type.title() }}
                                    </span>
                                </td>
                                <td><strong class="{{ transaction.type }}">{{ format_currency(transaction.amount) }}</strong></td>
                                <td><small class="text-muted">{{ transaction.description }}</small></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Features Demo -->
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-star me-2"></i>Key Features</h6>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>Income & Expense Tracking</li>
                            <li><i class="fas fa-check text-success me-2"></i>Category Management</li>
                            <li><i class="fas fa-check text-success me-2"></i>Data Persistence (JSON)</li>
                            <li><i class="fas fa-check text-success me-2"></i>Monthly Reports</li>
                            <li><i class="fas fa-check text-success me-2"></i>CSV Export</li>
                            <li><i class="fas fa-check text-success me-2"></i>Tagging System</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-code me-2"></i>Technical Highlights</h6>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-primary me-2"></i>Object-Oriented Design</li>
                            <li><i class="fas fa-check text-primary me-2"></i>Type Hints & Data Classes</li>
                            <li><i class="fas fa-check text-primary me-2"></i>Modern Python Practices</li>
                            <li><i class="fas fa-check text-primary me-2"></i>Error Handling</li>
                            <li><i class="fas fa-check text-primary me-2"></i>Responsive Web UI</li>
                            <li><i class="fas fa-check text-primary me-2"></i>Professional Documentation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- Call to Action -->
        <div class="text-center mt-4">
            <div class="alert alert-info">
                <h5><i class="fas fa-info-circle me-2"></i>This is a Web Demo</h5>
                <p class="mb-0">The full application includes a complete CLI interface and comprehensive web interface with charts, filtering, and data management.</p>
            </div>
            <a href="#" class="btn btn-primary btn-lg">
                <i class="fas fa-download me-2"></i>Download Full Application
            </a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    """Demo dashboard."""
    total_income = sum(t['amount'] for t in sample_transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in sample_transactions if t['type'] == 'expense')
    balance = total_income - total_expenses
    
    return render_template_string(HTML_TEMPLATE,
                                transactions=sample_transactions,
                                total_income=total_income,
                                total_expenses=total_expenses,
                                balance=balance,
                                format_currency=format_currency)

if __name__ == '__main__':
    print("🚀 Starting Budget Tracker Web Demo...")
    print("📱 Open your browser to: http://127.0.0.1:8080")
    print("💡 This is a demo - the full app has complete functionality!")
    app.run(debug=True, host='127.0.0.1', port=8080) 