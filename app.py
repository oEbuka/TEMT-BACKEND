from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the pre-trained machine learning model
model = joblib.load(r"C:\Users\1\Desktop\webdev\TEMT_Backend\model.pkl")


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
    Average_Individual_Income = request.json.get('Average_Individual_Income')
    Average_Business_Income = request.json.get('Average_Business_Income')
    Average_Transportation_Costs = request.json.get('Average_Transportation_Costs')
    Average_Healthcare_Costs = request.json.get('Average_Healthcare_Costs')
    Average_Miscellaneous_Expenses = request.json.get('Average_Miscellaneous_Expenses')
    Average_Household_Income = request.json.get('Average_Household_Income')
    Average_Housing_Costs = request.json.get('Average_Housing_Costs')
    Average_Food_Costs = request.json.get('Average_Food_Costs')
    Average_Education_Costs = request.json.get('Average_Education_Costs')

    # Validate input parameters
    #Average_Individual_Income, Average_Business_Income, Average_Transportation_Costs, Average_Healthcare_Costs, Average_Miscellaneous_Expenses, Average_Household_Income, Average_Housing_Costs, Average_Food_Costs, Average_Education_Costs
    missing_params = [param for param in ['Average_Individual_Income', 'Average_Business_Income', 'Average_Transportation_Costs', 'Average_Healthcare_Costs', 'Average_Miscellaneous_Expenses', 'Average_Household_Income', 'Average_Housing_Costs', 'Average_Food_Costs', 'Average_Education_Costs'] if request.json.get(param) is None]
    if missing_params:
        return jsonify({'error': f"Missing input parameters: {', '.join(missing_params)}"}), 400

    # Measure using the formulae
    Average_Total_Income = float(Average_Individual_Income) + float(Average_Housing_Costs)
    # Return Measurement
    return jsonify({' Average_Total_Income' : Average_Total_Income})

if __name__ == '__main__':
    app.run(debug=True)
