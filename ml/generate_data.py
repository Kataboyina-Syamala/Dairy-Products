import pandas as pd
import numpy as np
import random
import os
import sqlite3
from datetime import datetime, timedelta

def generate_dummy_data(output_file='historical_sales.csv', num_days=365):
    """
    Generates dummy historical sales data for all 100 dairy products to be used in ML training.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'dairy_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    products_db = conn.execute("SELECT name, category FROM Products").fetchall()
    conn.close()
    
    if not products_db:
        print("No products found in DB. Run seed.py first.")
        return
        
    data = []
    start_date = datetime.now() - timedelta(days=num_days)
    
    for p in products_db:
        product = p['name']
        category = p['category']
        
        # Initial previous sales
        previous_sales = random.randint(20, 100)
        
        for i in range(num_days):
            current_date = start_date + timedelta(days=i)
            day_of_week = current_date.weekday() # 0 = Monday, 6 = Sunday
            
            # Simple season mapping (Northern Hemisphere)
            month = current_date.month
            if month in [12, 1, 2]: season = 'Winter'
            elif month in [3, 4, 5]: season = 'Spring'
            elif month in [6, 7, 8]: season = 'Summer'
            else: season = 'Autumn'
            
            season_encoded = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Autumn': 3}[season]
            
            # Base logic influenced by previous sales (Linear relationship)
            base_sales = int(previous_sales * random.uniform(0.9, 1.1))
            
            # Weekend bump
            if day_of_week in [5, 6]:
                base_sales += random.randint(10, 30)
                
            # Summer bump for cold products
            if season == 'Summer' and category in ['Ice Cream', 'Milk', 'Curd / Yogurt', 'Other Dairy']:
                base_sales += random.randint(20, 50)
                
            # Winter bump for Ghee/Butter
            if season == 'Winter' and category in ['Ghee', 'Butter']:
                base_sales += random.randint(10, 25)
                
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'product_name': product,
                'day_of_week': day_of_week,
                'season_encoded': season_encoded,
                'previous_sales': previous_sales,
                'quantity_sold': base_sales
            })
            
            previous_sales = base_sales # update for next day
            
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} records in {output_file}")

if __name__ == '__main__':
    generate_dummy_data(os.path.join(os.path.dirname(__file__), 'historical_sales.csv'))
