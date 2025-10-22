## Strategic Reflections

## 1. Model Failure. 

Question: Your model underestimates delivery time on rainy days. Do you fix the model, the data, or the business expectations?

I would do the all 3 options, but in the following order:

1.  Fix the Data : As this is the root cause, the model is under predicting because its only input is Weather='Rainy'. This feature is too vague. A 20 minute drizzle is not the same as a 2 hour monsoon. I would work with the data engineering team to see if we can get a more detailed input, like rainfall intensity from a API. This new feature would give the model the detail it needs to distinguish between a minor delay and a major one.

2.  Fix the Model: If new data is not an option, my next step is implement a business rule on top of the model's prediction. As explained in my error insight md file. 

3.  Fix the Business Expectations : I would talk with the stakeholder and team and express that the model average error is 8.5 minutes, but on rainy days, its known error margin is higher. So maybe, apply like a period of grace when raining. 


## 2. Transferability: 

Question: The model performs well in Mumbai. It’s now being deployed in São Paulo. How do you ensure generalization?

I would not deploy the Mumbai trained model directly in Sao Paulo. I would assume it will fail, as the data values and the values of the city (traffic, common vehicle types, city layout, and even restaurant times) are different.

My process would be:

1.  Acquire São Paulo Database with food logs (same file as the one used but for Sao Paulo)
2. I would perform a new oversee on this data. 
3.  Rerun my train.py script, feeding it the new sao paulo odeliveries.csv. 
4.  Analyze metrics. 

---

## 3. GenAI Disclosure

Question: What parts of this project did you use GenAI tools for? How did you validate or modify their output?

I used AI as to accelerate development and fix some minor errors, not as a replacement for my own skills.
I used it to generate the initial file structure and the a pseudocode for the sklearn.Pipeline and ColumnTransformer. The use of libraries and explicit code was also consulted and comapared with AI. 
Also, the formatting of some md and code was used. 
I never trust AI code blindly. I manually reviewed every line. AI was a tool to help me work faster, but all final decisions, code logic, and insights were my own.


## Your Signature Insight

Question:What's one non-obvious insight or decision you're proud of from this project?

My proudest decision was handling missing data by building the SimpleImputer directly into the Pipeline instead of just dropping rows with data.dropna().

A more basic approach would be to clean the data first by removing all rows with nan values. However, this would eliminate valuable training data and creates a model that is less robust with less data used to be trained. It preserve data and made it production ready. 

Also, comparing the models gives a clear and transparent guide to select the model. 

## Going to Production

Question: How would you deploy your model to production? What other components would you need?

The train.py and predict.py scripts are the core of the system but a full production deployment requires a surrounding infrastructure. 

1.  I would wrap my predict.py logic in a web framework. This creates a web server with an API endpoint (, /predict) that can receive an order's features as a JSON request and return the predicted time as a JSON response

2.  I would create a Dockerfile to package API app, the requirements.txt, and the saved delivery_time_model.pkl file into a Docker image.

3.  I would deploy this container to a cloud service so that it is not local anymore. 

4. Lastly, I would keep an eye on the metrics of both the model and the deployment and made necessary arranges among time based on performance, scalability, users, accurary, etc. 
