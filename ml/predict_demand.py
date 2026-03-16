import os
import joblib
import pandas as pd
from datetime import datetime, timedelta

class DemandPredictor:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.base_dir, 'demand_model.pkl')
        self.encoder_path = os.path.join(self.base_dir, 'label_encoder.pkl')
        
        self.model = None
        self.encoder = None
        self._load_models()
        
    def _load_models(self):
        if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
            self.model = joblib.load(self.model_path)
            self.encoder = joblib.load(self.encoder_path)
            
    def predict_next_days(self, product_name, days=7):
        """
        Predict demand for a specific product for the next N days.
        Returns a list of dictionaries with date and predicted quantity.
        """
        if not self.model or not self.encoder:
            return []
            
        try:
            # Check if product is known to the encoder
            if product_name not in self.encoder.classes_:
                return []
                
            product_encoded = self.encoder.transform([product_name])[0]
            
            predictions = []
            start_date = datetime.now()
            
            for i in range(days):
                target_date = start_date + timedelta(days=i)
                day_of_week = target_date.weekday()
                
                month = target_date.month
                if month in [12, 1, 2]: season = 'Winter'
                elif month in [3, 4, 5]: season = 'Spring'
                elif month in [6, 7, 8]: season = 'Summer'
                else: season = 'Autumn'
                
                season_encoded = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Autumn': 3}[season]
                
                # Mock previous sales for the prediction if not available.
                # In a real app we'd fetch the actual sales from yesterday.
                if i == 0:
                    previous_sales = 50 # Base estimate
                
                # Model expects DataFrame conceptually, or 2D array: [[product_encoded, day_of_week, season_encoded, previous_sales]]
                input_data = pd.DataFrame([{
                    'product_encoded': product_encoded,
                    'day_of_week': day_of_week,
                    'season_encoded': season_encoded,
                    'previous_sales': previous_sales
                }])
                
                pred_qty = self.model.predict(input_data)[0]
                
                predictions.append({
                    'date': target_date.strftime('%Y-%m-%d'),
                    'day_name': target_date.strftime('%A'),
                    'predicted_demand': max(0, int(round(pred_qty))) # ensure no negative predictions
                })
                
                # Set previous sales for the NEXT day's prediction to be today's predicted demand
                previous_sales = pred_qty
                
            return predictions
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return []
