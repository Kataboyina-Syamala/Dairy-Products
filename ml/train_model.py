import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

def train_models():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'historical_sales.csv')
    
    if not os.path.exists(data_path):
        print("Data not found. Run generate_data.py first.")
        return
        
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Encode product names
    label_encoder = LabelEncoder()
    df['product_encoded'] = label_encoder.fit_transform(df['product_name'])
    
    # Save the encoder for inference later
    joblib.dump(label_encoder, os.path.join(base_dir, 'label_encoder.pkl'))
    
    # Updated features for Linear Regression
    features = ['product_encoded', 'day_of_week', 'season_encoded', 'previous_sales']
    target = 'quantity_sold'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\nTraining Linear Regression Model...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_predictions = lr_model.predict(X_test)
    print(f"LR R2 Score: {r2_score(y_test, lr_predictions):.2f}")
    
    # We will save and use Linear Regression as requested
    model_path = os.path.join(base_dir, 'demand_model.pkl')
    joblib.dump(lr_model, model_path)
    print(f"\nSaved Linear Regression model to {model_path}")

if __name__ == '__main__':
    train_models()
