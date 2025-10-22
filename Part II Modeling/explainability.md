# Explainability Report

## 1. Information Source

These insights come from the feature importance tool of the winning model LightGBM.
<img width="380" height="314" alt="image" src="https://github.com/user-attachments/assets/f6e36704-c5c8-4731-ad26-5afc28f1429a" />


The importance type shown in the output is count. This means the numbers (for example 783) are not a percentage but the total number of times that feature was used to make a decision ,a split across, all the trees in the model. higher count means the model relies on that feature more heavily.

## Key Feature Insights

Distance_km .783. This is the most dominant factor. The model learned that distance is the most frequent and reliable question to ask when estimating delivery time. 

Preparation_Time_min.  480 . This is the second most used feature. It confirms that time spent at the restaurant is a decissive and independent component of the total delivery time.

Courier_Experience_yrs . 309 .  Courier experience is a significant factor.

## Other Interesting Insights

* **Weather_Clear (112) vs. Weather_Rainy (34):** This doesn't mean "Rainy" is unimportant. It means the model found it more efficient to ask, "Is the weather 'Clear'?" (Yes/No) with the binary approach. If the answer is "no," it assumes a delay and moves on.

* **Traffic_Level_Low (93) vs. Traffic_Level_High (62):** Similar to weather, the model often checks for Low traffic. This implies that "Low" traffic is a strong signal for a faster delivery.
  
* **Vehicle_Type_Bike (81):** The fact that Bike is the most important vehicle type shows that the model identifies bike deliveries as a special case that requires significant adjustments, maybe due to their sensitivity to distance or weather.

## Actionable Takeaways

1.  **The business cannot control distance (#1), but it can control Preparation_Time_min (#2). Optimizing kitchen to courier process is the biggest internal opportunity for improvement.
2.  ** Courier_Experience_yrs (#3) is a powerful predictor. The platform could use this for more accurate arrivals. 
