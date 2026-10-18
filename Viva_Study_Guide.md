# Complete Viva Study Guide: Flight Fare Prediction

**How to use this guide:**
This guide is designed for someone who is learning from scratch. Read this 2-3 times before your Viva. It explains what you built, how the code works, and exactly how to answer the mentor's questions.

---

## 1. The Elevator Pitch (Memorize This)
If the mentor asks: **"What is your project about?"**

**Your Answer:** 
> "My project is a Machine Learning web application that predicts domestic flight prices in India. I took a dataset of 300,000 flight records from Kaggle, cleaned the data, and trained five different algorithms. The Random Forest model performed the best with 98.5% accuracy. Finally, I deployed this model using Flask so a user can interact with it on a webpage."

---

## 2. Core Concepts Explained Simply

### What is Exploratory Data Analysis (EDA)?
* **Simple terms:** EDA is just looking at your data using graphs to find patterns before you do any machine learning.
* **In your project:** You used Matplotlib and Seaborn (Python graphing libraries) to see that flight prices go up as the departure date gets closer.

### What is an Outlier and what is IQR?
* **Simple terms:** An outlier is crazy, unrealistic data (like a flight ticket that costs 10 lakh rupees). IQR (Interquartile Range) is a math formula used to find these crazy numbers and delete them so they don't confuse your model.

### What is One-Hot Encoding?
* **Simple terms:** Machine Learning models only understand numbers, not text. So if you have an airline named "Vistara", the model crashes. One-Hot Encoding converts text into 0s and 1s. So "Vistara" becomes `[1, 0, 0]` and "Indigo" becomes `[0, 1, 0]`.

### What is a Random Forest Regressor?
* **Simple terms:** A 'Decision Tree' is like asking a series of Yes/No questions to guess a price. A 'Random Forest' is literally a forest of hundreds of Decision Trees guessing the price at the same time, and then taking the average of all their guesses. It is an "Ensemble" (group) method. That's why it is so highly accurate.

### What are MAE, RMSE, and R-Squared (R²)?
These are report cards for your model:
* **MAE (Mean Absolute Error):** On average, how many Rupees was your model's guess wrong by? (Yours was wrong by only 1,250 INR).
* **RMSE (Root Mean Squared Error):** Similar to MAE, but it punishes the model heavily for really massive mistakes.
* **R² Score:** A score out of 100% showing how well your model explains the data. Yours got 98.56%, which is an A+ grade.

### What is Flask?
* **Simple terms:** Python code usually runs in a boring black terminal. Flask is a tool that lets you connect your Python code to a beautiful HTML website. When the user clicks "Predict" on the website, Flask sends that data to the Python model, gets the price, and sends it back to the screen.

---

## 3. Top 5 Viva Questions and Answers

**Q1: Why did you choose Random Forest over Linear Regression?**
> **Answer:** "Airline pricing is very complex and non-linear. A simple Linear Regression tries to draw a straight line through the data, which gave a poor accuracy of 91%. Random Forest combines hundreds of decision trees to capture complex patterns, which boosted my accuracy to 98.56%."

**Q2: How did you handle categorical variables (text data)?**
> **Answer:** "I used Pandas `get_dummies` for One-Hot Encoding to convert nominal data like Airline names and City names into binary numbers (0s and 1s)."

**Q3: Did you do any Feature Scaling?**
> **Answer:** "Yes, I used `StandardScaler` from Scikit-learn. It scales large numbers (like flight duration) down to a standard size so that large numbers don't unfairly dominate the machine learning math."

**Q4: What was the biggest challenge you faced?**
> **Answer:** "The dataset was very large (over 300,000 rows). Training ensemble models like Random Forest on that much data took a lot of computational power and time. Also, One-Hot Encoding created many new columns which increased the dimensionality."

**Q5: Can you explain your `app.py` file?**
> **Answer:** "My `app.py` is the Flask backend. It loads my pre-trained Random Forest model using a library called `joblib`. It has an `@app.route` that listens for the user to submit the HTML form, processes the inputs through my scaler, asks the model for a prediction, and returns the estimated ticket price."
