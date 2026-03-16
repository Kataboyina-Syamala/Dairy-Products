import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'dairy_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def seed_database():
    print("Initializing Database with 100 Products and Delivery Slots...")
    conn = get_db_connection()
    c = conn.cursor()
    
    # 1. Execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        c.executescript(f.read())
        
    print("Schema executed. Seeding data...")

    # 2. Add Delivery Slots
    slots = [
        ('Morning (5 AM \u2013 7 AM)', '05:00', '07:00'),
        ('Morning (7 AM \u2013 9 AM)', '07:00', '09:00'),
        ('Afternoon (12 PM \u2013 2 PM)', '12:00', '14:00'),
        ('Evening (5 PM \u2013 7 PM)', '17:00', '19:00'),
        ('Night (7 PM \u2013 9 PM)', '19:00', '21:00'),
    ]
    c.executemany("INSERT INTO Delivery_Slots (name, start_time, end_time) VALUES (?, ?, ?)", slots)

    # 3. Add Admin User
    admin_pw = generate_password_hash("admin123")
    c.execute("""
        INSERT INTO Users (name, email, phone, address, password, role)
        VALUES ('Admin', 'admin@dairy.com', '0000000000', 'HQ', ?, 'admin')
    """, (admin_pw,))
    
    # 4. Add 100 Products with appropriate categories and target delivery slots
    products = [
        # Milk
        ('Cow Milk', 60, 'Milk', 1), ('Buffalo Milk', 70, 'Milk', 1), ('Toned Milk', 50, 'Milk', 1),
        ('Double Toned Milk', 45, 'Milk', 1), ('Skimmed Milk', 40, 'Milk', 1), ('Organic Milk', 80, 'Milk', 1),
        ('Flavored Milk \u2013 Chocolate', 35, 'Milk', 2), ('Flavored Milk \u2013 Strawberry', 35, 'Milk', 2),
        ('Flavored Milk \u2013 Mango', 35, 'Milk', 2), ('Flavored Milk \u2013 Vanilla', 35, 'Milk', 2),
        
        # Curd
        ('Plain Curd', 40, 'Curd / Yogurt', 2), ('Thick Curd', 50, 'Curd / Yogurt', 2), ('Organic Curd', 60, 'Curd / Yogurt', 2),
        ('Greek Yogurt', 120, 'Curd / Yogurt', 2), ('Probiotic Yogurt', 90, 'Curd / Yogurt', 2), ('Strawberry Yogurt', 45, 'Curd / Yogurt', 2),
        ('Mango Yogurt', 45, 'Curd / Yogurt', 2), ('Blueberry Yogurt', 55, 'Curd / Yogurt', 2), ('Sweet Curd', 50, 'Curd / Yogurt', 2),
        ('Low Fat Yogurt', 45, 'Curd / Yogurt', 2),

        # Butter
        ('Salted Butter', 250, 'Butter', 3), ('Unsalted Butter', 260, 'Butter', 3), ('White Butter', 300, 'Butter', 3),
        ('Garlic Butter', 280, 'Butter', 3), ('Herb Butter', 290, 'Butter', 3), ('Cooking Butter', 240, 'Butter', 3),
        ('Low Fat Butter', 270, 'Butter', 3), ('Amul Style Butter', 255, 'Butter', 3), ('Spreadable Butter', 285, 'Butter', 3),
        ('Organic Butter', 350, 'Butter', 3),

        # Cheese
        ('Mozzarella Cheese', 200, 'Cheese', 3), ('Cheddar Cheese', 220, 'Cheese', 3), ('Paneer Cheese', 150, 'Cheese', 3),
        ('Processed Cheese', 180, 'Cheese', 3), ('Cheese Slices', 130, 'Cheese', 3), ('Cheese Cubes', 140, 'Cheese', 3),
        ('Pizza Cheese', 250, 'Cheese', 3), ('Cream Cheese', 300, 'Cheese', 3), ('Cottage Cheese', 160, 'Cheese', 3),
        ('Cheese Spread', 170, 'Cheese', 3),

        # Paneer
        ('Fresh Paneer', 100, 'Paneer', 3), ('Low Fat Paneer', 110, 'Paneer', 3), ('Organic Paneer', 150, 'Paneer', 3),
        ('Malai Paneer', 130, 'Paneer', 3), ('Paneer Cubes', 120, 'Paneer', 3), ('Paneer Block', 200, 'Paneer', 3),
        ('Paneer Crumbles', 90, 'Paneer', 3), ('Smoked Paneer', 180, 'Paneer', 3), ('Tandoori Paneer', 160, 'Paneer', 3),
        ('Paneer Spread', 140, 'Paneer', 3),

        # Ghee
        ('Cow Ghee', 600, 'Ghee', 4), ('Buffalo Ghee', 650, 'Ghee', 4), ('Organic Ghee', 800, 'Ghee', 4),
        ('Desi Ghee', 750, 'Ghee', 4), ('A2 Cow Ghee', 1200, 'Ghee', 4), ('Herbal Ghee', 900, 'Ghee', 4),
        ('Homemade Style Ghee', 700, 'Ghee', 4), ('Cultured Ghee', 850, 'Ghee', 4), ('Pure Cow Ghee', 620, 'Ghee', 4),
        ('Premium Ghee', 950, 'Ghee', 4),

        # Ice Cream
        ('Vanilla Ice Cream', 150, 'Ice Cream', 5), ('Chocolate Ice Cream', 180, 'Ice Cream', 5), ('Strawberry Ice Cream', 170, 'Ice Cream', 5),
        ('Mango Ice Cream', 200, 'Ice Cream', 5), ('Butterscotch Ice Cream', 190, 'Ice Cream', 5), ('Pista Ice Cream', 220, 'Ice Cream', 5),
        ('Cassata Ice Cream', 250, 'Ice Cream', 5), ('Kulfi Ice Cream', 60, 'Ice Cream', 5), ('Cone Ice Cream', 50, 'Ice Cream', 5),
        ('Ice Cream Family Pack', 400, 'Ice Cream', 5),

        # Dairy Desserts
        ('Rasgulla', 120, 'Dairy Desserts', 4), ('Gulab Jamun', 150, 'Dairy Desserts', 4), ('Rasmalai', 200, 'Dairy Desserts', 4),
        ('Milk Cake', 300, 'Dairy Desserts', 4), ('Kheer Mix', 80, 'Dairy Desserts', 4), ('Basundi', 180, 'Dairy Desserts', 4),
        ('Rabri', 220, 'Dairy Desserts', 4), ('Peda', 250, 'Dairy Desserts', 4), ('Kalakand', 320, 'Dairy Desserts', 4),
        ('Sandesh', 280, 'Dairy Desserts', 4),

        # Other Dairy Products
        ('Buttermilk', 20, 'Other Dairy', 2), ('Lassi Sweet', 30, 'Other Dairy', 2), ('Lassi Salted', 25, 'Other Dairy', 2),
        ('Mango Lassi', 40, 'Other Dairy', 2), ('Sweetened Condensed Milk', 110, 'Other Dairy', 3), ('Milk Powder', 250, 'Other Dairy', 3),
        ('Baby Milk Formula', 500, 'Other Dairy', 3), ('Whey Protein Dairy', 1500, 'Other Dairy', 3), ('Milk Cream', 130, 'Other Dairy', 3),
        ('Fresh Cream', 150, 'Other Dairy', 3),

        # Value Added
        ('Chocolate Milkshake', 60, 'Value Added Dairy', 2), ('Strawberry Milkshake', 60, 'Value Added Dairy', 2), ('Cold Coffee Milk', 70, 'Value Added Dairy', 2),
        ('Milk Smoothie', 80, 'Value Added Dairy', 2), ('Banana Milkshake', 50, 'Value Added Dairy', 2), ('Protein Milk Drink', 100, 'Value Added Dairy', 2),
        ('Energy Milk Drink', 90, 'Value Added Dairy', 2), ('Almond Milk Drink', 120, 'Value Added Dairy', 2), ('Saffron Milk', 150, 'Value Added Dairy', 2),
        ('Turmeric Milk', 80, 'Value Added Dairy', 2)
    ]
    
    # Insert with stock=50, availability logic (will just be 'Available' as stock > 0)
    for p in products:
        name, price, category, slot_id = p
        # Image placeholder
        image = f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"
        c.execute("""
            INSERT INTO Products (name, price, stock, description, image, category, delivery_slot_id, availability)
            VALUES (?, ?, 50, ?, ?, ?, ?, 'Available')
        """, (name, price, f"Premium quality {name}", image, category, slot_id))

    conn.commit()
    conn.close()
    print("Database Seeded Successfully!")

if __name__ == '__main__':
    seed_database()
