from exceptions.RepeatLocationException import RepeatLocationException
from exceptions.LocationKeyException import LocationKeyException
from datetime import datetime

"""
The Weather class provides all the information that can be retrieved at any
point for a Weather Forecast entry.
"""
class Weather :

    def __init__(self, date_time : datetime, avg_temp : float, temp_min : float, temp_max : float, \
                 feels_like : float, humidity : float, description : str, wind_speed : float, \
                 rain : float, visibility : int) -> None :

        self.date_time : datetime = date_time
        self.avg_temp : float = avg_temp
        self.temp_min : float = temp_min
        self.temp_max : float = temp_max
        self.feels_like : float = feels_like
        self.humidity : float = humidity
        self.description : str = description
        self.wind_speed : float = wind_speed
        self.rain : float = rain
        self.visibility : int = visibility

