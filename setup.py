#!/usr/bin/env python3
"""
Setup script for Professional Budget Tracker
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    return []

setup(
    name="professional-budget-tracker",
    version="1.0.0",
    author="[Your Name]",
    author_email="your.email@example.com",
    description="A comprehensive personal finance management system built with Python",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/professional-budget-tracker",
    py_modules=["budget_tracker"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "budget-tracker=budget_tracker:main",
        ],
    },
    keywords="budget, finance, personal, money, tracking, cli",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/professional-budget-tracker/issues",
        "Source": "https://github.com/yourusername/professional-budget-tracker",
        "Documentation": "https://github.com/yourusername/professional-budget-tracker#readme",
    },
) 