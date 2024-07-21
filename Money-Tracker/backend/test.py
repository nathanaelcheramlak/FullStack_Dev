# test.py
from config import db, app
from models.user import User
from models.transaction import Transaction
from models import DBStorage

# Initialize storage
storage = DBStorage()

# Add a user and a transaction within the same session
with app.app_context():
    new_user = User(email="newtest3@example.com", full_name="Test User", password="password")
    storage.new(new_user)
    storage.save()

    new_transaction = Transaction(user_id=new_user.id, name="Test Transaction", amount=100.0, description="Test Description", date="2024-07-19T00:00:00")
    storage.new(new_transaction)
    storage.save()

# Retrieve the user and their transactions within the same session
with app.app_context():
    user = storage.get('User', new_user.id)
    if user:
        # Ensure the user is associated with the session
        db.session.add(user)
        db.session.refresh(user)
        
        print(f"User found: {user.full_name}")
        print("Transactions:")
        for transaction in user.transactions:
            print(f"  - {transaction.name}: {transaction.amount}")
    else:
        print("User not found")
