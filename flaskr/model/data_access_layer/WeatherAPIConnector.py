import requests
from datetime import datetime
import pytz

from exceptions.WeatherRequestException import WeatherRequestException
from Weather import Weather


class WeatherConnector :

    VAR_URL = "api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key : str) -> None :

        self.url : str = self.VAR_URL + f"?appid={api_key}&lang=en&units=metric"

    
    def request(self, latitude : float, longitude : float) -> Weather :
        
        response = requests.get(self.url, params = {"lat" : latitude, "lon" : longitude})

        json_data : dict | None = None

        if response.status_code == requests.codes.ok :

            try :
            
                json_data = response.json()
            
            except requests.exceptions.JSONDecodeError as e :

                raise WeatherRequestException() # 500
            
        else :

            raise WeatherRequestException() # 500
        
        weather_data = json_data["list"][0]
        
        weather = Weather(
            datetime.fromtimestamp(weather_data["dt"], pytz.utc),
            weather_data.get("temp", None),
            weather_data.get("temp_min", None),
            weather_data.get("temp_max", None), 
            weather_data.get("feels_like", None),
            weather_data.get("humidity", None),
            weather_data.get("weather", dict()).get("description", None),
            weather_data.get("wind", dict()).get("speed", None),
            weather_data.get("pop", None),
            weather_data.get("rain", dict()).get("3h", None),
            weather_data.get("visibility", None)
        )

        return weather
    

    def request_bulk(self, latitude : float, longitude : float, num : int = 40) -> list[Weather] :

        response = requests.get(self.url, params = {"lat" : latitude, "lon" : longitude, "cnt" : num})

        json_data : dict | None = None

        if response.status_code == requests.codes.ok :

            try :
            
                json_data = response.json()
            
            except requests.exceptions.JSONDecodeError as e :

                raise WeatherRequestException() # 500
            
        else :

            raise WeatherRequestException() # 500

        forecast = []

        for weather_data in json_data["list"] :

            forecast.append(Weather(
                datetime.fromtimestamp(weather_data["dt"], pytz.utc),
                weather_data.get("temp", None),
                weather_data.get("temp_min", None),
                weather_data.get("temp_max", None), 
                weather_data.get("feels_like", None),
                weather_data.get("humidity", None),
                weather_data.get("weather", dict()).get("description", None),
                weather_data.get("wind", dict()).get("speed", None),
                weather_data.get("pop", None),
                weather_data.get("rain", dict()).get("3h", None),
                weather_data.get("visibility", None)
            ))

        return forecast


        
        

                

            





        
        




        

        
        