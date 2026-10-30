import pytest
import mongomock
from app import create_app

@pytest.fixture
def client():
    database = mongomock.MongoClient().test_database
    collection = database.transactions
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-budget-tracker-key",
        "TRANSACTIONS_COLLECTION": collection
    })
    with app.test_client() as test_client:
        yield test_client

def test_homepage(client):
    """Test that the homepage loads successfully with empty transactions."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Personal Budget Tracker" in response.data
    assert b"Remaining Balance" in response.data

def test_add_income(client):
    """Test adding an income transaction."""
    response = client.post("/add", data={
        "type": "income",
        "category": "Salary",
        "description": "Monthly Salary",
        "amount": "25000.00"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Income transaction added successfully." in response.data
    assert b"25000.00" in response.data
    assert b"Monthly Salary" in response.data

def test_add_expense(client):
    """Test adding an expense transaction."""
    response = client.post("/add", data={
        "type": "expense",
        "category": "Food",
        "description": "Grocery Shopping",
        "amount": "3500.00"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Expense transaction added successfully." in response.data
    assert b"3500.00" in response.data
    assert b"Grocery Shopping" in response.data

def test_balance_calculation(client):
    """Test balance and category aggregation with multiple transactions."""
    client.post("/add", data={
        "type": "income",
        "category": "Salary",
        "description": "Salary deposit",
        "amount": "10000.00"
    }, follow_redirects=True)

    client.post("/add", data={
        "type": "expense",
        "category": "Food",
        "description": "Lunch",
        "amount": "1500.00"
    }, follow_redirects=True)

    response = client.post("/add", data={
        "type": "expense",
        "category": "Travel",
        "description": "Metro pass",
        "amount": "500.00"
    }, follow_redirects=True)

    assert response.status_code == 200
    # Remaining Balance = 10000 - 2000 = 8000.00
    assert b"8000.00" in response.data
    # Category totals check
    assert b"Food" in response.data
    assert b"1500.00" in response.data
    assert b"Travel" in response.data
    assert b"500.00" in response.data

def test_invalid_amount_validation(client):
    """Test that zero or negative amounts are rejected."""
    response = client.post("/add", data={
        "type": "expense",
        "category": "Bills",
        "description": "Electricity",
        "amount": "-50.00"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Amount must be greater than zero." in response.data

def test_delete_transaction(client):
    """Test deleting an existing transaction."""
    client.post("/add", data={
        "type": "income",
        "category": "Salary",
        "description": "Bonus",
        "amount": "5000.00"
    }, follow_redirects=True)

    home_resp = client.get("/")
    assert b"Bonus" in home_resp.data

    collection = client.application.config["TRANSACTIONS_COLLECTION"]
    transaction = collection.find_one({"description": "Bonus"})
    assert transaction is not None

    del_resp = client.post(f"/delete/{transaction['_id']}", follow_redirects=True)
    assert del_resp.status_code == 200
    assert b"Transaction deleted successfully." in del_resp.data
    assert b"Bonus" not in del_resp.data

