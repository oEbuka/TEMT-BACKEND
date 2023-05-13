from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the pre-trained machine learning model
model = joblib.load('model.pkl')


#Home Page route
@app.route('/')
def Home():
    return "message : TEMT Energy"

# Define a route to handle incoming requests
@app.route('/predict', methods=['POST'])
def predict():
    # Extract the input parameters from the request
    temperature = request.json.get('temperature')
    humidity = request.json.get('humidity')
    pressure = request.json.get('pressure')
    wind_direction = request.json.get('wind_direction')
    wind_speed = request.json.get('wind_speed')
    day_of_year = request.json.get('day_of_year')
    time_of_day = request.json.get('time_of_day')

    # Validate input parameters
    missing_params = [param for param in ['temperature', 'humidity', 'pressure', 'wind_direction', 'wind_speed', 'day_of_year', 'time_of_day'] if request.json.get(param) is None]
    if missing_params:
        return jsonify({'error': f"Missing input parameters: {', '.join(missing_params)}"}), 400


    # Make a prediction using the pre-trained model
    # The input to the model should be in the form of a 2D array, with one row for each sample
    # In this case, we have only one sample, so we need to reshape the input to a 2D array with one row
    
    input_data = [[temperature, humidity, pressure, wind_direction, wind_speed, day_of_year, time_of_day]]
    prediction = model.predict(input_data)[0]
    

    # Return the predicted value as a JSON response
    return jsonify({'solar_irradiance': prediction})
    


# Route to measure market viability
@app.route('/measure', methods=['POST'])
def measure():
    # Extract the input parameters to be calculated from the request
    Average_Household_Income = request.json.get('Average_Household_Income')
    Average_Business_Income = request.json.get('Average_Business_Income')
    Average_Household_Costs = request.json.get('Average_Household_Costs')
    Average_Business_Costs = request.json.get('Average_Business_Costs')
    Estimated_Cost_Of_Project = request.json.get('Estimated_Cost_Of_Project')
    Estimated_Annual_Operational_Costs = request.json.get('Estimated_Annual_Operational_Costs')

    # Validate input parameters
    missing_params = [param for param in ['Average_Household_Income', 'Average_Business_Income', 'Average_Household_Costs', 'Average_Business_Costs', 'Estimated_Cost_Of_Project', 'Estimated_Annual_Operational_Costs'] if request.json.get(param) is None]
    if missing_params:
        return jsonify({'error': f"Missing input parameters: {', '.join(missing_params)}"}), 400

    # Measure using the formulae
    Average_SpendingPower_Households = float(Average_Household_Income) - float(Average_Household_Costs)
    Average_SpendingPower_Businesses = float(Average_Business_Income) - float(Average_Business_Costs)
    Average_SpendingPower_Of_Town = float(Average_SpendingPower_Businesses) + float(Average_SpendingPower_Households)
    Annual_Potential_Revenue = (0.20) * Average_SpendingPower_Of_Town
    Spread_Cost_of_Production = float(Estimated_Cost_Of_Project) / (25)
    Net_Revenue = Annual_Potential_Revenue - float(Estimated_Annual_Operational_Costs) - Spread_Cost_of_Production


    # Return Measurement
    return jsonify({'Average_SpendingPower_Of_Town' : Average_SpendingPower_Of_Town,
                    'Spread_Cost_of_Production': Spread_Cost_of_Production,
                    'Potential_Revenue' :Annual_Potential_Revenue,
                    'Net_Revenue' : Net_Revenue
                    })

if __name__ == '__main__':
    app.run(debug=True)
