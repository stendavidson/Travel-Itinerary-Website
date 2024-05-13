

class RepeatLocationException(Exception) :


    def __init__(self, location : str) -> None:

        self.location = location
        super().__init__()


    def __str__(self) -> str:

        return f"Repeat Location Exception: The location {self.location}, already exists on the itinerary."
    

    def __repr__(self) -> str:

        return f"RepeatLocationException({self.location})"