import requests
from flask import Flask , render_template , request

API_KEY = "xxx"
OPENWEATHERAPI_ENDPOINT="https://api.openweathermap.org/data/2.5/weather"
ZIPCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/zip"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=['POST'])
def receive_data():
    zip_code = request.form["zipcode"]
    zipcode_params = {
        "zip": zip_code,
        "country code" : "US",
        "appid" : API_KEY
         }

    response = requests.get(url=ZIPCODE_ENDPOINT , params= zipcode_params)
    response.raise_for_status()
    result = response.json()
    lat_value = result["lat"]
    lon_value = result["lon"]

    # get the weather data for your zipcode from above lat and lon values

    weather_params = {
        "lat" : lat_value ,
        "lon" : lon_value ,
        "units" : "metric" ,
        "appid" :  API_KEY
    }

    response_weather_data = requests.get(url=OPENWEATHERAPI_ENDPOINT , params= weather_params)
    response_weather_data.raise_for_status()
    result_current_weather_data = response_weather_data.json()
    main_data = result_current_weather_data['weather'][0]['main']
    description = result_current_weather_data['weather'][0]['description']
    temp = result_current_weather_data['main']['temp']
    feels_like = result_current_weather_data['main']['feels_like']
    
    data = {
        "main" : main_data ,
        "description" : description ,
        "temp" : temp,
        "feels_like" : feels_like
    }
    return f"<h2>  Current Weather looks like  {data['description']} <br> Feels like : {data['feels_like']}C <br> Temperature is : {data['temp']}C  </h2>"

if __name__ == "__main__":
    app.run(debug=True)


