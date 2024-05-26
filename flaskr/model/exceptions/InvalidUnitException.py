

class InvalidUnitException(Exception) : 
    """
    This exception class is a custom class, specific to the WeatherAPIConnector
    class - and is raised when an invalid unit type is passed.
    """

    def __init__(self, units : str) -> None:
        """
        InvalidMetricException object initializer

        Parameters:
            units (str): the invalid unit type
        """

        self.units = units

        super().__init__()


    def __str__(self) -> str:
        """
        This method displays a plain text description of the exception's
        cause.
        """

        return f"Invalid request, the unit type {self.units} is invalid - only " +\
                "metric and imperial are accepted values."
    

    def __repr__(self) -> str:
        """
        This method displays a plain text description of the exception's intialization
        for debugging purposes.
        """

        return f"WeatherRequestException()"