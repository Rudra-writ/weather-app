from fastapi import FastAPI, Request, Form
from main.weather_app import WeatherApp
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()    #Creating a FastAPI instance
templates = Jinja2Templates(directory="templates/") #Creating a template object with the .html file in templates directory
app.mount("/static", StaticFiles(directory="static"), name="static") #Mounting the static files from the static directory

@app.get("/")
def form_post(request: Request):
    current_weather = {"temp": "N/A", "feels_like": "N/A", "humidity": "N/A", "pressure": "N/A", "wind_speed" : "N/A"} #When the app is launched, display not available for each weather parameter, initially
    
    return templates.TemplateResponse('first_page.html', context={'request': request, 'result': 'None', 'current_weather': current_weather}) # Returning the template response

@app.post("/")
def form_post(request: Request, city : str = Form(None)): #If the user clicks on the button, recieve the name of the city from the submitted form

    weather = WeatherApp(city)    #Creating an instance of the WeatherApp class
    current_weather = weather.current_weather()    #Calling the current_weather() method of the WeatherApp class
    five_days_forecast = weather.five_days_forecast()    #Calling the five_days_forecast() method of the WeatherApp Class
    message = ""

    if (current_weather == "no_response" or five_days_forecast == "no_response"):    #checking for error messages returned by the methods
        current_weather = {"overall_weather": "", "city":"", "temp": "", "feels_like": "", "humidity": "", "pressure": "", "wind_speed" : ""}    #Initializing the weather parameters of current weather as empty strings
        return templates.TemplateResponse('first_page.html', context={'request': request, 'message': "API call was unsuccesful, please check the API key", 'current_weather': current_weather})    #If either current_weather() or the five_days_forecast() method returns "no_response" message informing the user that the API call was not successful.
    
    elif (current_weather == "invalid_city" or five_days_forecast == "invalid_city"):    #checking for error messages returned by the methods
        current_weather = {"overall_weather": "", "city":"", "temp": "", "feels_like": "", "humidity": "", "pressure": "", "wind_speed" : ""}     #Initializing the weather parameters of current weather as empty strings
        return templates.TemplateResponse('first_page.html', context={'request': request, 'message': "City not found...Please try again!!", 'current_weather': current_weather})    #If either current_weather() or the five_days_forecast() method returns "invalid_city" message informing the user that the city is invalid
    
    else:
        message = ""
        return templates.TemplateResponse('first_page.html', context={'request': request, 'current_weather': current_weather, 'five_days_forecast': five_days_forecast, 'message': message}) #Otherwise, if everything is fine, returning the current weather and the five days forecast
