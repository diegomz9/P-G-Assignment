
## EDA Report

## Key Patterns & Findings

My initial exploration focused on understanding the relationships between the features and the target variable `Delivery_Time_min`.

* **Target:** There are late deliveries that are the source of customer complaints and are the single most important events for the model to predict.
* **Predictors:** Based on the output, `Distance_km` and `Preparation_Time_min` show a strong correlation with delivery time. Before running the code, when overviewing the columns, these two were the my top features. 
* **Categorical Impact:** `Weather` conditions like 'Snowy' or 'Rainy' and `Traffic_Level` 'High' are clearly associated with higher average delivery times compared to 'Clear' or 'Low' conditions. These were transformed to binary values for the model to interpret them correctly. 

## 2. Outliers

I identified two types of outliers in the dataset:

1.  **Data entry Errors:** Some rows had illogical values. These were treated as missing data and handled by the imputation pipeline.
2.  **Key Eent Outliers:** These are the very long delivery times, these were the cases that needed to be improved as the business scenario. 

## 3. Assumptions Made for Modeling
I made the following assumptions, which are built into the code:

1.  **Missing Data is Best Imputed:** Dropping rows with any missing value, such as Courier Experience, would be wasteful.  I assumed its better to fill in these values to retain the information from the other columns.
2.  **Imputation Strategy:**
    * For numerical features, I assumed the **median** is the best fill-in value, best when dealing outliers.
    * For categorical features, I assumed the **most frequent** value is the safest and most representative.
3.  **Irrelevant Features:** I assumed Order_ID is a unique identifier with no predictive power and should be dropped.
4.  **Target Feature:** I assumed rows with a missing Delivery_Time_min are unusable for training and were safely dropped.
