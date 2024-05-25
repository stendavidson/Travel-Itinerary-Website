
class GeocodeRequestException(Exception) :
    """
    This exception class is a custom class, specific to the GeocodeAPIConnector
    class - and is raised when the Google Geocode API returns an unexpected 
    response or error.
    """

    def __init__(self) -> None:
        """
        GeocodeRequestException object initializer
        """

        super().__init__()

    def __str__(self) -> str:
        """
        This method displays a plain text description of the exception's cause.
        """

        return f"The location data requested could not be retrieved."
    

    def __repr__(self) -> str:
        """
        This method displays a plain text description of the exception's intialization
        for debugging purposes.
        """

        return f"LocationRequestException()"