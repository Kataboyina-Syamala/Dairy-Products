from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.db import init_db
import os

app = Flask(__name__)
# Secure secret key for sessions
app.secret_key = os.urandom(24)

# Initialize blueprints/modules (to be implemented)
from modules.auth import auth_bp
from modules.auth import create_default_admin
from modules.products import products_bp
from modules.orders import orders_bp
from modules.subscriptions import subscriptions_bp
from modules.ml_prediction import ml_bp

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(subscriptions_bp)
app.register_blueprint(ml_bp)

@app.route('/')
def home():
    # Fetch some featured products from DB later
    return render_template('home.html')

if __name__ == '__main__':
    # Initialize the database before running
    init_db()
    with app.app_context():
        create_default_admin()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
