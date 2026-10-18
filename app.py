"""
==============================================================================
 FLIGHT FARE PREDICTION - Flask Web Application
 Machine Learning Project - Evaluation Ready
==============================================================================
 Run: python app.py
 Open: http://localhost:5000
==============================================================================
"""

import os
import sys
import io
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

# Fix Windows encoding
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# ── Setup ───────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'saved_models')

app = Flask(__name__, template_folder=BASE_DIR, static_folder=os.path.join(BASE_DIR, 'plots'))

# ── Load trained model assets ───────────────────────────────────────────────
model = joblib.load(os.path.join(MODEL_DIR, 'best_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.pkl'))

print("[OK] Model loaded successfully!")
print(f"   Features: {len(feature_names)}")


# ── Routes ──────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Accept flight details and return predicted price."""
    try:
        # Get form data
        airline = request.form['airline']
        source = request.form['source_city']
        destination = request.form['destination_city']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        stops = int(request.form['stops'])
        ticket_class = int(request.form['ticket_class'])
        duration = float(request.form['duration'])
        days_left = int(request.form['days_left'])

        # Encode time categories
        time_map = {'Early_Morning': 0, 'Morning': 1, 'Afternoon': 2,
                    'Evening': 3, 'Night': 4, 'Late_Night': 5}

        # Build feature vector
        sample = pd.DataFrame(0, index=[0], columns=feature_names)
        sample['stops'] = stops
        sample['class'] = ticket_class
        sample['duration'] = duration
        sample['days_left'] = days_left
        sample['departure_time'] = time_map[departure_time]
        sample['arrival_time'] = time_map[arrival_time]

        # Set one-hot encoded columns
        airline_col = f"airline_{airline}"
        if airline_col in feature_names:
            sample[airline_col] = 1

        source_col = f"source_city_{source}"
        if source_col in feature_names:
            sample[source_col] = 1

        dest_col = f"destination_city_{destination}"
        if dest_col in feature_names:
            sample[dest_col] = 1

        # Predict
        predicted_price = model.predict(sample)[0]

        # Also predict last-minute price for comparison
        sample_late = sample.copy()
        sample_late['days_left'] = 2
        late_price = model.predict(sample_late)[0]

        return jsonify({
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'late_price': round(late_price, 2),
            'difference': round(late_price - predicted_price, 2),
            'airline': airline.replace('_', ' '),
            'route': f"{source} → {destination}",
            'class': 'Business' if ticket_class == 1 else 'Economy'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/plots/<filename>')
def serve_plot(filename):
    """Serve plot images from the plots directory."""
    return app.send_static_file(filename)


# ── Run ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🌐 Starting Flask server...")
    print("   Open http://localhost:5000 in your browser on PC")
    print("   To access on phone, use your PC's IP address: http://<YOUR_IP>:5000\n")
    app.run(host='0.0.0.0', debug=True, port=5000)
