-- Drop tables if they exist to prevent errors on multiple runs
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Delivery_Slots;
DROP TABLE IF EXISTS Users;

-- Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'customer' -- 'customer' or 'admin'
);

-- Delivery Slots Table
CREATE TABLE Delivery_Slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    name TEXT NOT NULL
);

-- Products Table
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    image TEXT,
    category TEXT,
    delivery_slot_id INTEGER,
    availability TEXT DEFAULT 'Available',
    FOREIGN KEY (delivery_slot_id) REFERENCES Delivery_Slots(slot_id)
);

-- Orders Table
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'Pending', -- Pending, Confirmed, Delivered, Cancelled
    delivery_slot_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_slot_id) REFERENCES Delivery_Slots(slot_id)
);

-- Order_Items Table
CREATE TABLE Order_Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- Subscriptions Table (for daily milk delivery)
CREATE TABLE Subscriptions (
    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    start_date DATE NOT NULL,
    duration INTEGER NOT NULL, -- in days
    status TEXT DEFAULT 'Active', -- Active, Cancelled, Completed
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- Payments Table (simulation)
CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    payment_method TEXT NOT NULL, -- Credit Card, UPI, etc.
    payment_status TEXT DEFAULT 'Pending', -- Success, Failed, Pending
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);
