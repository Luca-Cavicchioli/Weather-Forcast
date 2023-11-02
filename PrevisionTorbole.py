import pandas as pd

data = pd.read_csv('OpenMeteoTorbole.csv', skiprows=2)

data.columns = ['time', 'temperature', 'relativehumidity', 'precipitation', 'cloudcover', 'windspeed']

print(data.head())

data['time'] = pd.to_datetime(data['time'])
data['day_of_year'] = data['time'].dt.dayofyear

averages = data.groupby('day_of_year').mean()

data['average_temperature'] = data['day_of_year'].map(averages['temperature'])
prob = (data['temperature'] > data['average_temperature']).mean()

print(prob)
