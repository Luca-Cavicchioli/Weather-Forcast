#data_list = [[lots of values]] con tutte le combinazioni in parentesi quadra

#pip install pgmy
from pgmpy.models import bayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
play_tennis = bayesianNetwork([('outlook','play tennis'),('humidity','play tennis'),
('temperature','play tennis'),('wind','playtennis')])

"""
outlook : sunny, overcast, rain
humidity : high, normal
wind: weak, strong
tennis : yes, no


"""
cpd = TabularCPD(
    'play tennis',
    2, #but a lot of connected values
    [
        [0, 0.5, 0.4] ,
        [1, 0.5, 0.6]
    ],
    evidence=['outlook','temperature','humidity','wind'],
    evidence_card=[3,3,2,2],
    state_names={'outlook': ['sunny','overcast','rain'], 'temperature':['hot','mild','cold'], 'humidity':['high','normal'],'wind':['strong','weak'],'play tennis':['yes','no']}

)
play_tennis.add_cpds(cpd)

#completare, ci sono errori ma la logica sembra chiara


cpd = TabularCPD(
    'outlook',
    3, #number of options written above
    [[0.4],[0.3],[0.3]],#example, it is the probability calculate with id3 algorithm(?)
    state_names={'outlook': ['sunny','overcast','rain']}
)
play_tennis.add_cpds(cpd)

cpd = TabularCPD(
    'Humidity',
    2,
    [[0.85],[0.15]],
    state_names={'temperature':['hot','mild','cold']}#graffe non tonde
)
play_tennis.add_cpds(cpd)

if play_tennis.check_model():
    print('ok')
    cpds = play_tennis.get_cpds()
    for cpd in cpds:
        print(cpd)
    var = {
        'outlook': 'sunny',
        'temperature': 'mild',
        'humidity': 'normal',
        'wind': 'weak',
        'play_tennis':'yes'

    }
    prob = play_tennis.get_state_probability(var)
    