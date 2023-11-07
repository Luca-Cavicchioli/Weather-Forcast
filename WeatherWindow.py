import tkinter as tk
from tkcalendar import DateEntry
import pandas as pd

import BayesianTorbole 

def print_date(date):
     # Convert the selected date to day of year
    day_of_year = date.get_date().timetuple().tm_yday

    # Create a DataFrame representing the scenario you want to predict
    scenario = pd.DataFrame({'day_of_year': [day_of_year]})

    # Use the model to predict the weather parameters for this scenario
    predictions = BayesianTorbole.model.predict(scenario)

    # Convert the predictions to a string
    results_text = '\n'.join(f'{param}: {result}' for param, result in predictions.items())

    # Display the predictions
    results_label.config(text=results_text)
    '''
    print(date.get_date())
    selected_params = [param for param, var in param_vars.items() if var.get()]
    # Here you would call your Bayesian network function and get the results
    # For now, I'll just use some dummy results
    all_results = {
        'Temperature': 'Hot (70%)',
        'Precipitation': 'None (80%)',
        'Humidity': 'Low (60%)',
        'Cloud Cover': 'Clear (90%)',
        'Wind Speed': 'Moderate (50%)'
    }
    results = {param: all_results[param] for param in selected_params}
    results_text = '\n'.join(f'{param}: {result}' for param, result in results.items())
    results_label.config(text=results_text)
    '''

root = tk.Tk()
root.title("Weather Torbole")
root.configure(bg='#ADD8E6')

date_entry = DateEntry(root, width=20, background='blue', 
                       foreground='white', borderwidth=2, font=('Helvetica', 14, 'bold'))
date_entry.pack(padx=10, pady=10)

weather_params = ['Temperature', 'Precipitation', 'Humidity', 'Cloud Cover', 'Wind Speed']
param_vars = {param: tk.BooleanVar() for param in weather_params}

for param, var in param_vars.items():
    cb = tk.Checkbutton(root, text=param, variable=var, bg='#ADD8E6', fg='blue', selectcolor='black')
    cb.pack(padx=10, pady=2)

button = tk.Button(root, text="OK", command=lambda: print_date(date_entry), 
                   bg='blue', fg='white', font=('Helvetica', 14, 'bold'))
button.pack(padx=10, pady=10)

results_label = tk.Label(root, text='', bg='#ADD8E6', fg='blue', font=('Helvetica', 14, 'bold'))
results_label.pack(padx=10, pady=10)

root.mainloop()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing

