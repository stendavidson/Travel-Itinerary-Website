

class ItineraryRequestException(Exception) : # 500


    def __init__(self) -> None:

        super().__init__()


    def __str__(self) -> str:

        return f"Itinerary Request Exception: The itinerary data requested could not be retrieved."
    

    def __repr__(self) -> str:

        return f"ItineraryRequestException()"