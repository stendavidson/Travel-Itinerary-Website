

class LocationKeyException(Exception) :


    def __init__(self, location) :

        self.location = location
        super().__init__()


    def __str__(self) :

        return f"Location Key Exception: The location {self.location}, does not exist in this itinerary."
    

    def __repr__(self) :

        return f"LocationKeyException({self.location})"