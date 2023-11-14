import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
from RainProbability import Calculate_probabilities
import RainProbability as rp

def get_weather_forecast():
    date = date_var.get()
    time = time_entry.get()
    # Extract the month from the selected date
    target_month = pd.to_datetime(date).month
    # Determine the day period from the chosen time
    target_hour = int(time.split(':')[0])

    print(target_month)
    print(target_hour)



    selected_parameters = []

    if temperature_var.get():
        selected_parameters.append("Temperature")

    if precipitation_var.get():
        selected_parameters.append("Precipitation")

    if humidity_var.get():
        selected_parameters.append("Humidity")

    if cloudcover_var.get():
        selected_parameters.append("Cloud Cover")

    # Call the functions from RainProbability and FinalBayesian
    # Create an instance of Calculate_probabilities
    instance = Calculate_probabilities(target_month, target_hour)

    # Call the calculate_bayesian_network method
    rain_prob = instance.calculate_bayesian_network()
    print(rain_prob)
    

    result_label.config(text=f"Weather forecast for {date} at {time} with parameters: {', '.join(selected_parameters)}")
    return target_month, target_hour



def open_calendar():
    cal_window = tk.Toplevel(window)
    cal = Calendar(cal_window, selectmode="day", year=2023, month=11, day=12)
    cal.pack()

    def set_date():
        date_var.set(cal.get_date())
        cal_window.destroy()

    set_date_button = ttk.Button(cal_window, text="Set Date", command=set_date)
    set_date_button.pack()

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


# Create the main window
window = tk.Tk()
window.title("Weather Forecast")
window.geometry("600x400")  # Set the desired width and height

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

parameters_label = ttk.Label(window, text="Select Parameters:")
parameters_label.grid(row=3, column=0, padx=10, pady=10)

temperature_var = tk.BooleanVar()
precipitation_var = tk.BooleanVar()
humidity_var = tk.BooleanVar()
cloudcover_var = tk.BooleanVar()

temperature_checkbox = ttk.Checkbutton(window, text="Temperature", variable=temperature_var)
temperature_checkbox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

precipitation_checkbox = ttk.Checkbutton(window, text="Precipitation", variable=precipitation_var)
precipitation_checkbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

humidity_checkbox = ttk.Checkbutton(window, text="Humidity", variable=humidity_var)
humidity_checkbox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

cloudcover_checkbox = ttk.Checkbutton(window, text="Cloud Cover", variable=cloudcover_var)
cloudcover_checkbox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

# Add more checkboxes for other parameters as needed

get_forecast_button = ttk.Button(window, text="Get Forecast", command=get_weather_forecast)
get_forecast_button.grid(row=8, column=0, columnspan=2, pady=10)

result_label = ttk.Label(window, text="")
result_label.grid(row=6, column=0, columnspan=2, pady=10)

# Run the main loop
window.mainloop()
