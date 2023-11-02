import pandas

#pip install pandas
#pip install numpy
#<1.21
#>1.24
#xlsx - openpyxl
#xls - xlrd, xlwt

file_address=".https://archive-api.open-meteo.com/v1/archive?latitude=45.508256&longitude=10.13164&start_date=2010-01-01&end_date=2019-12-31&hourly=temperature_2m,relativehumidity_2m,precipitation,cloudcover,windspeed_10m&timezone=Europe%2FBerlin"

# execute in directory

file = pandas.read_csv(file_address, skiprows=3)
print(file)
print(file.head())
print(file.tail())
print(file.sample())
print(file.iloc[10])

print(file.shape)
print(file.shape[0])
print(file.columns)
print(file["temperature_2m (°C)"].isnull().sum())
print(file[filter])

filter = file["time"] == "2020-01-01T03:00"
print(file[filter])


file = file.dropna()
print(file.shape)
print(file.dtypes)

# float64 = float
#int64 = int
#datetime64 = datatime + additional functions

#timedealta
#bool = bool
#category = pandas data type
#object = string / string + numbers / any other mix up of data types

#to_numbers to_datetime -> as type
#coerce or ignore
#m / M y/Y

#val = file["temp"].mean()
#file["temp"].fillna(val, inplace=true)
#median()
#mode()[0]
#mean - average, median - value in middle of list, mode - most used
