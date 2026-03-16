from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import bcrypt
from database.db import get_db_connection

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')
        
        if not all([name, email, phone, address, password]):
            flash("All fields are required.", "danger")
            return redirect(url_for('auth_bp.register'))
            
        # Hash password
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO Users (name, email, phone, address, password, role)
                VALUES (?, ?, ?, ?, ?, 'customer')
            ''', (name, email, phone, address, hashed_pw))
            conn.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('auth_bp.login'))
        except conn.IntegrityError:
            flash("Email already registered.", "danger")
        finally:
            conn.close()
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['name'] = user['name']
            
            if user['role'] == 'admin':
                return redirect(url_for('ml_bp.dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

def create_default_admin():
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM Users WHERE email = ?', ('admin@dairy.com',)).fetchone()
    if not admin:
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw('admin123'.encode('utf-8'), salt).decode('utf-8')
        conn.execute('''
            INSERT INTO Users (name, email, phone, address, password, role)
            VALUES (?, ?, ?, ?, ?, 'admin')
        ''', ('Admin', 'admin@dairy.com', '0000000000', 'Admin Office', hashed_pw))
        conn.commit()
        print("Default admin created (admin@dairy.com / admin123)")
    conn.close()

# Provide a utility endpoint to check login status
@auth_bp.route('/api/user_status')
def user_status():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "name": session['name'], "role": session['role']})
    return jsonify({"logged_in": False})
