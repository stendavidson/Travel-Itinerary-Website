

class WeatherRequestException(Exception) : 
    """
    This exception class is a custom class, specific to the WeatherAPIConnector
    class - and is raised when the API returns an unexpected response or error.
    """

    def __init__(self) -> None:
        """
        WeatherRequestException object initializer
        """

        super().__init__()


    def __str__(self) -> str:
        """
        This method displays a plain text description of the exception's
        cause.
        """

        return f"The weather data requested could not be retrieved."
    

    def __repr__(self) -> str:
        """
        This method displays a plain text description of the exception's intialization
        for debugging purposes.
        """

        return f"WeatherRequestException()"