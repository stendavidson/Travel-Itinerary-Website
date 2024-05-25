
# This exception class is a custom class, specific to the Itinerary
# data structure - and is raised when a location is stored twice.
class RepeatLocationException(Exception) :
    
    # Constructor
    def __init__(self, location : str) -> None:
        """
        RepeatLocationException object initializer

        Parameter:
            location (str): The plain text name of a location
        """

        self.location: str = location
        super().__init__()


    def __str__(self) -> str:
        """
        This method displays a plain text description of the exception's
        cause.
        """

        return f"The location requested {self.location}, already exists on the itinerary."
    

    def __repr__(self) -> str:
        """
        This method displays a plain text description of the exception's intialization
        for debugging purposes.
        """

        return f"RepeatLocationException({self.location})"