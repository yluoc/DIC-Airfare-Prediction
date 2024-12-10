### Since the database is too large
### for data preprocessing, data analysis, EDA, LSTM model fitting, download the database from using link: https://www.kaggle.com/datasets/yiclgg/airfare-database. Please rename the first column of cleaned data to idx.


## Airfare Prediction Flask App

This Flask app predicts airfare based on user input.

### Installation

1. Download  the repository:
    ```
   unzip directory
    ```

2. Create a virtual environment and activate it:
    ```
    python3 -m venv venv
    source venv/bin/activate   # For Linux/Mac
    venv\Scripts\activate      # For Windows
    ```

3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

### Training the Model

1. Run the `StackRegressor.py` script to train the Stack Regressor model:
    ```
    python StackRegressor.py
    ```

   This will create a file named `StackRegressor.pkl` which contains the trained model.

### Running the Flask application

1. Start the Flask Application:
   - python app.py
   - Ensure your virtual environment is active when running this command.

2. Access the Website:
   - Open a web browser and navigate to http://127.0.0.1:5000 to use the web interface.

Using the Web Interface
-----------------------

- Input details such as airline, source city, destination city, flight class, number of stops, departure and arrival times.
- Adjust sliders for days left to the flight and flight duration.
- Click "Predict Airfare" to receive the predicted price.
	

### Usage

- Select the airline, source city, destination city, flight class, number of stops, departure time category, and arrival time category.
- Adjust the days left and flight duration sliders as needed.
- Click the "Predict Airfare" button to get the predicted airfare.
