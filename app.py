from flask import Flask, request, jsonify, send_file, render_template
from io import BytesIO
import pdfkit
from flask_cors import CORS
from datetime import datetime
import joblib
import pickle
import os

#path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

app = Flask(__name__)
CORS(app)
# Load the pre-trained machine learning model
#model_path = os.path.join(os.getcwd(), 'model.pkl')
#model = joblib.load(model_path)
model_path = os.path.join(os.getcwd(), 'model.pkl')


#Home Page route
@app.route('/')
def Home():
    return "message : TEMT Energy"

# Define a route to handle incoming requests
@app.route('/predict', methods=['POST'])
def predict():
    # Extract the input parameters from the request {day_of_year: '2023-05-19', time_of_day: '17:47'}
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
    # Convert the date to day of the year
    date_object = datetime.strptime(day_of_year, '%Y-%m-%d')
    day_of_year = date_object.timetuple().tm_yday

     # Convert the time to seconds
    time_parts = time_of_day.split(':')
    time_seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60


    # Load the model from the pickle file
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    # Make a prediction using the pre-trained model
    # The input to the model should be in the form of a 2D array, with one row for each sample
    # In this case, we have only one sample, so we need to reshape the input to a 2D array with one row
    
    input_data = [[temperature, humidity, pressure, wind_direction, wind_speed, day_of_year, time_seconds]]
    prediction = model.predict(input_data)[0]
    prediction = int(prediction)
    

    # Return the predicted value as a JSON response
    return jsonify({'solar_irradiance': prediction})
    


# Generate the PDF report
#def generate_report(report_data):
    rendered_report = render_template('report_template.html', report=report_data)
    pdf = pdfkit.from_string(rendered_report, False, options={'encoding': 'UTF-8'})

    return pdf


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
    Average_SpendingPower_Households = int(Average_Household_Income) - int(Average_Household_Costs)
    Average_SpendingPower_Businesses = int(Average_Business_Income) - int(Average_Business_Costs)
    Average_SpendingPower_Of_Town = int(Average_SpendingPower_Businesses) + int(Average_SpendingPower_Households)
    Annual_Potential_Revenue = int((0.20) * Average_SpendingPower_Of_Town)
    Spread_Cost_of_Production = int(Estimated_Cost_Of_Project) // (25)
    Net_Revenue = Annual_Potential_Revenue - int(Estimated_Annual_Operational_Costs) - Spread_Cost_of_Production

    #report data
    def format_large_number(number):
        length = len(str(number))
        if length >= 13:
            trillions = number / 1_000_000_000_000
            return f'{trillions:.1f} trillion'
        elif length >= 10:
            billions = number / 1_000_000_000
            return f'{billions:.1f} billion'
        elif length >= 7:
            millions = number / 1_000_000
            return f'{millions:.1f} million'
        else:
            return number
    report_data = {
            'Average_SpendingPower_Of_Town': format_large_number(Average_SpendingPower_Of_Town),
            'Spread_Cost_of_Production': format_large_number(Spread_Cost_of_Production),
            'Potential_Revenue': format_large_number(Annual_Potential_Revenue),
            'Net_Revenue': format_large_number(Net_Revenue)
        }
    
    
    # Return Measurement
    return report_data

#@app.route('/measure/download', methods=['POST'])
#def download_report():
    
    Average_SpendingPower_Of_Town = request.json.get('Average_SpendingPower_Of_Town')
    Spread_Cost_of_Production = request.json.get('Spread_Cost_of_Production')
    Annual_Potential_Revenue = request.json.get('Annual_Potential_Revenue')
    Net_Revenue = request.json.get('Net_Revenue')
    
    # Generate the PDF report
    
    def format_large_number(number):
        length = len(str(number))
        if length >= 13:
            trillions = number / 1_000_000_000_000
            return f'{trillions:.1f} trillion'
        elif length >= 10:
            billions = number / 1_000_000_000
            return f'{billions:.1f} billion'
        elif length >= 7:
            millions = number / 1_000_000
            return f'{millions:.1f} million'
        else:
            return number
    
    report_data = {
        'Average_SpendingPower_Of_Town': format_large_number(Average_SpendingPower_Of_Town),
        'Spread_Cost_of_Production': format_large_number(Spread_Cost_of_Production),
        'Potential_Revenue': format_large_number(Annual_Potential_Revenue),
        'Net_Revenue': format_large_number(Net_Revenue)
    }

    # Generate the PDF report
   # pdf = generate_report(report_data)

    # Create a BytesIO stream and write the PDF data into it
    pdf_stream = BytesIO()
    pdf_stream.write(pdf)
    pdf_stream.seek(0)

    # Return the PDF file for download
    return send_file(
        pdf_stream,
        attachment_filename='market_viability_report.pdf',
        as_attachment=True,
        mimetype='application/pdf',
        charset='UTF-8'
    )

if __name__ == '__main__':
    app.run(debug=True)
