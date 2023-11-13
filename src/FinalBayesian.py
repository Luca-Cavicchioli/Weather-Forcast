from pgmpy.models import BayesianNetwork
from pgmpy.estimators import ParameterEstimator
from pgmpy.inference import VariableElimination
import pandas as pd
from pgmpy.factors.discrete import TabularCPD
import RainProbability as rp


def calculate_bayesian_network(target_month, target_hour):

    
# Assuming you have already calculated the probabilities and stored them in variables like below
# You can replace these with your actual probability values
    temperature_probabilities = rp.temperature_probabilities
    relativehumidity_probabilities = rp.relativehumidity_probabilities
    cloudcover_probabilities = rp.cloudcover_probabilities
    precipitation_probabilities = rp.precipitation_probabilities
    
        
    '''
    temp_prob_yes = rp.temp_prob_yes
    temp_prob_no = rp.temp_prob_no

    humi_prob_yes = rp.humi_prob_yes
    humi_prob_no = rp.humi_prob_no

    cloud_prob_yes = rp.cloud_prob_yes
    cloud_prob_no = rp.cloud_prob_no

    # Create a DataFrame with the calculated probabilities
    data = {
        'temperature': temperature_probabilities.index,
        'relativehumidity': relativehumidity_probabilities.index,
        'cloudcover': cloudcover_probabilities.index,
        'precipitation': precipitation_probabilities.index,
        'temp_precipitation': temp_prob_yes, 
        'humi_precipitation': humi_prob_yes,
        'cloud_precipitation': cloud_prob_yes
    }
    #df_probabilities = pd.DataFrame(data)
    '''
    # Define the structure of the Bayesian Network
    model = BayesianNetwork([('temperature', 'precipitation'), ('relativehumidity', 'precipitation'), ('cloudcover', 'precipitation')])

    # Fit the Conditional Probability Distributions using the calculated probabilities
    #model.fit(df_probabilities, estimator=ParameterEstimator)

    # Perform Variable Elimination for inference
    #inference = VariableElimination(model)

    # Example: Query the probability of precipitation given specific conditions
    #query_result = inference.query(variables=['precipitation'], evidence={'temperature': 'Mild', 'relativehumidity': 'High', 'cloudcover': 'Cloudy'})
    #print(query_result)

    # In [1]
    #print(list(temperature_probabilities))

    # In[1]
    temperature_probabilities_2d = [[temperature_probabilities.iloc[i]] for i in range(len(temperature_probabilities))]
    relativehumidity_probabilities_2d = [[relativehumidity_probabilities.iloc[i]] for i in range(len(relativehumidity_probabilities))]
    cloudcover_probabilities_2d = [[cloudcover_probabilities.iloc[i]] for i in range(len(cloudcover_probabilities))]
    #print(temperature_probabilities_2d)
    # In[2]

    #print(temperature_probabilities_2d)
    #print(cloud_prob_yes)



    cpd_temp = TabularCPD(variable='temperature', variable_card=3, values=temperature_probabilities_2d, state_names={'temperature':['Cold', 'Mild', 'Hot']})
    cpd_hum = TabularCPD(variable='relativehumidity', variable_card=2, values=relativehumidity_probabilities_2d, state_names={'relativehumidity':['Low', 'High']})
    cpd_cloud = TabularCPD(variable='cloudcover', variable_card=2, values=cloudcover_probabilities_2d, state_names={'cloudcover':['Clear', 'Cloudy']})

    cpd_rain_values = rp.cpd_rain_values
    cpd_rain_values_transposed = list(map(list, zip(*cpd_rain_values)))
    #print(cpd_rain_values)
    # In[122]:
    '''
    cpd_rain_values = [
        [0.8097165991902834, 0.1767881241565452, 0.01349527665317139, 0.0, 0.0, 0.0, 0.0020242914979757085, 0.0, 0.8211875843454791, 0.1767881241565452, 0.004048582995951417, 0.0, 0.8191632928475033, 0.1767881241565452],  # probabilities for 'yes'
        [0.1902834008097166, 0.8232118758434548, 0.9865047233468286, 1.0, 1.0, 1.0, 0.9979757085020243, 1.0, 0.1788124156545209, 0.8232118758434548, 0.9959514170040485, 1.0, 0.18083670715249664, 0.8232118758434548]  # probabilities for 'no'
    ]
    '''
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

    #prob = model.get_state_probability(var)
    #assert model.check_model()

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