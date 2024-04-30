from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)

OPENWEATHERMAP_API_KEY = '3656096e864188f8e7bfaf3be3577e51'

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for getting weather by coordinates
@app.route('/weather_by_coordinates')
def get_weather_by_coordinates():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    if not latitude or not longitude:
        return render_template('error.html', message="Harap berikan parameter lintang dan bujur.")

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHERMAP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return render_template('error.html', message=f"Gagal mengambil data cuaca. Error: {data['message']}")

    weather_description = data['weather'][0]['description']
    temperature_kelvin = data['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15

    return render_template('weather.html', location=f"Coordinates ({latitude}, {longitude})", weather=weather_description, temperature=temperature_celsius)


# Route for getting weather by postal code
@app.route('/weather_by_postal_code')
def get_weather_by_postal_code():
    postal_code = request.args.get('postal_code')

    if not postal_code:
        return render_template('error.html', message="Harap berikan parameter kode pos.")

    url = f"http://api.openweathermap.org/data/2.5/weather?zip={postal_code}&appid={OPENWEATHERMAP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return render_template('error.html', message=f"Gagal mengambil data cuaca. Error: {data['message']}")

    weather_description = data['weather'][0]['description']
    temperature_kelvin = data['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15

    return render_template('weather.html', location=f"Postal code {postal_code}", weather=weather_description, temperature=temperature_celsius)

# Route for getting weather by location
@app.route('/weather')
def get_weather():  
    location = request.args.get('location')
    if not location:
        return render_template('error.html', message="Harap berikan parameter lokasi.")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return render_template('error.html', message=f"Gagal mengambil data cuaca. Error: {data['message']}")

    weather_description = data['weather'][0]['description']
    temperature_kelvin = data['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15

    return render_template('weather.html', location=location, weather=weather_description, temperature=temperature_celsius)

# Route for getting weather forecast for the next 5 days
@app.route('/weather_forecast')
def get_weather_forecast():
    location = request.args.get('location')

    if not location:
        return render_template('error.html', message="Harap berikan parameter lokasi.")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHERMAP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return render_template('error.html', message=f"Gagal mengambil data ramalan cuaca. Error: {data['message']}")

    # Extract weather forecast data for the next 5 days
    forecast_data = []
    for entry in data['list']:
        forecast_time = entry['dt_txt']
        weather_description = entry['weather'][0]['description']
        temperature_kelvin = entry['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15
        forecast_data.append({'time': forecast_time, 'weather': weather_description, 'temperature': temperature_celsius})

    return render_template('weather_forecast.html', location=location, forecast_data=forecast_data)



if __name__ == "__main__":
    app.run(debug=True)


