#Weather App


Instructions to use the Weather App:

Navigate to "/weather_app" directory and run the command "pip install -r requirements.txt" to install the dependencies

Run the command "python -m uvicorn main.app:app --reload" to launch the application

Navigate to the link "http://127.0.0.1:8000" to use the application

The directory "weather_app/static/images/" contain some pre-downloaded images to serve as indicator icons namely, temperature, feels like, humidity, atmospheric pressure and wind speed. (These icons are constants, used for aesthetic purposes. These does not change unlike the dynamic weather icon pulled from 'openweathermap', when the user enters a city name.)
