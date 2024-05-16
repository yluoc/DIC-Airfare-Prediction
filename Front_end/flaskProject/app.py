from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import random
import os

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, 'RF.pkl')

with open(path, 'rb') as f:
    trained_model = pickle.load(f)

@app.route('/')
@app.route('/')
def index():
    # Example data for dropdowns
    airlines = ["SpiceJet", "AirAsia", "Vistara", "GO FIRST", "Indigo", "Air India", "Trujet"]
    cities = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
    flight_classes = ["Business", "Economy"]
    stops = ["non-stop", "1-stop", "2+-stop"]
    times = ["Evening", "Early Morning", "Morning", "Afternoon", "Night"]
    return render_template('index.html', airlines=airlines, cities=cities, flight_classes=flight_classes, stops=stops, times=times)


@app.route('/predict', methods=['POST'])
def predict_airfare():
    data = request.form
    max_days_left = int(data.get('days_left', 22))  # Get the maximum days left from the form

    # Prepare data that doesn't change with days left
    airline_map = {'SpiceJet': 0, 'AirAsia': 1, 'Vistara': 2, 'GO FIRST': 3, 'Indigo': 4, 'Air India': 5, 'Trujet': 6}
    source_city_map = {'Delhi': 0, 'Mumbai': 1, 'Bangalore': 2, 'Kolkata': 3, 'Hyderabad': 4, 'Chennai': 5}
    dest_city_map = {'Delhi': 0, 'Mumbai': 1, 'Bangalore': 2, 'Kolkata': 3, 'Hyderabad': 4, 'Chennai': 5}
    dep_time_category_map = {'Evening': 0, 'Early Morning': 1, 'Morning': 2, 'Afternoon': 3, 'Night': 4}
    arr_time_category_map = {'Evening': 0, 'Early Morning': 1, 'Morning': 2, 'Afternoon': 3, 'Night': 4}
    stop_map = {'non-stop': 0, '1-stop': 1, '2+-stop': 2}
    flight_class_map = {"Business": 1, "Economy": 0}

    # Initialize a list to hold each day's DataFrame
    data_frames = []
    results = []
    for day in range(0, max_days_left + 1):
        user_input = {
            'Days_Left': day,
            'airline': airline_map.get(data.get('airline'), -1),
            'source_city': source_city_map.get(data.get('source_city'), -1),
            'destinate_city': dest_city_map.get(data.get('dest_city'), -1),
            'Class': flight_class_map.get(data.get('flight_class'), -1),
            'time_taken': int(data.get('flight_duration', 6)),
            'stop': stop_map.get(data.get('num_stops'), 2),
            'dep_time_category': dep_time_category_map.get(data.get('dep_time_category'), -1),
            'arr_time_category': arr_time_category_map.get(data.get('arr_time_category'), -1)
        }
        user_input_df = pd.DataFrame([user_input])

        try:
            prediction = trained_model.predict(user_input_df)
            results.append({'days_left': day, 'predicted_price': float(prediction[0])})
        except Exception as e:
            print(f"Error predicting for day {day}: {str(e)}")
            continue
    print(results)
    results=results[::-1]
    print(results)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
