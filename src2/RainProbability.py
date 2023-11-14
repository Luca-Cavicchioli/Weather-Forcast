import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import ParameterEstimator
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

file2 = pd.read_csv(r"C:\Users\temug\Desktop\ProgettiPython\Previsionimeteo\src2\OpenMeteoTorbole.csv", skiprows=2)
non_filtered_df = file2.drop(columns =['windspeed_10m (km/h)'])
temperature_conditions = ['Cold', 'Mild', 'Hot']
humidity_conditions = ['Low', 'High']
cloudcover_conditions = ['Clear', 'Cloudy']
precipitation_conditions = ['None', 'Yes']
 
class Calculate_probabilities():
    
    def __init__(self, target_month, target_hour):    
        
        #target_month, target_hour = get_weather_forecast()
        target_day_period = self.get_day_period_from_hour(target_hour)
        print(target_day_period)
        
        df = self.filter_by_month_and_day_period(non_filtered_df, target_month=target_month, target_day_period=target_day_period)



        df.rename(columns=dict(zip(list(df.columns), list(['time', 'temperature', 'relativehumidity', 'precipitation', 'cloudcover']))), inplace=True)
        df

        average_temperature = df['temperature'].mean()
        average_cloud = df['cloudcover'].mean()
        print("Average temperature: ", average_temperature)
        print("Average Cloudcover", average_cloud)

        df['temperature'] = pd.cut(df['temperature'], bins=[-np.inf, 10, 19, np.inf], labels=['Cold', 'Mild', 'Hot'])
        df['relativehumidity'] = pd.cut(df['relativehumidity'], bins=[0, 50, 100], labels=['Low', 'High'])
        df['precipitation'] = pd.cut(df['precipitation'], bins=[0, 1, np.inf], labels=['None', 'Yes'])
        df['cloudcover'] = pd.cut(df['cloudcover'], bins=[0, 50, 100], labels=['Clear', 'Cloudy'])
        df

        df = df.dropna()
        df = df.reset_index(drop=True)
        self.cpd_rain_values = self.conditioned_probability(df)

        # Call the calculate_bayesian_network method on the instance
        # Replace 'df' with your actual DataFrame
        rain_prob = self.calculate_bayesian_network(df)

        print(rain_prob)
        

        

    def filter_by_month_and_day_period(self, non_filtered_df, target_month, target_day_period):
        # Convert the 'time' column to datetime format
        non_filtered_df['time'] = pd.to_datetime(non_filtered_df['time'])
        
        # Extract the month from the 'time' column
        non_filtered_df['month'] = non_filtered_df['time'].dt.month
        
        # Extract the hour from the 'time' column
        non_filtered_df['hour'] = non_filtered_df['time'].dt.hour

        # Create the 'day_period' column
        non_filtered_df['day_period'] = non_filtered_df['hour'].apply(self.get_day_period_from_hour)
        
        # Filter the DataFrame based on the specified month and day period
        df = non_filtered_df[(non_filtered_df['month'] == target_month) & (non_filtered_df['day_period'] == target_day_period)]
        
        # Remove the 'month', 'hour', and 'day_period' columns if not needed
        df = df.drop(columns=['month', 'hour', 'day_period'])
        
        return df

    # Call the function to get target_month and target_day_period
    

    def get_day_period_from_hour(self, hour):
        if 23 <= hour or hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'
        
    def calculate_bayesian_network(self, df):

        
    # Assuming you have already calculated the probabilities and stored them in variables like below
    # You can replace these with your actual probability values

        temperature_probabilities = df['temperature'].value_counts(normalize=True)
        relativehumidity_probabilities = df['relativehumidity'].value_counts(normalize=True)
        precipitation_probabilities = df['precipitation'].value_counts(normalize=True)
        cloudcover_probabilities = df['cloudcover'].value_counts(normalize=True)

        # Define the structure of the Bayesian Network
        model = BayesianNetwork([('temperature', 'precipitation'), ('relativehumidity', 'precipitation'), ('cloudcover', 'precipitation')])

        temperature_probabilities_2d = [[temperature_probabilities.iloc[i]] for i in range(len(temperature_probabilities))]
        relativehumidity_probabilities_2d = [[relativehumidity_probabilities.iloc[i]] for i in range(len(relativehumidity_probabilities))]
        cloudcover_probabilities_2d = [[cloudcover_probabilities.iloc[i]] for i in range(len(cloudcover_probabilities))]
    
        cpd_temp = TabularCPD(variable='temperature', variable_card=3, values=temperature_probabilities_2d, state_names={'temperature':['Cold', 'Mild', 'Hot']})
        cpd_hum = TabularCPD(variable='relativehumidity', variable_card=2, values=relativehumidity_probabilities_2d, state_names={'relativehumidity':['Low', 'High']})
        cpd_cloud = TabularCPD(variable='cloudcover', variable_card=2, values=cloudcover_probabilities_2d, state_names={'cloudcover':['Clear', 'Cloudy']})

        cpd_rain_values = self.conditioned_probability(df)
        cpd_rain_values_transposed = list(map(list, zip(*cpd_rain_values)))

        cpd_rain = TabularCPD(
            'precipitation',
            2, 
            cpd_rain_values_transposed, 
            evidence=['temperature','relativehumidity','cloudcover'],
            evidence_card=[3,2,2],
            state_names={'temperature':['Cold', 'Mild', 'Hot'], 'relativehumidity':['Low', 'High'],'cloudcover':['Clear', 'Cloudy'],'precipitation':['Yes','No']}

        )

        model.add_cpds(cpd_temp)

        model.add_cpds(cpd_hum)

        model.add_cpds(cpd_cloud)

        model.add_cpds(cpd_rain)


        infer = VariableElimination(model)

        most_probable_temperature = temperature_probabilities.idxmax()
        most_probable_humidity = relativehumidity_probabilities.idxmax()
        most_probable_cloudcover = cloudcover_probabilities.idxmax()

        print(most_probable_temperature)
        print(most_probable_humidity)
        print(most_probable_cloudcover)
        # Set the evidence as these states
        evidence = {'temperature': most_probable_temperature, 'relativehumidity': most_probable_humidity, 'cloudcover': most_probable_cloudcover}

        rain_prob = infer.query(variables=['precipitation'], evidence=evidence)

        # Print the result
        print(rain_prob)
        return rain_prob
    
    def conditioned_probability(self, df):
            cpd_rain_values = []

            # Loop over all combinations of conditions
            for temp_condition in temperature_conditions:
                for humi_condition in humidity_conditions:
                    for cloud_condition in cloudcover_conditions:
                        # Calculate the probabilities for each combination
                        count_yes = df[(df['temperature'] == temp_condition) & (df['relativehumidity'] == humi_condition) & (df['cloudcover'] == cloud_condition) & (df['precipitation'] == 'Yes')].shape[0]
                        count_no = df[(df['temperature'] == temp_condition) & (df['relativehumidity'] == humi_condition) & (df['cloudcover'] == cloud_condition) & (df['precipitation'] == 'None')].shape[0]
                        
                        total = count_yes + count_no
                        prob_yes = count_yes / total if total != 0 else 0
                        prob_no = count_no / total if total != 0 else 1
                        
                        # Add the probabilities to the cpd_rain_values list
                        cpd_rain_values.append([prob_yes, prob_no])
            return cpd_rain_values

        
