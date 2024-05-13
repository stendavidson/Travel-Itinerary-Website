

class WeatherRequestException(Exception) : # 500


    def __init__(self) -> None:

        super().__init__()


    def __str__(self) -> str:

        return f"Weather Request Exception: The weather data requested could not be retrieved."
    

    def __repr__(self) -> str:

        return f"WeatherRequestException()"