# Flight Fare Prediction using Machine Learning

An end-to-end Machine Learning regression project and interactive Flask web application to estimate domestic flight ticket fares in India. Developed as part of the **Hybrid Internship Program on Machine Learning through Python** at **ICFOSS (International Centre for Free and Open Source Software)**, Government of Kerala.

---

## 📌 Project Overview
Airline pricing in India is dynamic and non-linear, driven by numerous factors such as travel class, booking timing (days left to departure), route, carrier, and flight duration. This project builds a complete data science and predictive modeling pipeline to accurately forecast domestic flight fares and visualizes price trends through an interactive web portal.

### 🏆 Key Results
- **Best Model**: Random Forest Regressor (200 estimators)
- **R² Score**: **98.56%**
- **Mean Absolute Error (MAE)**: **₹1,250**
- **Root Mean Squared Error (RMSE)**: **₹2,707**
- **Dataset**: 300,153 real domestic flight booking records across 6 major Indian metropolises

---

## 📊 Models Evaluated

| Model | MAE (₹) | RMSE (₹) | R² Score |
|---|---|---|---|
| **Random Forest Regressor** | **1,250** | **2,707** | **0.9856** |
| XGBoost Regressor | 1,599 | 2,880 | 0.9837 |
| Decision Tree Regressor | 1,372 | 3,159 | 0.9804 |
| Linear Regression | 4,476 | 6,731 | 0.9112 |
| Support Vector Regressor (SVR - RBF) | 7,419 | 12,514 | 0.6931 |

---

## 🛠️ Tech Stack & Libraries
- **Language**: Python 3.13
- **Data Manipulation**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-Learn, XGBoost, Joblib
- **Web Deployment**: Flask, HTML5, CSS3, JavaScript
- **Documentation**: LaTeX, python-docx, python-pptx

---

## 📂 Project Structure
```text
├── archive/                     # Dataset files (Clean_Dataset.csv, economy.csv, business.csv)
├── plots/                       # Generated high-resolution visualization charts (300 DPI)
├── saved_models/                # Scalers and feature schemas (best_model.pkl generated upon training)
├── Screenshot of the website/   # Application interface screenshots
├── app.py                       # Flask web server and prediction routing
├── flight_fare_prediction.py    # Complete ML training & evaluation pipeline
├── index.html                   # Interactive web frontend template
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/karthikks2004/Flight-Fare-Prediction-ML.git
cd Flight-Fare-Prediction-ML
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the ML Pipeline (Optional)
To retrain the models and generate all evaluation metrics and plots:
```bash
python flight_fare_prediction.py
```

### 4. Launch the Flask Web Application
```bash
python app.py
```
Open your browser and navigate to **`http://localhost:5000`**.

---

## 👤 Author
**Karthik KS**  
- GitHub: [@karthikks2004](https://github.com/karthikks2004)  
- ICFOSS Hybrid Internship Program on Machine Learning through Python  
- Date: June 2026
