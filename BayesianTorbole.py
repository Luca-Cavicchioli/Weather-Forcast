import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator


data = pd.read_csv('OpenMeteoTorbole.csv', skiprows=2)

data.columns = ['time', 'temperature', 'relativehumidity', 'precipitation', 'cloudcover', 'windspeed']


# Convert time to datetime and extract day of year
data['time'] = pd.to_datetime(data['time'])
data['day_of_year'] = data['time'].dt.dayofyear

# Categorize the weather parameters
data['temperature'] = pd.cut(data['temperature'], bins=[-np.inf, 10, 25, np.inf], labels=['Cold', 'Mild', 'Hot'])
data['relativehumidity'] = pd.cut(data['relativehumidity'], bins=[0, 30, 70, 100], labels=['Low', 'Medium', 'High'])
data['precipitation'] = pd.cut(data['precipitation'], bins=[0, 1, np.inf], labels=['None', 'Yes'])
data['cloudcover'] = pd.cut(data['cloudcover'], bins=[0, 30, 100], labels=['Clear', 'Cloudy'])
data['windspeed'] = pd.cut(data['windspeed'], bins=[0, 15, np.inf], labels=['Calm', 'Windy'])

# Define the model structure
model = BayesianModel([('day_of_year', 'temperature'), 
                       ('day_of_year', 'relativehumidity'), 
                       ('day_of_year', 'precipitation'), 
                       ('day_of_year', 'cloudcover'), 
                       ('day_of_year', 'windspeed')])

# Fit the data to the model using Maximum Likelihood Estimation
model.fit(data, estimator=MaximumLikelihoodEstimator)


# Make the model available for import
bayesian_model = model