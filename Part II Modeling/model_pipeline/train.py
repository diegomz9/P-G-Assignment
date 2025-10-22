# train.py
import pandas as pd
import numpy as np
import joblib 

# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Models 
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# eval metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# PATHS
DATABASE_PROVIDED = 'Food_Delivery_Times.csv'
MODEL_CHOSEN = 'delivery_time_model.pkl'
TARGET = 'Delivery_Time_min'


NUMERICAL_FEATURES = [
    'Distance_km',
    'Preparation_Time_min',
    'Courier_Experience_yrs'
]
CATEGORICAL_FEATURES = [
    'Weather',
    'Traffic_Level',
    'Time_of_Day',
    'Vehicle_Type'
]

# randon state for ML model random number
RANDOM_STATE = 50

#prepocessing function
def build_preprocessor() -> ColumnTransformer:
    
    # numerical data prepocessing
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical data preprocessing
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        #binary so that model understand
        ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    # combine pipelines preprocessing 
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, NUMERICAL_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ],
        remainder='drop'
    )
    
    return preprocessor

#helper function to not repeat on 3 models .
def evaluate_model(y_true, y_pred, model_name, dataset_name="Validation"):
    
    #calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"Results for {model_name} on {dataset_name} Set ")
    print(f"  R-squared R²: {r2:.4f}")
    print(f"  Mean Absolute Error MAE: {mae:.4f} ")
    print(f"  Root Mean Squared Error RMSE: {rmse:.4f} ")
    print("-" * (25 + len(model_name) + len(dataset_name)))
    
    # return RMSE for comparison
    return rmse

def main():
    
    # Load data file 
    try:
        data = pd.read_csv(DATABASE_PROVIDED)
    except FileNotFoundError:
        print(f"Error data file not found at {DATABASE_PROVIDED}")
        return

    data = data.replace('', np.nan)
    
    #Define features X and target y
    X = data.drop(columns=[TARGET, 'Order_ID'])
    y = data[TARGET]
    
    X = X[y.notna()]
    y = y.dropna()

    # Data split Train Validation Test
    print("Splitting data into train, validation, and test sets.")
    
    #split into training+validation 80% and a final test set 20%
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    
    # Now, split the 80% into training 60% total and validation 20% total
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.25, random_state=RANDOM_STATE
    )

    print(f"Total samples: {len(X)}")
    print(f"  Training samples:   {len(X_train)}") #train models
    print(f"  Validation samples: {len(X_val)}") # compare and choose winner
    print(f"  Test samples:       {len(X_test)}") # test at the end

    # Build Preprocessor so that it cleans the data
    preprocessor = build_preprocessor()

    # models to Compare
    models = {
        'RandomForest': RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
        'XGBoost': XGBRegressor(random_state=RANDOM_STATE, n_jobs=-1,
                                objective='reg:squarederror'),
        'LightGBM': LGBMRegressor(random_state=RANDOM_STATE, n_jobs=-1, verbose=-1)
    }

    model_comparison = []
    best_pipeline = None
    best_model_name = ""
    best_val_rmse = float('inf')


    # train and Evaluate Models on Validation Set ---
    print("\nStarting model training and comparison...")
    
    for name, model in models.items():
        
        # full process, preposessing and model for each model
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        # train the model on TRAINING set
        print(f"\nTraining {name}...")
        pipeline.fit(X_train, y_train)
        
        # make predictions on the VALIDATION set
        y_val_pred = pipeline.predict(X_val)
        
        # evaluate and store results
        val_rmse = evaluate_model(y_val, y_val_pred, name, dataset_name="Validation")
        
        model_comparison.append({'Model': name, 'Validation RMSE': val_rmse})
        
        # check if this is the best model so far
        if val_rmse < best_val_rmse:
            best_val_rmse = val_rmse
            best_pipeline = pipeline  # Save the whole pipeline
            best_model_name = name

    # show Comparison and Select Best Model ---
    print("\nModel Comparison on Validation Set")
    results_df = pd.DataFrame(model_comparison).sort_values(by='Validation RMSE')
    print(results_df.to_markdown(index=False, floatfmt=".4f"))

    print(f"\nBest model selected: {best_model_name} (Validation RMSE: {best_val_rmse:.4f})")
    
    # final Evaluation on Test Set
    # This is the "locked box" evaluation. We only do this ONCE.
    print(f"\nRunning final evaluation for {best_model_name} on the (unseen) TEST set...")
    y_test_pred = best_pipeline.predict(X_test)
    
    # This is our final, most honest score, using all metrics
    test_rmse = evaluate_model(y_test, y_test_pred, best_model_name, dataset_name="Test")

    # save Best Model
    print(f"Saving best model to {MODEL_CHOSEN}...")
    joblib.dump(best_pipeline, MODEL_CHOSEN)
    print("Model saved successfully.")

    # Show Feature Importances ---
    print(f"\n Feature Importances for {best_model_name} ")
    try:
        final_model = best_pipeline.named_steps['model']
        feature_names = best_pipeline.named_steps['preprocessor'].get_feature_names_out()
        importances = final_model.feature_importances_
        
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        
        importance_df['Feature'] = importance_df['Feature'].str.replace('num__', '').str.replace('cat__', '')
        
        print("Top 10 most important features:")
        print(importance_df.head(10).to_markdown(index=False, floatfmt=".4f"))
    
    except Exception as e:
        print(f"Could not retrieve feature importances: {e}")


if __name__ == "__main__":
    main()
