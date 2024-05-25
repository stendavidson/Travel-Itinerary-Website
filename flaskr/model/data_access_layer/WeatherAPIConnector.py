import requests
from threading import Thread, Lock

from flaskr.model.exceptions.WeatherRequestException import WeatherRequestException
from flaskr.model.exceptions.InvalidLocationException import InvalidLocationException
from flaskr.model.Weather import Weather



class WeatherAPIConnector :
    """
    This class provides a mechanism by which weather data can be retrieved from the
    OpenWeather API.
    """

    # This url is the current weather data api endpoint
    URL = "https://api.openweathermap.org/data/2.5/weather"


    def __init__(self, api_key : str) -> None :
        """
        WeatherAPIConnector object initializer

        Parameters:
            api_key (str): a valid OpenWeather API key.
        """

        self.url : str = self.URL + f"?appid={api_key}"

    
    def current_weather(self, latitude : float, longitude : float, units : str = "metric") -> Weather:
        """
        This method retrieves the current weather data can be from the OpenWeather API.

        Parameters:
            latitude (float): the latitude
            longitude (float): the latitude
            units (str): an optional paramter to set the units, "metric" by default.

        Returns:
            Weather: A Weather object encapsulating the Weather data retrieved from the api.
        """
        
        # Raise TypeError for invalid input type
        if (not isinstance(latitude, float) or (not isinstance(longitude, float))) :

            raise TypeError("Invalid argument, coordinates parameter must be of type tuple[float, float].")
        

        # Coordinates are validated
        if latitude < -90 or latitude > 90 or  longitude < -180  or longitude > 180 :

            raise InvalidLocationException((latitude, longitude))
        

        # The request is sent
        response = requests.get(self.url, params = {
            "lat" : latitude, 
            "lon" : longitude,
            "units" : units
            })
        

        weather_data : dict | None = None

        # The api response is validated
        if response.status_code == requests.codes.ok :

            try :
            
                weather_data = response.json()
            
            except requests.exceptions.JSONDecodeError as e :

                raise WeatherRequestException()
            
        else :

            raise WeatherRequestException()
        


        # A Weather object is created
        weather = Weather(
            latitude, 
            longitude,
            weather_data.get("main", dict()).get("temp", None),
            weather_data.get("main", dict()).get("temp_min", None),
            weather_data.get("main", dict()).get("temp_max", None), 
            weather_data.get("main", dict()).get("feels_like", None),
            weather_data.get("main", dict()).get("humidity", None),
            weather_data.get("weather", [dict()])[0].get("description", None),
            weather_data.get("wind", dict()).get("speed", None),
            weather_data.get("rain", dict()).get("1h", None),
            weather_data.get("visibility", None)
        )

        return weather
    


    def bulk_weather(self, coordinates : list[tuple[float, float]], units : str = "metric") -> list[Weather]:
        """
        This method retrieves the weather data corresponding to a list of coordinates. This
        method utilizes threading to perform a bulk request.

        Parameters:
            coordinates (list[tuple[float, flaot]]): a list of coordinates.
            units (str): an optional paramter to set the units, "metric" by default.

        Returns:
            list[Weather]: A list of Weather objects encapsulating the weather data retrieved
            from the api.
        """
        
        # The variable shared between threads - to stored weather data
        weather_list = [None for i in coordinates]

        # This function requests the data and then safely allocates the result to a shared
        # variable that is mutex locked.
        def threaded_weather(pos : int, thread_lock : Lock, latitude : float,\
                             longitude : float, units : str = "metric") -> None:
            
            weather = self.current_weather(latitude, longitude, units)
            
            # safely lock the thread
            with thread_lock :

                weather_list[pos] = weather

        # A container for the threads.
        threads = []

        # A mutex lock
        thread_lock = Lock()

        # Create threads
        for i in range(len(coordinates)) :

            threads.append(Thread(target=threaded_weather, kwargs={
                "pos" : i, 
                "thread_lock" : thread_lock, 
                "latitude" : coordinates[i][0], 
                "longitude" : coordinates[i][1], 
                "units" : units
            }))

            threads[i].start()


        # Join the threads to the main thread
        for j in range(len(coordinates)) :

            threads[j].join()


        # Exception handling
        for k in weather_list :

            if k == None :

                raise WeatherRequestException()

        return weather_list

        

        


        
        

                

            





        
        




        

        
        