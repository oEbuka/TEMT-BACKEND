
# Solar Irradiance Prediction API
This Flask app serves as an API for predicting solar irradiance based on several input parameters. The app uses a pre-trained machine learning model to make predictions.

## Usage
#### Create Virtual Environment

Run the following to create a virtual environment:

```bash
python -m venv env
```

Activate your newly created virtual environment by running:

```bash
source env/bin/activate 
```
```bash
    using windows cdm, navigate to your \env\Scripts then press the tab key to see 'activate' then press enter.
```

### Installation
To install the required dependencies, run the following command:

Copy code
```bash
pip install -r requirements.txt
```
## Running the App
To start the app, run the following command:

Copy code
```bash
python app.py
```
The app will run on [http://localhost:5000](http://localhost:5000) by default.

## Endpoints
### POST /predict
This endpoint accepts a JSON payload containing the following input parameters:

- temperature : the temperature in degrees Celsius`
- humidity : the relative humidity as a percentage
- pressure : the atmospheric pressure in hPa
- wind_direction : the wind direction in degrees
- wind_speed : the wind speed in m/s
- day_of_year : the day of the year (1-365)
- time_of_day : the time of day in seconds past midnight

## Example request:

```bash
 {
  "temperature": 20,
  "humidity": 50,
  "pressure": 1013.25,
  "wind_direction": 180,
  "wind_speed": 5,
  "day_of_year": 150,
  "time_of_day": 780
} 
```
### Example response:

json
```bash
{
  "solar_irradiance": 400
}
```
### If any of the input parameters are missing, the API will return an error with a status code of 400:

json
```bash
{
  "error": "Missing input parameters{parameter name}"
}
```

### POST /measure
This endpoint accepts a JSON payload containing the following input parameters:

- Average_household_income : the average income coming into each household annually
- Average_Business_Income : the average income coming into each business annually
- Average_Household_Costs : the average amount spent in each household annually
- Average_Business_Costs : the average amount spent in each business annually
- Estimated_Cost_Of_Project : the estimated amount to be spent on the project
- Estimated_Annual_Operational_Costs : the estimated amount to be spent yearly on the project operation

## Example request:

```bash
{
    "Average_household_income" : "900000", 
    "Average_Business_Income" : "60000000", 
    "Average_Household_Costs" : "300000", 
    "Average_Business_Costs" : "1500000", 
    "Estimated_Cost_Of_Project" :" 3000000", 
    "Estimated_Annual_Operational_Costs" : "700000"
} 
```
### Example response:

json
```bash
{
    "Average_SpendingPower_Of_Town": 59100000.0,
    "Net_Revenue": 11000000.0,
    "Potential_Revenue": 11820000.0,
    "Spread_Cost_of_Production": 120000.0
}

```
### If any of the input parameters are missing, the API will return an error with a status code of 400:

json
```bash
{
  "error": "Missing input parameters{parameter name}"
}
```


## Authors
- [Adetoki Timilehin](https://github.com/Adetoki-timilehin)
- [Obiora Chukwuebuka](https://github.com/oEbuka)
