import requests

from flaskr.model.exceptions.GeocodeRequestException import GeocodeRequestException


class GeocodeApiConnector :
    """
    This class provides a mechanism by which location data can be retrieved
    from google's geocode api.
    """

    
    # This url is the url for the google "geocode" api
    URL_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json"

    
    def __init__(self, api_key : str) -> None :
        
        """
        GeocodeApiConnector object initializer

        Parameters:
            api_key (str): a google cloud api key.
        """

        self.url_geocode : str = self.URL_GEOCODE + f"?key={api_key}"   


    def request_coordinates(self, location : str) -> tuple[float, float] :

        """
        This method retrieves the coordinates corresponding to an input location name.

        Parameters:
            location (str): the plain text description address or name of a certain 
            location.

        Returns:
            tuple: the latitude and longitude of the location.
        """

        # Input validation
        if (not isinstance(location, str)) :

            raise TypeError("Invalid input parameters: location => str and lang => str.")

        # The request is sent
        response = requests.get(self.url_geocode, params = {
            "address" : location
        })

        json_data : dict | None = None

        # The api response is validated
        if response.status_code == requests.codes.ok :

            try :
            
                json_data = response.json()
            
            except requests.exceptions.JSONDecodeError as e :

                raise GeocodeRequestException()
            
        else :

            raise GeocodeRequestException()
        
        
        coordinates = ()

        # Results validation
        if json_data["results"] != [] :

            location = json_data["results"][0]["geometry"]["location"]

            coordinates = (location["lat"], location["lng"])

        return coordinates


        
        

                

            





        
        




        

        
        
