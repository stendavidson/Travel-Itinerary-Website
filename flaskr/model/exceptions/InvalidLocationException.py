
class InvalidLocationException(Exception) :
    """
    This exception class is a custom class, specific to the ItineraryConnector
    class - and is raised when the coordinates do not exist.    
    """

    def __init__(self, coordinates : tuple[float, float]) -> None:
        """
        InvalidLocationException object initializer

        Parameter:
            coordinates (tuple[float, float]): The coordinates that caused the exception.
        """

        self.coordinates: tuple[float, float] = coordinates
        super().__init__()


    def __str__(self) -> str:
        """
        This method displays a plain text description of the exception's
        cause.
        """

        return f"This location is invalid, the coordinates {self.coordinates} are not real coordinates."
    

    def __repr__(self) -> str:
        """
        This method displays a plain text description of the exception's intialization
        for debugging purposes.
        """

        return f"InvalidLocationException({self.coordinates})"