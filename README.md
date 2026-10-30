# budget

A lightweight, automated Personal Budget Tracker web application built using Python Flask and MongoDB, with automated CI/CD pipeline automation powered by Jenkins.

## Features
- **Income & Expense Tracking**: Quickly log daily earnings and expenditures.
- **Categorization**: Organize expenses into Food, Travel, Shopping, Education, Entertainment, Bills, Healthcare, and Other.
- **Live Summary**: Real-time display of Total Income, Total Expenses, and Remaining Balance.
- **Category Breakdown**: Aggregated view of expense totals per category.
- **Transaction History**: View full history with single-click delete.
- **Automated Testing**: 100% test coverage using Pytest and Mongomock.
- **CI/CD Pipeline**: Automated checkout, environment check, dependency installation, testing, and verification using Jenkins.

## Tech Stack
- **Backend**: Python 3.13, Flask 3.1
- **Database**: MongoDB 8.0 / PyMongo
- **Frontend**: HTML5, CSS3 (Modern responsive UI)
- **Automated Tests**: Pytest, Mongomock
- **CI/CD Automation**: Jenkins Declarative Pipeline
- **Version Control**: Git & GitHub

## Quick Start (Local Run)

1. **Activate Virtual Environment**:
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run Automated Tests**:
   ```powershell
   python -m pytest -v
   ```

4. **Start the Application**:
   ```powershell
   python app.py
   ```
   Open your browser at `http://127.0.0.1:5000`.

## CI/CD Pipeline (Jenkins)
The automated pipeline executes the following stages on every Git push:
1. **Checkout**: Pulls latest source code from GitHub `main` branch.
2. **Environment Check**: Verifies Python and pip versions on the build agent.
3. **Install Dependencies**: Installs packages from `requirements.txt`.
4. **Automated Tests**: Executes Pytest test suite. Halts pipeline if any test fails.
5. **Application Verification**: Verifies application module import and syntax integrity.
6. **Post Actions**: Reports execution success or failure.
