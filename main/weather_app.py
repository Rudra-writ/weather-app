# importing requests and json
import requests, json
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import datetime
import math
import urllib.request
from PIL import Image
import os
 
class WeatherApp:

     API_KEY = "33eda175e811c6c24c8714b80135937c" #Defining the API key for OpenWeatherMap as class variable

     def __init__(self, city):
          self.city = city

     ''' Method to obtain current time, location and the country of the city entered by the user '''
     def location_finder(self):

          try:
               city = self.city.lower()    #Converting the city name entered by the user to lower case
               geolocator = Nominatim(user_agent = "geoapiExercises")    #Used the geopy library to create a Nominatim instance
               location = geolocator.geocode(city)    #Use the instance to find the location information of the given city by creating a geocode instanse
               country = str(location).split(',')[-1]    #The variable location cotains name of the city, state and country in the last position. The country name is obtained using the split() function
               tz = TimezoneFinder()    #An instance of TimezoneFinder is created
               country_time_zone = tz.timezone_at(lng = location.longitude, lat = location.latitude ) #The time zone of the country is obtained by passing the latitude and longitude of the city to the timezone_at method of the TimeZonefinder class
               current_time = datetime.datetime.now(pytz.timezone(country_time_zone)) #Using the date time module to find the current time of the input city. The pytz module is used to convert the string object, "country_time_zone" to a tzinfo subclass (which is a valid tzinfo argument for datetime.now())

               return current_time,location,city,country
          except:
               return None  #returning None if the city entered by the user is invalid and hence valid informations cannot be obtained

         
     '''Method to obtain the current weather from the OpenWeatherMap using 'Current Weather Data' '''
     def current_weather(self):

          if self.location_finder() != None:
               current_time,location,city, country= self.location_finder()    #calling the location_finder method to get the required information
               current_time = current_time.strftime("%d,%B,%Y  %H:%M")    #converting the current time to a desired format for aesthetic purpose
               city_country = city.capitalize() + "," + country    #Capitalize the first letter of the city name and concat it with country

               BASE_URL_CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?" #Defining the base url for the API call to current weather data
               

               
               URL_CURRENT_WEATHER = BASE_URL_CURRENT_WEATHER + "lat=" + str(location.latitude) + "&lon=" + str(location.longitude) + "&appid=" + WeatherApp.API_KEY    #Create the complete URL by concating the latitude and longitude of the city and the API key

               response_current_weather = requests.get(URL_CURRENT_WEATHER)    #Initiating an API call to the above url, using the requests library
               

               if response_current_weather.status_code == 200 :     
                    
                    '''If the status code is 200, the snippet below, parses the json response received using the json() library
                       and extracts 8 weather parameters from it including the weather icon '''

                    data_cw = response_current_weather.json()
                    overall_weather = data_cw["weather"][0]["main"]
                    overall_weather_description = data_cw["weather"][0]["description"]
                    temperature = str(round((float(data_cw["main"]["temp"]) - 273.15),2)) #converting the temperature to celcius from kelvin
                    feels_like = str(round((float(data_cw["main"]["feels_like"]) - 273.15),2)) 
                    humidity = str(data_cw["main"]["humidity"]) 
                    pressure = str(data_cw["main"]["pressure"])
                    wind_speed = str(data_cw["wind"]["speed"]) 
                    icon = data_cw["weather"][0]["icon"]
                    #The line below creates a dictionary of the obtained parameters to be returned and used in the front end code.
                    current_weather_list = {"overall_weather": overall_weather, "overall_weather_dec": overall_weather_description, "temp": temperature, "feels_like": feels_like, "humidity": humidity, "pressure": pressure, "wind_speed" : wind_speed, "city": city_country, "current_time": current_time}
                    
                    try:
                         os.remove('/weather_app/static/images/icon.png')    #if the previous weather icon exists, it has to be removed to render the new icon. If the app is being run for the first time, there is no icon and hence exception handling is used to prevent this line from throwing error.
                    except:
                         pass
                    
                    urllib.request.urlretrieve("http://openweathermap.org/img/w/"+icon+".png",icon+".png")    #Using Urlib library to retrieve the weather icon from openweathermap using the icon id extracted from json response
                    img = Image.open(icon+'.png')
                    img = img.save("/weather_app/static/images/icon.png")   #saving the image under static/images/, to be rendered in the html response.
               
                    
                    return current_weather_list

               else:
                    return "no_response"    #if the status code is not 200 returning a custom message for error handling

          else:
               return "invalid_city"    #if the city entered doesn't exit returning a custom message for error handling


     '''Method to obtain the weather forecast from the OpenWeatherMap using '5 day/3 hour forecast' '''
     def five_days_forecast(self):
          
          if self.location_finder() != None:
               current_time,location,city,country = self.location_finder()    #calling the location_finder method to get the required information

               BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast?"    #Defining the base url for the API call to 5 day/3 hour forecast
               URL_FORECAST = BASE_URL_FORECAST + "lat=" + str(location.latitude) + "&lon=" + str(location.longitude) + "&appid=" + WeatherApp.API_KEY    #Creating the complete URL by concating the latitude and longitude of the city and the API key
               response_forecast = requests.get(URL_FORECAST)    #Initiating an API call to the above url, using the requests library

               if  response_forecast.status_code == 200:

                    '''If the status code is 200, the snippet below, parses the json response received using the json() library
                       and extracts the 'list' of dictionaries from it which contains sub informations of interest '''

                    data_forecast = response_forecast.json()
                    forecast_five_days = data_forecast["list"]
                    forecast_list_five_days = []

               
                    for main in forecast_five_days:

                         date_time = datetime.datetime.strptime(main["dt_txt"], '%Y-%m-%d %H:%M:%S')    #Converting the date time string from the Json response to date time object
                         date_time = date_time.strftime("%d,%b %H:%M")    #Converting the date time object to desired format for aesthetic purposes
                         forecast_list_five_days.append({ "weather": main["weather"][0]["main"] ,"temp_f": round(float(main["main"]["temp"] - 273.15),2),"humidity_f": main["main"]["humidity"], "wind_speed_f": main["wind"]["speed"], "dt": date_time} )    #Creating a list of dictionaries, containing few weather forecast parameters at particular time stamps


                    return forecast_list_five_days
               
               else:
                    return "no_response"    #if the status code is not 200 returning a custom message for error handling

          else:
               return "invalid_city"    #if the city entered doesn't exit returning a custom message for error handling


          
          


          



         