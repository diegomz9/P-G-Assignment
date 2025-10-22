## Model Notes

## Modeling Logic
My approach was to create a robust and production ready pipeline for the presented business scenario. Also, I wanted to test the most common ML libraries/models to select the most efficient based on the need and data. 

1.  **Problem Formulation:** supervised regression.
2.  **Pipeline:** Using the existing Python libraries, all preprocessing is built into an sklearn.Pipeline. This is a critical best practice that prevents data leakage.
3.  **Data Splitting:** I used a 60% / 20% / 20% Train / Validation / Test split.
    * Train Set : Used for fitting the models.
    * Validation Set : Used to compare the trained models and select a winner.
    * Test Set : used only once at the very end to get an unbiased score of the final winning model with unseen data. 
4.  **Model :** I decided to use the xisting libraries, and fit the 3 most industry common models/libraries and based on the RMSE selected a winner
    * RandomForestRegressor
    * XGBRegressor
    * LGBMRegressor
5.  **Model Selection:** Based on the output, LightGBM was selected as the final model, as it achieved the lowest RMSE on the validation set RMSE: 12.1513. 

## Metric Choice

I used a primary metric for selection and secondary metrics for context.
* **Primary Metric: RMSE (Root Mean Squared Error)**
    * RMSE penalizes large errors heavily than small ones. For this business problem, a 30-minute delay is much worse than two 15 minute delays. RMSE captures this business cost and understand it. 
    * **Final Score:** The models final, unbiased performance on the unseen test set was an RMSE of 12.7980 minute.
* **Secondary Metric: MAE (Mean Absolute Error)**
    * **The final MAE of 8.4805 minutes means that, on average, the models prediction is off by around 8.5 minutes
* **Contextual Metric: R-squared (R²)**
    * **This gives a high-level sense of fit. Our final **R² of 0.6751** means the model can explain around 67.5% of the variance in delivery times.
