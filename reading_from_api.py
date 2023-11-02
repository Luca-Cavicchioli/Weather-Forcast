import requests
import json
import pandas

#pip install request
#pip install json

aPI_Address = "http OPEN METEO"
#GET API LINK
#it will give dataset csv

#timezone auto is laptop location, if you are constantly in one place

#this method is for not having file on the laptop

answer = requests.get(aPI_Address)
if answer.status_code == 200:
    print(":)")

    #2000 - all is well you can continue
    #40x - page not found
    #50x, 30x- server down
    #200 - not usefull data (maybe, check)

    data = answer.text
   # print(data) #to see what's in there

    data = json.loads(data)
    print(type(data))
    # json.dumps(data, indent=4)
    print(len(data))
    # dict - key values
    for k in data.keys():
        print(f"'[key]'", end=",") #la quadra è una graffa
    print()
    print(data["latitude"])
    print(len(data["hourly"]))
    for key in data["hourly"].keys():
        print(f"'[key]'", end=",") #quadra è graffa
    print()
    data_table = pandas.DataFrame(data["hourly"])
    print(data_table)


    

