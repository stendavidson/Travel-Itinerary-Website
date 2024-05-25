

class Weather :
    """
    The Weather class encapsulate a distinct set of Weather data that can be retrieved
    via the OpenWeather API
    """

    
    def __init__(self, lat : float, lng : float, current_temp : float | None,\
                 min_temp : float | None, max_temp : float | None, feels_like : float | None,\
                 humidity : float | None, description : str | None,wind_speed : float | None,\
                 rain : float | None, visibility : int | None) -> None :
        """
        Weather object initializer.

        Parameters:
            lat (float): the latitude of the Weather data
            lng (float): the longitude of the Weather data
            current_temp (float | None): the current temperature
            min_temp (float | None): the minimum temperature
            max_temp (float | None): the maximum temperature
            feels_like (float | None): what the current temperature effectively feels like
            humidity (float | None): humidity in %
            description (str | None): the plain text description of the weather
            wind_speed (float | None): the windspeed
            rain (float | None): the volume of rain in mm.
            visibility (int | None): visibility distance in meters with a maximum of 10000.
        """

        self.coordinates : list[float, float] = [lat, lng]
        self.main : dict = {
            "current_temp" : current_temp,
            "min_temp" : min_temp,
            "max_temp" : max_temp,
            "feels_like" : feels_like,
            "humidity" : humidity,
            "description" : description,
            "wind_speed" : wind_speed,
            "rain" : rain,
            "visibility" : visibility
        }



        
