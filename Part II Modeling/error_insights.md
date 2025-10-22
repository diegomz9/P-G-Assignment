## Error Insights

## Residual Analysis
To understand when the model fails, analyze its residuals. A residual is the difference between the actual time and the predicted time (Actual - Predicted).

## Failure Scenarios

<img width="595" height="117" alt="image" src="https://github.com/user-attachments/assets/a3682cf9-3511-4483-b736-5b574cf68438" />

Our final model has an RMSE of around 12.8 minutes, meaning its good at predicting the average delivery. 

### Failure Scenario
* For example, the combination of Weather = 'Snowy' AND Traffic_Level = 'High' AND Distance_km > 15.
* The model learns the average cost of snow and the average cost of high traffic. Its less likely to learn the multiplicative effect when they happen together, Snow + Traffic. This  can lead to a severe under-prediction.

### Failure Scenario
* For example, a courier with low experience  is given a high traffic or long distance route.
* Courier_Experience_yrs is the #3 feature, for example, an experienced courier knows how to handle high traffic, a new courier does not. The model may fail to capture this. 

### Failure Scenario
The model sees Vehicle_Type_Bike is important (rank #6), but it may underestimate how dramatically a bikes speed drops off with long distances.

## Actionable Insights

1.  **Add Business Rules:** We cannot rely on the model for extreme  cases. We should implement a  rule based on the business scenarios or needs. 
2.  **Dispatch:**  implement an algorithm that avoid giving new couriers or bikers the more complicated routes or scenarios. 
