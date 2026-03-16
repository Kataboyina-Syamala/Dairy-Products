from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import get_db_connection
from datetime import datetime, timedelta

subscriptions_bp = Blueprint('subscriptions_bp', __name__)

@subscriptions_bp.route('/subscribe/<int:product_id>', methods=['GET', 'POST'])
def subscribe(product_id):
    if not session.get('user_id'):
        flash("Please login to subscribe to products.", "warning")
        return redirect(url_for('auth_bp.login'))
        
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM Products WHERE product_id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        flash("Product not found.", "danger")
        return redirect(url_for('products_bp.catalog'))
        
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        duration = int(request.form.get('duration', 30)) # days
        start_date = request.form.get('start_date')
        
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
            
        try:
            conn.execute('''
                INSERT INTO Subscriptions (user_id, product_id, quantity, start_date, duration, status)
                VALUES (?, ?, ?, ?, ?, 'Active')
            ''', (session['user_id'], product_id, quantity, start_date, duration))
            conn.commit()
            flash(f"Successfully subscribed to {product['name']} for {duration} days!", "success")
            return redirect(url_for('subscriptions_bp.my_subscriptions'))
        except Exception as e:
            conn.rollback()
            flash("Error creating subscription.", "danger")
        finally:
            conn.close()
            
    conn.close()
    return render_template('subscriptions/subscribe.html', product=product)

@subscriptions_bp.route('/subscriptions')
def my_subscriptions():
    if not session.get('user_id'):
        return redirect(url_for('auth_bp.login'))
        
    conn = get_db_connection()
    if session.get('role') == 'admin':
        subs = conn.execute('''
            SELECT s.*, p.name as product_name, p.price, u.name as customer_name 
            FROM Subscriptions s
            JOIN Products p ON s.product_id = p.product_id
            JOIN Users u ON s.user_id = u.user_id
            ORDER BY s.start_date DESC
        ''').fetchall()
    else:
        subs = conn.execute('''
            SELECT s.*, p.name as product_name, p.price 
            FROM Subscriptions s
            JOIN Products p ON s.product_id = p.product_id
            WHERE s.user_id = ?
            ORDER BY s.start_date DESC
        ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('subscriptions/list.html', subscriptions=subs)

@subscriptions_bp.route('/subscriptions/cancel/<int:sub_id>', methods=['POST'])
def cancel_subscription(sub_id):
    if not session.get('user_id'):
        return redirect(url_for('auth_bp.login'))
        
    conn = get_db_connection()
    # Verify ownership or admin
    sub = conn.execute('SELECT user_id FROM Subscriptions WHERE subscription_id = ?', (sub_id,)).fetchone()
    
    if sub and (sub['user_id'] == session['user_id'] or session.get('role') == 'admin'):
        conn.execute('UPDATE Subscriptions SET status = ? WHERE subscription_id = ?', ('Cancelled', sub_id))
        conn.commit()
        flash("Subscription cancelled successfully.", "info")
    else:
        flash("Unauthorized action.", "danger")
        
    conn.close()
    return redirect(url_for('subscriptions_bp.my_subscriptions'))
