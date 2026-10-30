import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId

CATEGORIES = [
    "Food", "Travel", "Shopping", "Education",
    "Entertainment", "Bills", "Healthcare", "Other"
]

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "budget-tracker-dev-key")

    if test_config:
        app.config.update(test_config)
        collection = app.config["TRANSACTIONS_COLLECTION"]
    else:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        collection = client["personal_budget"]["transactions"]
        app.config["TRANSACTIONS_COLLECTION"] = collection

    @app.route("/")
    def index():
        transactions = list(collection.find().sort("_id", -1))
        total_income = sum(
            float(t["amount"]) for t in transactions if t.get("type") == "income"
        )
        total_expenses = sum(
            float(t["amount"]) for t in transactions if t.get("type") == "expense"
        )
        balance = total_income - total_expenses

        # Category-wise expenses calculation
        category_totals = {}
        for t in transactions:
            if t.get("type") == "expense":
                cat = t.get("category", "Other")
                category_totals[cat] = category_totals.get(cat, 0.0) + float(t["amount"])

        return render_template(
            "index.html",
            transactions=transactions,
            total_income=total_income,
            total_expenses=total_expenses,
            balance=balance,
            categories=CATEGORIES,
            category_totals=category_totals
        )

    @app.route("/add", methods=["POST"])
    def add_transaction():
        t_type = request.form.get("type")
        category = request.form.get("category")
        description = request.form.get("description", "").strip()
        amount_str = request.form.get("amount")

        if not t_type or not category or not amount_str:
            flash("Please provide all required fields.", "error")
            return redirect(url_for("index"))

        try:
            amount = float(amount_str)
            if amount <= 0:
                flash("Amount must be greater than zero.", "error")
                return redirect(url_for("index"))
        except ValueError:
            flash("Invalid amount entered. Please enter a valid number.", "error")
            return redirect(url_for("index"))

        doc = {
            "type": t_type,
            "category": category,
            "description": description or "No description",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        collection.insert_one(doc)
        flash(f"{t_type.capitalize()} transaction added successfully.", "success")
        return redirect(url_for("index"))

    @app.route("/delete/<transaction_id>", methods=["POST"])
    def delete_transaction(transaction_id):
        try:
            collection.delete_one({"_id": ObjectId(transaction_id)})
            flash("Transaction deleted successfully.", "success")
        except Exception as e:
            flash(f"Error deleting transaction: {str(e)}", "error")
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

