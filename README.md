# 🥛 Smart Dairy Management System V2

A comprehensive, Machine Learning-powered full-stack web application designed for dairy product ordering, inventory management, and demand forecasting.

## 🌟 Key Features

### 🛒 Customer Experience
* **Massive Catalog:** Browse over 100 dairy products across 10 distinct categories (Milk, Curd, Ghee, Butter, Ice Cream, etc.).
* **Smart Checkout:** Seamlessly add items to your cart and choose preferred **Delivery Slots** (e.g., Morning 5 AM - 7 AM).
* **Subscriptions:** Set up recurring daily milk and dairy deliveries that automatically deduct from inventory.
* **Modern Interface:** A clean, responsive design built with Bootstrap 5 and custom CSS animations.

### 🛡️ Admin & Analytics
* **RBAC Authentication:** Secure, bcrypt-hashed login separating Customer and Administrator views.
* **Inventory Control:** Full CRUD capabilities to manage products, update tracking, and toggle availability.
* **AI Demand Prediction (V2):** Utilizing a custom-trained **Linear Regression Model** (Scikit-Learn) with an **R2 Score of 0.99**, the Admin Dashboard predicts actionable stock requirements for the next 7 days based on simulated historical sales, seasonality, and previous days' momentum.

## 🚀 Tech Stack

* **Backend:** Python, Flask, Werkzeug
* **Database:** SQLite (Relational structure via `schema.sql`)
* **Machine Learning:** Pandas, NumPy, Scikit-Learn
* **Frontend:** HTML5, CSS3, JavaScript, Jinja2, Bootstrap 5, Chart.js

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kataboyina-Syamala/Dairy-Products.git
   cd Dairy-Products
   ```

2. **Install dependencies:**
   Make sure you have Python 3.8+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize & Seed the Database:**
   This will create the SQLite database and seed it with 100 products and 5 delivery slots.
   ```bash
   python database/seed.py
   ```

4. **Generate ML Data & Train the Model:**
   ```bash
   python ml/generate_data.py
   python ml/train_model.py
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

## 🔑 Default Credentials

* **Admin Access:**
  * Email: `admin@dairy.com`
  * Password: `admin123`

---
*Built with modern full-stack methodologies and integrated AI optimization.*
