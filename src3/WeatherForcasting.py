import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

#define dataset, remove columns not needed and define intervals for the parameters considered
file2 = pd.read_csv("OpenMeteoTorbole.csv", skiprows=2)
non_filtered_df = file2.drop(columns =['windspeed_10m (km/h)'])
temperature_conditions = ['Cold', 'Mild', 'Hot']
humidity_conditions = ['Low', 'High']
cloudcover_conditions = ['Clear', 'Cloudy']
precipitation_conditions = ['None', 'Yes']

#this function will convert time in a day period to semplify the search
def get_day_period_from_hour(hour):
        if 23 <= hour or hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'

#bayesian network function for finding rain probability
def calculate_bayesian_network(df):

    #probabilities of the parameters used
    temperature_probabilities = df['temperature'].value_counts(normalize=True)
    relativehumidity_probabilities = df['relativehumidity'].value_counts(normalize=True)
    cloudcover_probabilities = df['cloudcover'].value_counts(normalize=True)

    # Structure of the Bayesian Network
    model = BayesianNetwork([('temperature', 'precipitation'), ('relativehumidity', 'precipitation'), ('cloudcover', 'precipitation')])

    temperature_probabilities_2d = [[temperature_probabilities.iloc[i]] for i in range(len(temperature_probabilities))]
    relativehumidity_probabilities_2d = [[relativehumidity_probabilities.iloc[i]] for i in range(len(relativehumidity_probabilities))]
    cloudcover_probabilities_2d = [[cloudcover_probabilities.iloc[i]] for i in range(len(cloudcover_probabilities))]

    #CPDs for the three parameters using the probabilities considered before
    cpd_temp = TabularCPD(variable='temperature', variable_card=3, values=temperature_probabilities_2d, state_names={'temperature':['Cold', 'Mild', 'Hot']})
    cpd_hum = TabularCPD(variable='relativehumidity', variable_card=2, values=relativehumidity_probabilities_2d, state_names={'relativehumidity':['Low', 'High']})
    cpd_cloud = TabularCPD(variable='cloudcover', variable_card=2, values=cloudcover_probabilities_2d, state_names={'cloudcover':['Clear', 'Cloudy']})

    #we use the function conditioned_probability to find the probability of rain depending on the three parameters
    cpd_rain_values = conditioned_probability(df)
    cpd_rain_values_transposed = list(map(list, zip(*cpd_rain_values)))

    #cpd for rain
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

    result_label = tk.Label(window, text=f"Temperature: {most_probable_temperature}")
    result_label.grid(row=20, column=15, padx=10, pady=10)
    result_label = tk.Label(window, text=f"Humidity: {most_probable_humidity}")
    result_label.grid(row=25, column=15, padx=10, pady=10)
    result_label = tk.Label(window, text=f"Cloudcover: {most_probable_cloudcover}")
    result_label.grid(row=30, column=15, padx=10, pady=10)

    #considering the most probable case we create an evidence that will be used in the bayesian to get the probability of rain
    evidence = {'temperature': most_probable_temperature, 'relativehumidity': most_probable_humidity, 'cloudcover': most_probable_cloudcover}

    rain_prob = infer.query(variables=['precipitation'], evidence=evidence)

    result_label = tk.Label(window, text=f"Rain probability: {rain_prob}")
    result_label.grid(row=40, column=15, padx=10, pady=10)

    return rain_prob

#this function searches the conditioned probabilities inside the df. we use them inside the cpd rain
def conditioned_probability(df):
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

#this function returns the df only with the month of interest and the target day period that we want to predict
def filter_by_month_and_day_period(non_filtered_df, target_month, target_day_period):
        # cast the time column to datetime and create columns for month hour and day period
        non_filtered_df['time'] = pd.to_datetime(non_filtered_df['time'])
        non_filtered_df['month'] = non_filtered_df['time'].dt.month
        non_filtered_df['hour'] = non_filtered_df['time'].dt.hour
        non_filtered_df['day_period'] = non_filtered_df['hour'].apply(get_day_period_from_hour)

        df = non_filtered_df[(non_filtered_df['month'] == target_month) & (non_filtered_df['day_period'] == target_day_period)]
        
        df = df.drop(columns=['month', 'hour', 'day_period'])
        
        return df

#this function is used to make the changes needed to the df and to have the results we need
def bayesian(target_month, target_hour):

    target_day_period = get_day_period_from_hour(target_hour)

    df = filter_by_month_and_day_period(non_filtered_df, target_month, target_day_period)
    df = df.dropna()
    df = df.reset_index(drop=True)
    #cpd_rain_values = conditioned_probability(df)
    
    df.rename(columns=dict(zip(list(df.columns), list(['time', 'temperature', 'relativehumidity', 'precipitation', 'cloudcover']))), inplace=True)

    df['temperature'] = pd.cut(df['temperature'], bins=[-np.inf, 10, 19, np.inf], labels=['Cold', 'Mild', 'Hot'])
    df['relativehumidity'] = pd.cut(df['relativehumidity'], bins=[0, 50, 100], labels=['Low', 'High'])
    df['precipitation'] = pd.cut(df['precipitation'], bins=[0, 1, np.inf], labels=['None', 'Yes'])
    df['cloudcover'] = pd.cut(df['cloudcover'], bins=[0, 50, 100], labels=['Clear', 'Cloudy'])

    rain_prob = calculate_bayesian_network(df)

    print(rain_prob)


########
#window#
########

#this function opens the calendar to chose the date
def open_calendar():
    cal_window = tk.Toplevel(window)
    cal = Calendar(cal_window, selectmode="day", year=2023, month=11, day=12)
    cal.pack()

    def set_date():
        date_var.set(cal.get_date())
        cal_window.destroy()

    set_date_button = ttk.Button(cal_window, text="Set Date", command=set_date)
    set_date_button.pack()

#this funtion permits to chose the time of the day
def open_time_selector():
    time_selector_window = tk.Toplevel(window)

    hours = list(range(24))
    time_selector_listbox = tk.Listbox(time_selector_window, selectmode=tk.SINGLE, exportselection=0)
    for hour in hours:
        time_selector_listbox.insert(tk.END, f"{hour}:00")

    def set_time():
        selected_index = time_selector_listbox.curselection()
        if selected_index:
            selected_time = time_selector_listbox.get(selected_index)
            time_var.set(selected_time)
        time_selector_window.destroy()

    set_time_button = ttk.Button(time_selector_window, text="Set Time", command=set_time)
    set_time_button.pack()

    time_selector_listbox.pack()

#this is the function that starts the prediction when we press the button for weather forecasting

def get_weather_forecast():
    
    date = date_var.get()
    time = time_entry.get()
    print(date)
    # Extract the month from the selected date
    target_month = pd.to_datetime(date).month
    # Determine the day period from the chosen time
    target_hour = int(time.split(':')[0])
    
    bayesian(target_month, target_hour)
    

# Create the main window
window = tk.Tk()
window.title("Weather Forecast")
window.geometry("800x600")  # Set the desired width and height

# Set the background color
window.configure(bg="#87CEEB")



date_label = ttk.Label(window, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_var = tk.StringVar()
date_entry = ttk.Entry(window, textvariable=date_var, state="readonly")
date_entry.grid(row=0, column=1, padx=10, pady=10)

date_button = ttk.Button(window, text="Select Date", command=open_calendar)
date_button.grid(row=0, column=2, padx=10, pady=10)

time_label = ttk.Label(window, text="Time:")
time_label.grid(row=1, column=0, padx=10, pady=10)
time_var = tk.StringVar()
time_entry = ttk.Entry(window, textvariable=time_var, state="readonly")
time_entry.grid(row=1, column=1, padx=10, pady=10)

time_button = ttk.Button(window, text="Select Time", command=open_time_selector)
time_button.grid(row=1, column=2, padx=10, pady=10)

position_label = ttk.Label(window, text="Postion: Torbole Casaglia (BS, Italy):")
position_label.grid(row=1, column=30, padx=10, pady=10)

get_forecast_button = ttk.Button(window, text="Get Forecast", command=get_weather_forecast)
get_forecast_button.grid(row=8, column=0, columnspan=2, pady=10)

window.mainloop()