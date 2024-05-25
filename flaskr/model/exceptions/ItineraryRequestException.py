

class ItineraryRequestException(Exception) :
    """
    This exception class is a custom class specific to the ItineraryRequestException
    class.
    """


    def __init__(self, error_message : str) -> None:
        """
        ItineraryRequestException object initializer

        Parameter:
            error_message (str): The plain text cause of the exception.
        """

        self.error_message : str = error_message
        super().__init__()


    def __str__(self) -> str:
        """
        This method displays a plain text description of the exception's
        cause.
        """

        return f"Something went wrong while accessing the itinerary service: {self.error_message}."
    

    def __repr__(self) -> str:
        """
        This method displays a plain text description of the exception's intialization
        for debugging purposes.
        """

        return f"ItineraryRequestException({self.error_message})"