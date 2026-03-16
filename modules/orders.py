from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import get_db_connection

orders_bp = Blueprint('orders_bp', __name__)

@orders_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    if not session.get('user_id'):
        flash("Please login to add items to your cart.", "warning")
        return redirect(url_for('auth_bp.login'))
        
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    
    # Check current stock
    conn = get_db_connection()
    product = conn.execute('SELECT stock, name FROM Products WHERE product_id = ?', (product_id,)).fetchone()
    conn.close()
    
    if not product:
        flash("Product not found.", "danger")
        return redirect(request.referrer or url_for('products_bp.catalog'))
        
    current_cart_qty = cart.get(product_id, 0)
    if current_cart_qty + quantity > product['stock']:
        flash(f"Cannot add {quantity} more of {product['name']}. Only {product['stock']} left in stock.", "danger")
    else:
        cart[product_id] = current_cart_qty + quantity
        session.modified = True
        flash(f"Added {product['name']} to cart.", "success")
        
    return redirect(request.referrer or url_for('products_bp.catalog'))

@orders_bp.route('/cart/remove/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
        flash("Item removed from cart.", "info")
    return redirect(url_for('orders_bp.view_cart'))

@orders_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    if cart:
        conn = get_db_connection()
        # Fetch product details for items in cart
        placeholders = ','.join('?' * len(cart))
        products = conn.execute(f'SELECT * FROM Products WHERE product_id IN ({placeholders})', list(cart.keys())).fetchall()
        conn.close()
        
        for p in products:
            pid = str(p['product_id'])
            if pid in cart:
                qty = cart[pid]
                item_total = p['price'] * qty
                total_amount += item_total
                cart_items.append({
                    'product_id': p['product_id'],
                    'name': p['name'],
                    'price': p['price'],
                    'quantity': qty,
                    'item_total': item_total,
                    'image': p['image']
                })
                
    return render_template('orders/cart.html', cart_items=cart_items, total_amount=total_amount)

@orders_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('user_id'):
        return redirect(url_for('auth_bp.login'))
        
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('products_bp.catalog'))
        
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        user_id = session['user_id']
        total_amount = float(request.form.get('total_amount', 0))
        delivery_slot_id = request.form.get('delivery_slot_id')
        
        conn = get_db_connection()
        try:
            # 1. Create Order
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Orders (user_id, total_amount, status, delivery_slot_id) VALUES (?, ?, ?, ?)',
                           (user_id, total_amount, 'Confirmed', delivery_slot_id))
            order_id = cursor.lastrowid
            
            # 2. Re-verify stock and create Order_Items, then deduct stock
            for pid, qty in cart.items():
                p = cursor.execute('SELECT price, stock FROM Products WHERE product_id = ?', (pid,)).fetchone()
                if p['stock'] < qty:
                    raise Exception(f"Insufficient stock for product ID {pid}")
                
                # Insert order item
                cursor.execute('INSERT INTO Order_Items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                               (order_id, pid, qty, p['price']))
                
                # Deduct stock
                cursor.execute('UPDATE Products SET stock = stock - ? WHERE product_id = ?', (qty, pid))
            
            # 3. Create Payment record
            cursor.execute('INSERT INTO Payments (order_id, payment_method, payment_status) VALUES (?, ?, ?)',
                           (order_id, payment_method, 'Success'))
                           
            conn.commit()
            session['cart'] = {} # Clear cart
            flash(f"Order #{order_id} placed successfully!", "success")
            return redirect(url_for('orders_bp.order_history'))
            
        except Exception as e:
            conn.rollback()
            flash(str(e), "danger")
            return redirect(url_for('orders_bp.view_cart'))
        finally:
            conn.close()
            
    # GET method - Calculate total for display
    conn = get_db_connection()
    placeholders = ','.join('?' * len(cart))
    products = conn.execute(f'SELECT product_id, price FROM Products WHERE product_id IN ({placeholders})', list(cart.keys())).fetchall()
    
    # Fetch Delivery Slots
    slots = conn.execute('SELECT * FROM Delivery_Slots').fetchall()
    conn.close()
    
    total_amount = sum(p['price'] * cart[str(p['product_id'])] for p in products if str(p['product_id']) in cart)
    
    return render_template('orders/checkout.html', total_amount=total_amount, slots=slots)

@orders_bp.route('/orders')
def order_history():
    if not session.get('user_id'):
        return redirect(url_for('auth_bp.login'))
        
    conn = get_db_connection()
    user_id = session['user_id']
    
    if session.get('role') == 'admin':
        orders = conn.execute('''
            SELECT o.*, u.name as customer_name 
            FROM Orders o 
            JOIN Users u ON o.user_id = u.user_id 
            ORDER BY o.order_date DESC
        ''').fetchall()
    else:
        orders = conn.execute('SELECT * FROM Orders WHERE user_id = ? ORDER BY order_date DESC', (user_id,)).fetchall()
        
    conn.close()
    return render_template('orders/history.html', orders=orders)
