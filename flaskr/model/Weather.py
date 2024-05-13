from exceptions.RepeatLocationException import RepeatLocationException
from exceptions.LocationKeyException import LocationKeyException
from datetime import datetime

"""
The Weather class provides all the information that can be retrieved at any
point for a Weather Forecast entry.
"""
class Weather :

    def __init__(self, date_time : datetime , current_temp : float | None,\
                 min_temp : float | None, max_temp : float | None, feels_like : float | None,\
                 humidity : float | None, description : str | None,wind_speed : float | None,\
                 rain_prob : float | None, rain : float | None, visibility : int | None) -> None :

        self.date_time : datetime = date_time
        self.current_temp : float = current_temp
        self.min_temp : float = min_temp
        self.max_temp : float = max_temp
        self.feels_like : float = feels_like
        self.humidity : float = humidity
        self.description : str = description
        self.wind_speed : float = wind_speed
        self.rain_prob : float = rain_prob
        self.rain : float = rain
        self.visibility : int = visibility


        
