# predict.py
#add new values as needed and test the selected model on train.py.

import pandas as pd
import joblib
import numpy as np

# path to the model we saved in train.py
MODEL_PATH = 'delivery_time_model.pkl'

def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        print(f"Error: Model file '{MODEL_PATH}' not found.")
        print("Run train.py first.")
        return None

def predict(model, input_data: pd.DataFrame):
    #uses the data linked with model
    return model.predict(input_data)

if __name__ == "__main__":
    
    # load the model
    pipeline = load_model()
    
    if pipeline:
        print("Model loaded successfully.")
        
        # add new sample data to predict
        new_orders = pd.DataFrame({
            'Distance_km': [10.5, 5.2, 18.0],
            'Weather': ['Rainy', 'Clear', 'Snowy'],
            'Traffic_Level': ['High', 'Low', 'Medium'],
            'Time_of_Day': ['Evening', 'Afternoon', 'Night'],
            'Vehicle_Type': ['Scooter', 'Bike', 'Car'],
            'Preparation_Time_min': [25, 15, 22],
            'Courier_Experience_yrs': [3.0, None, 8.0]
        })
        
        print("\n Predicting on new data")
        print(new_orders.to_markdown(index=False))
        
        # make predictions
        predictions = predict(pipeline, new_orders)
        
        # show results
        new_orders['Predicted_Delivery_Time_min'] = np.round(predictions, 2)
        print("\nPredictions")
        print(new_orders[['Predicted_Delivery_Time_min']].to_markdown())