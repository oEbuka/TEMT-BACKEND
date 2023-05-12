
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


## Authors
- [Adetoki Timilehin]()
- [Obiora Chukwuebuka](https://github.com/oEbuka)
