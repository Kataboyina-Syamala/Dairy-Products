from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from database.db import get_db_connection
from ml.predict_demand import DemandPredictor

ml_bp = Blueprint('ml_bp', __name__)
predictor = DemandPredictor()

@ml_bp.route('/admin/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        flash("Access Denied.", "danger")
        return redirect(url_for('home'))
        
    conn = get_db_connection()
    
    # Basic Stats
    total_users = conn.execute('SELECT COUNT(*) as count FROM Users WHERE role="customer"').fetchone()['count']
    total_orders = conn.execute('SELECT COUNT(*) as count FROM Orders').fetchone()['count']
    total_revenue = conn.execute('SELECT SUM(total_amount) as total FROM Orders WHERE status="Confirmed"').fetchone()['total'] or 0
    
    # Products for prediction dropdown
    products = conn.execute('SELECT name FROM Products').fetchall()
    
    # Recent orders
    recent_orders = conn.execute('''
        SELECT o.*, u.name as customer_name 
        FROM Orders o JOIN Users u ON o.user_id = u.user_id 
        ORDER BY o.order_date DESC LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         products=products,
                         recent_orders=recent_orders)

@ml_bp.route('/api/predict_demand/<product_name>')
def get_prediction(product_name):
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
        
    predictions = predictor.predict_next_days(product_name, days=7)
    return jsonify(predictions)
