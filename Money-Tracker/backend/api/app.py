from flask import request, jsonify
from config import db, app
from models import storage

from models.user import User
from models.transaction import Transaction

# Hash Password
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

# Helper function for common error handling
def handle_error(message, status_code=400):
    return jsonify({"error": message}), status_code

# Get Users or a Single User
# Update User Balance
@app.route('/api/v1/users', methods=['GET'])
@app.route('/api/v1/users/<user_id>', methods=['GET', 'PATCH', 'DELETE'])
def users(user_id=None):
    if request.method == 'GET':
        if user_id:
            user = storage.get('User', user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify(user.to_dict()), 200
        else:
            all_users = storage.all('User')
            users = [user.to_dict() for user in all_users.values()]
            return jsonify(users)
    
    elif request.method == 'PATCH':
        if not user_id:
            return jsonify({"error": "User ID is required for updating"}), 400
        
        data = request.get_json()
        balance = data.get('balance')

        if balance is None:
            return jsonify({"error": "Missing balance"}), 400
        
        user = storage.get('User', user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.balance = balance

        try:
            user.save_to_db()
        except:
            return jsonify({"error": "Could not update user"}), 400
        
        return jsonify({"message": "Updated Successfully"}), 200
    
    elif request.method == 'DELETE':
        if not user_id:
            return jsonify({"error": "User ID is required for updating"}), 400
        
        user = storage.get('User', id=user_id)

        try:
            user.delete()
        except:
            return jsonify({"error":"Could not delete user"}), 400
        
        return jsonify({"message": "User Deleted"}), 200
    
    return handle_error("Method not allowed", 405)

# Register User
@app.route('/api/v1/users/sign_up', methods=['POST'])
def create_user():
    data = request.get_json()

    email = data.get('email')
    full_name = data.get('fullName')
    password = data.get('password')
    dob = data.get('DOB')
    balance = 0

    if not email or not full_name or not password or not dob:
        return handle_error("Missing data")
    # Checks if the user already exists
    if storage.get('User', email=email):
        return handle_error("User already exists", 400)
    
    hashed_password = generate_password_hash(password)
    
    new_user = User(email=email, full_name=full_name, password=hashed_password, dob=dob, balance=balance)

    try:
        new_user.save_to_db()
    except Exception as e:
        return handle_error(f"Could not create user: {str(e)}")
    
    return jsonify(new_user.to_dict()), 201

# Login User
@app.route('/api/v1/users/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return handle_error("Missing data")
    
    user = storage.get('User', email=email)
    if not user:
        return handle_error("No Account found, Register now", 404)
    
    if not check_password_hash(user.password, password):
        return handle_error("Invalid email or password", 401)
    
    return jsonify(user.to_dict()), 200

# Update User Password and Name
@app.route('/api/v1/users/<user_id>/update', methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()

    user = storage.get('User', user_id)

    name = data.get('name')
    email = data.get('email')
    new_password = data.get('newPassword')

    if not name or not email or not new_password:
        handle_error("Missing data")

    user.name = name
    user.email = email
    user.password = generate_password_hash(new_password)

    try:
        user.save_to_db()
    except Exception as e:
        return handle_error(f"Could not update user: {str(e)}")
    return jsonify(user.to_dict()), 200
    
# Get Transaction
@app.route('/api/v1/users/<user_id>/transaction/<transaction_id>', methods=["GET"])
@app.route('/api/v1/users/<user_id>/transaction', methods=["GET"])
def get_user_transactions(user_id, transaction_id=None):
    if request.method == 'GET':
        if not transaction_id:
            user = storage.get('User', user_id)

            if not user:
                return jsonify({"error":"User not found"}), 404
            
            transactions = user.transactions
            user_transactions = []

            posetive_transactions = 0
            negative_transactions = 0

            for transaction in transactions:
                if transaction.amount >= 0:
                    posetive_transactions += 1
                else: 
                    negative_transactions += 1
                user_transactions.append(transaction.to_dict())
            
            return jsonify({"total": len(transactions), "posetive_transactions": posetive_transactions, "negative_transactions": negative_transactions,"transactions":user_transactions}), 200
        
        else: # Get Single Transaction
            user = storage.get('User', user_id)
            if not user:
                return jsonify({"error":"User not found"}), 404
            
            transaction = storage.get('Transaction', transaction_id)
            if not transaction:
                return jsonify({"error":"Transaction not found"}), 404
            
            return jsonify(transaction.to_dict()), 200
        
# Add Transaction
@app.route('/api/v1/users/<user_id>/transaction/add', methods=["POST"])
def add_transaction(user_id):
    data = request.get_json()

    user = storage.get('User', user_id)

    if not user:
        return jsonify({"error":"User not found"}), 404
    
    name = data.get('name')
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date')

    if not name or not amount or not description:
        return jsonify({"error":"Missing data"}), 400
    
    new_transaction = Transaction(user_id=user_id, name=name, amount=amount, description=description, date=date)
    user.balance += amount

    try:
        new_transaction.save_to_db()
    except:
        return jsonify({"error":"Could not create transaction"}), 400
    
    return jsonify(new_transaction.to_dict()), 201

# Delete Transaction
@app.route('/api/v1/users/<user_id>/transaction/<transaction_id>/delete', methods=["DELETE"])
def delete_transaction(user_id, transaction_id):
    affect_balance = request.args.get('affect_balance', 'true').lower() == 'true'
    
    user = storage.get('User', user_id)
    if not user: 
        return jsonify({"error":"User not found"}), 404

    transaction = storage.get('Transaction', transaction_id)
    if not transaction:
        return jsonify({"error":"Transaction not found"}), 404
    
    if affect_balance:
        user.balance -= transaction.amount

    try:
        user.transactions.remove(transaction)
        transaction.delete()
        user.save_to_db()  # Save the user after modifying the balance
    except Exception as e:
        return jsonify({"error":"Could not delete transaction", "details": str(e)}), 400
    
    return jsonify({"message":"Transaction Deleted"}), 200


# Update Transaction
@app.route('/api/v1/users/<user_id>/transaction/<transaction_id>/update', methods=["PATCH"])
def update_transaction(user_id, transaction_id):
    data = request.get_json()

    user = storage.get('User', user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    transaction = storage.get('Transaction', transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    name = data.get('name')
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date')

    if not name or amount is None or not description:
        return jsonify({"error": "Missing data"}), 400

    # Calculate the difference and adjust the user's balance
    difference = amount - transaction.amount
    user.balance += difference

    transaction.name = name
    transaction.amount = amount
    transaction.description = description
    transaction.date = date

    try:
        transaction.save_to_db()
        user.save_to_db()
    except Exception as e:
        return jsonify({"error": "Could not update transaction", "details": str(e)}), 400

    return jsonify(transaction.to_dict()), 200


@app.teardown_appcontext
def close_db(error):
    storage.close()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)