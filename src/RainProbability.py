#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np

import FinalWindow as fw
#file_address="https://archive-api.open-meteo.com/v1/archive?latitude=45.508256&longitude=10.13164&start_date=2010-01-01&end_date=2019-12-31&hourly=temperature_2m,relativehumidity_2m,precipitation,cloudcover,windspeed_10m&timezone=Europe%2FBerlin"

#file = pd.read_json(file_address, orient="records")
#print(file)
def calculate_rain_probabilities(target_month, target_hour):


    file2 = pd.read_csv("OpenMeteoTorbole.csv", skiprows=2)



    non_filtered_df = file2.drop(columns =['windspeed_10m (km/h)'])

    #print(non_filtered_df.head())

#print(non_filtered_df.shape)


    '''
    def filter_by_month(non_filtered_df, target_month):
        # Converti la colonna 'time' in formato datetime
        non_filtered_df['time'] = pd.to_datetime(non_filtered_df['time'])
        
        # Estrai il mese dalla colonna 'time'
        non_filtered_df['month'] = non_filtered_df['time'].dt.month
        
        # Filtra il DataFrame in base al mese specificato
        df = non_filtered_df[non_filtered_df['month'] == target_month]
        
        # Rimuovi la colonna 'month' se non necessaria
        df = df.drop(columns=['month'])
        
        return df
    '''



    def filter_by_month_and_day_period(non_filtered_df, target_month, target_day_period):
        # Convert the 'time' column to datetime format
        non_filtered_df['time'] = pd.to_datetime(non_filtered_df['time'])
        
        # Extract the month from the 'time' column
        non_filtered_df['month'] = non_filtered_df['time'].dt.month
        
        # Extract the hour from the 'time' column
        non_filtered_df['hour'] = non_filtered_df['time'].dt.hour

        # Create the 'day_period' column
        non_filtered_df['day_period'] = non_filtered_df['hour'].apply(get_day_period_from_hour)
        
        # Filter the DataFrame based on the specified month and day period
        df = non_filtered_df[(non_filtered_df['month'] == target_month) & (non_filtered_df['day_period'] == target_day_period)]
        
        # Remove the 'month', 'hour', and 'day_period' columns if not needed
        df = df.drop(columns=['month', 'hour', 'day_period'])
        
        return df

    # Import the script where the window is defined
    from FinalWindow import get_weather_forecast

    # Call the function to get target_month and target_day_period
    target_month, target_hour = get_weather_forecast()

    def get_day_period_from_hour(hour):
        if 23 <= hour or hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'


    target_day_period = get_day_period_from_hour(target_hour)
    print(target_day_period)
    # Sostituisci 'target_month' con il numero del mese desiderato (1 per gennaio, 2 per febbraio, ecc.)
    df = filter_by_month_and_day_period(non_filtered_df, target_month=target_month, target_day_period=target_day_period)



    #print(df.head())

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


    temperature_conditions = ['Cold', 'Mild', 'Hot']
    humidity_conditions = ['Low', 'High']
    cloudcover_conditions = ['Clear', 'Cloudy']
    precipitation_conditions = ['None', 'Yes']


    '''
    for temp_condition in temperature_conditions:
        for precip_condition in precipitation_conditions:
            count_yes = df[(df['temperature'] == temp_condition) & (df['precipitation'] == precip_condition)].shape[0]
            count_no = df[(df['temperature'] != temp_condition) | (df['precipitation'] != precip_condition)].shape[0]

            temp_prob_yes = count_yes / df.shape[0]
            temp_prob_no = count_no / df.shape[0]

            print(f"{temp_condition}_{precip_condition}_yes: {temp_prob_yes}")
            print(f"{temp_condition}_{precip_condition}_no: {temp_prob_no}")



    for humi_condition in humidity_conditions:
        for precip_condition in precipitation_conditions:
            count_yes = df[(df['relativehumidity'] == humi_condition) & (df['precipitation'] == precip_condition)].shape[0]
            count_no = df[(df['relativehumidity'] != humi_condition) | (df['precipitation'] != precip_condition)].shape[0]

            humi_prob_yes = count_yes / df.shape[0]
            humi_prob_no = count_no / df.shape[0]

            print(f"{humi_condition}_{precip_condition}_yes: {humi_prob_yes}")
            print(f"{humi_condition}_{precip_condition}_no: {humi_prob_no}")

    for cloud_condition in cloudcover_conditions:
        for precip_condition in precipitation_conditions:
            count_yes = df[(df['cloudcover'] == cloud_condition) & (df['precipitation'] == precip_condition)].shape[0]
            count_no = df[(df['cloudcover'] != cloud_condition) | (df['precipitation'] != precip_condition)].shape[0]

            cloud_prob_yes = count_yes / df.shape[0]
            cloud_prob_no = count_no / df.shape[0]

            print(f"{cloud_condition}_{precip_condition}_yes: {cloud_prob_yes}")
            print(f"{cloud_condition}_{precip_condition}_no: {cloud_prob_no}")
    '''
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


    # Calculate marginal probabilities for individual weather conditions
    temperature_probabilities = df['temperature'].value_counts(normalize=True)
    relativehumidity_probabilities = df['relativehumidity'].value_counts(normalize=True)
    precipitation_probabilities = df['precipitation'].value_counts(normalize=True)
    cloudcover_probabilities = df['cloudcover'].value_counts(normalize=True)

    '''
    # Print marginal probabilities
    print("Marginal probabilities for temperature:")
    print(temperature_probabilities)

    print("\nMarginal probabilities for humidity:")
    print(relativehumidity_probabilities)

    print("\nMarginal probabilities for precipitation:")
    print(precipitation_probabilities)

    print("\nMarginal probabilities for cloud cover:")
    print(cloudcover_probabilities)

    print(cpd_rain_values)

    print(df.head())

    '''









    '''
    print(df.shape[0])

    cold_yes = 0
    cold_no = 0
    mild_yes = 0
    mild_no = 0
    hot_yes = 0
    hot_no = 0

    for i in range (df.shape[0]):
        if df['temperature'][i] == "Cold" and df['precipitation'][i] == "Yes":
            cold_yes+=1
        if df['temperature'][i] == "Cold" and df['precipitation'][i] == "None":
            cold_no+=1
        if df['temperature'][i] == "Mild" and df['precipitation'][i] == "Yes":
            mild_yes+=1
        if df['temperature'][i] == "Mild" and df['precipitation'][i] == "None":
            mild_no+=1 
        if df['temperature'][i] == "Hot" and df['precipitation'][i] == "Yes":
            hot_yes+=1
        if df['temperature'][i] == "Hot" and df['precipitation'][i] == "None":
            hot_no+=1 
    print("cold_yes : " + str(cold_yes/df.shape[0]))
    print("cold_no : " + str(cold_no/df.shape[0]))
    print("mild_yes : " + str(mild_yes/df.shape[0]))
    print("mild_no : " + str(mild_no/df.shape[0]))
    print("hot_yes : " + str(hot_yes/df.shape[0]))
    print("hot_no : " + str(hot_no/df.shape[0]))


    high_yes = 0
    high_no = 0
    low_yes = 0
    low_no = 0

    for i in range (df.shape[0]):
        if df['relativehumidity'][i] == "High" and df['precipitation'][i] == "Yes":
            high_yes+=1
        if df['relativehumidity'][i] == "High" and df['precipitation'][i] == "None":
            high_no+=1
        if df['relativehumidity'][i] == "Low" and df['precipitation'][i] == "Yes":
            low_yes+=1
        if df['relativehumidity'][i] == "Low" and df['precipitation'][i] == "None":
            low_no+=1 
    print("high_yes : " + str(high_yes/df.shape[0]))
    print("high_no : " + str(high_no/df.shape[0]))
    print("low_yes : " + str(low_yes/df.shape[0]))
    print("low_no : " + str(low_no/df.shape[0]))

    clear_yes = 0
    clear_no = 0
    cloudy_yes = 0
    cloudy_no = 0

    for i in range (df.shape[0]):
        if df['cloudcover'][i] == "Clear" and df['precipitation'][i] == "Yes":
            clear_yes+=1
        if df['cloudcover'][i] == "Clear" and df['precipitation'][i] == "None":
            clear_no+=1
        if df['cloudcover'][i] == "Cloudy" and df['precipitation'][i] == "Yes":
            cloudy_yes+=1
        if df['cloudcover'][i] == "Cloudy" and df['precipitation'][i] == "None":
            cloudy_no+=1 
    print("clear_yes : " + str(clear_yes/df.shape[0]))
    print("clear_no : " + str(clear_no/df.shape[0]))
    print("cloudy_yes : " + str(cloudy_yes/df.shape[0]))
    print("cloudy_no : " + str(cloudy_no/df.shape[0]))

    '''




