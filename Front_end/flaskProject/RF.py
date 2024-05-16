import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

df = pd.read_csv('../../database/cleaned_data.csv')

df['Class'] = df['Class'].replace({'Economy': 0, 'Business': 1})
df['stop'] = df['stop'].replace({'non-stop': 0, '1-stop': 1, '2+-stop': 2})
df['airline'] = df['airline'].replace({'SpiceJet': 0, 'AirAsia': 1, 'Vistara': 2, 'GO FIRST': 3, 'Indigo': 4, 'Air India': 5, 'Trujet': 6,
 'StarAir': 7})
df['source_city'] = df['source_city'].replace({'Delhi': 0, 'Mumbai': 1, 'Bangalore': 2, 'Kolkata': 3, 'Hyderabad': 4, 'Chennai': 5})
df['destinate_city'] = df['destinate_city'].replace({'Delhi': 0, 'Mumbai': 1, 'Bangalore': 2, 'Kolkata': 3, 'Hyderabad': 4, 'Chennai': 5})
df['dep_time_category'] = df['dep_time_category'].replace({'Evening': 0, 'Early Morning': 1, 'Morning': 2, 'Afternoon': 3, 'Night': 4})
df['arr_time_category'] = df['arr_time_category'].replace({'Evening': 0, 'Early Morning': 1, 'Morning': 2, 'Afternoon': 3, 'Night': 4})

x, y = df[['Days_Left', 'airline', 'source_city', 'destinate_city', 'Class', 'time_taken', 'stop', 'dep_time_category', 'arr_time_category']], df['price']

x_train, y_train = x, y

reg_rf = RandomForestRegressor()
reg_rf.fit(x_train, y_train)

with open('../Trained_Models_file/RF.pkl', 'wb') as file:
    pickle.dump(reg_rf, file)