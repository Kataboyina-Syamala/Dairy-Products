from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database.db import get_db_connection

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/products')
def catalog():
    search = request.args.get('search', '')
    conn = get_db_connection()
    query = '''
        SELECT p.*, d.name as delivery_slot_name, d.start_time, d.end_time 
        FROM Products p 
        LEFT JOIN Delivery_Slots d ON p.delivery_slot_id = d.slot_id
    '''
    
    if search:
        query += " WHERE p.name LIKE ? OR p.category LIKE ?"
        products = conn.execute(query, ('%' + search + '%', '%' + search + '%')).fetchall()
    else:
        products = conn.execute(query).fetchall()

    conn.close()
    return render_template('products/catalog.html', products=products, search=search)

@products_bp.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if session.get('role') != 'admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        image = request.form.get('image') # For simplicity, using image URL or path
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO Products (name, price, stock, description, image)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, stock, description, image))
        conn.commit()
        conn.close()
        flash("Product added successfully.", "success")
        return redirect(url_for('products_bp.catalog'))
        
    return render_template('products/add_product.html')

@products_bp.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
        
    conn = get_db_connection()
    conn.execute('DELETE FROM Products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    flash("Product deleted successfully.", "success")
    return redirect(url_for('products_bp.catalog'))

@products_bp.route('/api/products/<int:product_id>')
def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM Products WHERE product_id = ?', (product_id,)).fetchone()
    conn.close()
    if product:
        return jsonify(dict(product))
    return jsonify({"error": "Not found"}), 404
